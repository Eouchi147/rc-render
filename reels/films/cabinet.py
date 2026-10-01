"""The ledger cabinet: one continuous film for the verdict round-up of a File.

Every case of the File stands as a lit miniature in its own niche of a museum cabinet (the model is the case film's own
hero model, scaled down). The camera never cuts: it glides from niche to niche as the narrator names each case, and every
verdict is drawn, not written: a coloured frame traces itself around the niche, a small brass chip names the verdict,
and a gesture shows what the verdict means (the builders appear, a claimed layer is drawn dotted, a claimed date is struck
out, a question mark rises). At the end the camera pulls back and the whole cabinet is the ledger.

Grammar of the lines (the house style): solid = measured, dashed = inferred, dotted = claimed.
"""
import copy, math
from films import like

VCOL = {"strong": "#8fd9b0", "established": "#8fd9b0", "plausible": "#f2c98e", "awaiting": "#9fd0ff", "open": "#c9c1ee", "ruled": "#ff8a7a", "mixed": "#e8b87a"}
VWORD = {"strong": "STRONG EVIDENCE", "established": "ESTABLISHED", "plausible": "PLAUSIBLE", "awaiting": "AWAITING EVIDENCE", "open": "STILL OPEN",
         "ruled": "RULED OUT", "mixed": "MIXED RECORD"}
SHORT = {"strong": "STRONG", "established": "ESTABLISHED", "plausible": "PLAUSIBLE", "awaiting": "AWAITING", "open": "OPEN", "ruled": "RULED OUT", "mixed": "MIXED"}
WOOD, WOOD_D, BRASS, BONE = "#3b2a1c", "#1c140e", "#c9a86a", "#f5ecdc"
X0, X1, Y0, Y1 = 40, 960, 170, 1700          # the cabinet, in world units (the frame is 1000 x 1778)
C30 = math.cos(math.pi / 6)


def grid(n):
    if n <= 4:
        return 2, 2
    if n <= 6:
        return 2, 3
    if n <= 8:
        return 2, 4
    if n <= 9:
        return 3, 3
    return 3, 4


def _pts(it):
    """Corner points of an iso item (enough to bound it)."""
    t = it.get("t"); P = []
    if t == "box":
        for dx in (-.5, .5):
            for dz in (-.5, .5):
                for y in (it["y"], it["y"] + it["h"]):
                    P.append((it["x"] + dx * it["w"], y, it["z"] + dz * it["d"]))
    elif t == "slab":
        for x in (it["x0"], it["x1"]):
            for z in (it["z0"], it["z1"]):
                P.append((x, it.get("y", 0), z))
    elif t == "cyl":
        for a in range(0, 360, 45):
            for y in (it["y"], it["y"] + it["h"]):
                P.append((it["x"] + it["r"] * math.cos(math.radians(a)), y, it["z"] + it["r"] * math.sin(math.radians(a))))
    elif t == "prism":
        for q in it["pts"]:
            for y in (it.get("y", 0), it.get("y", 0) + it["h"]):
                P.append((q[0], y, q[1]))
    elif t == "pyr":
        h = it["b"] / 2
        P += [(it["x"] + a, it["y"], it["z"] + b) for a in (-h, h) for b in (-h, h)] + [(it["x"], it["y"] + it["h"], it["z"])]
    elif t == "ext":
        ax = it.get("axis", "x")
        for u, v in it["prof"]:
            for d in (-it["d"] / 2, it["d"] / 2):                      # the kit extrudes d/2 each side of `at`
                if ax == "x":
                    P.append((it["x"] + u, it.get("y", 0) + v, it.get("at", 0) + d))
                else:
                    P.append((it.get("at", 0) + d, it.get("y", 0) + v, it.get("z", 0) + u))
    elif t == "person":
        P += [(it["x"], it["y"], it["z"]), (it["x"], it["y"] + it.get("h", 1.7), it["z"])]
    elif t == "flat":
        P += [(q[0], it.get("y", 0), q[1]) for q in it["pts"]]
    elif t == "quad":
        P += [tuple(q) for q in it["p"]]
    elif t == "block":
        for x in (it["x0"], it["x1"]):
            for z in (it["z0"], it["z1"]):
                P.append((x, it.get("y", 0), z))
    return P


def bbox(items, az, el, S=1.0):
    """Screen bounding box (relative to the model origin) of iso items seen at azimuth az (degrees) and elevation el."""
    a = math.radians(az); ca, sa = math.cos(a), math.sin(a)
    xs, ys = [], []
    for it in items:
        for x, y, z in _pts(it):
            rx, rz = x * ca - z * sa, x * sa + z * ca
            xs.append((rx - rz) * C30 * S); ys.append(-y * S + (rx + rz) * el * S)
    if not xs:
        return -1, -1, 1, 1
    return min(xs), min(ys), max(xs), max(ys)


def drop_ids(ids):
    out = []
    for d in ids:
        out += [d, d + "g"]
    return out


class Cabinet:
    """cells: list of dicts {name, model (an iso element, or a list of plain elements in niche-local units)}; optional s, az, el, spin, dx, dy."""

    def __init__(self, cells, hmax=1.2):
        self.n = len(cells)
        self.cols, self.rows = grid(self.n)
        gap, pad = 26, 22
        self.w = (X1 - X0 - 2 * pad - (self.cols - 1) * gap) / self.cols
        self.h = (Y1 - Y0 - 2 * pad - (self.rows - 1) * gap) / self.rows
        self.h = min(self.h, self.w * hmax)                                   # no tall, empty niches: a short grid sits in the middle
        tall = 2 * pad + self.rows * self.h + (self.rows - 1) * gap
        self.Y0 = (Y0 + Y1) / 2 - tall / 2; self.Y1 = self.Y0 + tall
        self.cells = []
        for i, c in enumerate(cells):
            r, k = divmod(i, self.cols)
            x = X0 + pad + k * (self.w + gap); y = self.Y0 + pad + r * (self.h + gap)
            self.cells.append(dict(c, i=i, x=x, y=y, cx=x + self.w / 2, cy=y + self.h / 2))
        self.shots, self.chips, self.nid, self.cur = [], {}, 0, {}
        self._iso = {}

    # ---------- geometry ----------
    def floor(self, i):
        c = self.cells[i]; return c["y"] + self.h * .80

    def cam_cell(self, i, zk=.92, sy=780):
        """Close on one niche: it fills about 90 % of the frame width, its middle a little above the captions."""
        c = self.cells[i]; z = round(1000 * zk / self.w, 3)
        return [z, round(c["cx"], 1), round(c["cy"] - (sy - 860) / z, 1)]

    def cam_cells(self, ids, sy=790, margin=1.1):
        cs = [self.cells[i] for i in ids]
        x0 = min(c["x"] for c in cs); x1 = max(c["x"] for c in cs) + self.w
        y0 = min(c["y"] for c in cs); y1 = max(c["y"] for c in cs) + self.h
        z = round(min(1000 / ((x1 - x0) * margin), 1150 / ((y1 - y0) * margin)), 3)
        return [z, round((x0 + x1) / 2, 1), round((y0 + y1) / 2 - (sy - 860) / z, 1)]

    def cam_all(self, z=None, sy=740, k=1.0):
        """The whole cabinet (k < 1 pulls back further)."""
        z = round((z or min(.92, 1160 / (self.Y1 - self.Y0 + 36))) * k, 3)
        return [z, 500, round((self.Y0 + self.Y1) / 2 - (sy - 860) / z, 1)]

    # ---------- the cabinet itself ----------
    def build(self, cam=None, stagger=.48, t0=1.1):
        els = [{"k": "glow", "x": 500, "y": 900, "r": 1100, "kind": "lamp", "op": .10, "layer": "far"},
               {"k": "rect", "x": X0 - 18, "y": self.Y0 - 18, "w": X1 - X0 + 36, "h": self.Y1 - self.Y0 + 36, "r": 14, "fill": WOOD_D, "c": "#6b4f35", "sw": 3, "in": -1},
               {"k": "rect", "x": X0, "y": self.Y0, "w": X1 - X0, "h": self.Y1 - self.Y0, "r": 8, "fill": WOOD, "c": "#8a6a48", "sw": 1.5, "in": -1}]
        for c in self.cells:
            i = c["i"]; at = t0 + i * stagger
            fl = self.floor(i); pw = min(self.w * .66, 34 + len(c["name"]) * 12.5)
            els += [{"k": "rect", "x": c["x"], "y": c["y"], "w": self.w, "h": self.h, "r": 6, "fill": "#120d0a", "c": "#5a4330", "sw": 2, "in": -1},
                    {"k": "glow", "x": c["cx"], "y": c["y"] + self.h * .30, "r": self.w * .66, "kind": "lamp", "op": .5, "keepop": True, "in": at, "dur": 1.2},
                    {"k": "rect", "x": c["x"] + 10, "y": fl, "w": self.w - 20, "h": 12, "r": 3, "fill": "#4a3624", "c": "#7a5c3e", "sw": 1, "in": -1},
                    {"k": "rect", "x": c["cx"] - pw / 2, "y": fl + 20, "w": pw, "h": 34, "r": 5, "fill": "#2a1f15", "c": BRASS, "sw": 1.5, "in": -1},
                    {"k": "label", "x": c["cx"], "y": fl + 44, "t": c["name"], "st": "small", "c": "#ecd9b4", "size": 19, "scl": True, "halo": False, "in": at + .3}]
            els += self.model(i, at)
        s0 = {"base": "dark", "cam": cam or self.cam_all(), "els": els, "cont": True, "dir": {"move": "hold"}}
        self.shots = [s0]
        return 0

    def iso_of(self, i):
        """The niche's model as an iso element fitted to the niche (computed once)."""
        if i in self._iso:
            return self._iso[i]
        c = self.cells[i]; m = c["model"]
        e = copy.deepcopy(m)
        e["items"] = [it for it in e.get("items", []) if it.get("t") not in ("label", "q")]      # no text inside the niches
        az = c.get("az", e.get("az", -26)); el = c.get("el", .36); spin = c.get("spin", 1.4)
        solid = [it for it in e["items"] if it.get("t") != "line"]
        boxes = [bbox(solid, az + k * spin * 12, el) for k in range(6)]                           # the turn over about a minute
        bx0 = min(b[0] for b in boxes); by0 = min(b[1] for b in boxes); bx1 = max(b[2] for b in boxes); by1 = max(b[3] for b in boxes)
        S = c.get("s") or min(self.w * c.get("fw", .80) / (bx1 - bx0), self.h * c.get("fh", .56) / (by1 - by0))
        e.update(az=az, el=el, spin=spin, s=round(S, 3))
        e["x"] = round(c["cx"] - (bx0 + bx1) / 2 * S + c.get("dx", 0), 1)
        e["y"] = round(self.floor(i) - 8 - by1 * S + c.get("dy", 0), 1)
        self._iso[i] = e
        return e

    BG = {"map": "#1d3a4a", "sky": "#241f2e", "section": "#34281d", "paper": "#cdb58a", "plan": "#2b2219", "dark": "#120d0a", "land": "#241f2e"}
    TEXTK = {"label", "cap", "title", "para", "num", "q", "pin"}

    def window(self, i, shot, at, zk=1.0):
        """A framed window into the case film's own scene (for heroes that are maps, sections, papyri): no text inside."""
        c = self.cells[i]
        wx0, wy0 = c["x"] + 12, c["y"] + 12; ww, wh = self.w - 24, self.h * .80 - 22
        z, fx, fy = (shot.get("cam") or [1, 500, 860])[:3]
        fy = fy + c.get("wy", 0); fx = fx + c.get("wx", 0)
        sw = 1000 / z * .92 / zk; sh = sw * wh / ww; k = ww / sw
        els = []
        for e in shot.get("els", []):
            if e.get("k") in self.TEXTK:
                continue
            e = copy.deepcopy(e); e.pop("in", None); e.pop("layer", None)
            if e.get("k") == "iso":
                e["items"] = [it for it in e.get("items", []) if it.get("t") not in ("label", "q")]
            if e.get("k") == "map":
                e["land"] = e.get("land", [])
            els.append(e)
        tr = "translate(%.1f %.1f) scale(%.4f) translate(%.1f %.1f)" % (wx0 + ww / 2, wy0 + wh / 2, k, -fx, -fy)
        return [{"k": "group", "tr": tr, "clip": [round(fx - sw / 2, 1), round(fy - sh / 2, 1), round(sw, 1), round(sh, 1), 8 / k],
                 "bg": shot.get("bg") or self.BG.get(shot.get("base", "dark"), "#120d0a"), "els": els, "in": at, "dur": 1.0},
                {"k": "rect", "x": wx0, "y": wy0, "w": ww, "h": wh, "r": 8, "fill": "none", "c": BRASS, "sw": 2.5, "in": -1}]

    def model(self, i, at):
        c = self.cells[i]; m = c["model"]
        if isinstance(m, dict) and m.get("els") is not None and m.get("k") is None:        # a whole shot: show it through a window
            return self.window(i, m, at, c.get("zk", 1.0))
        if isinstance(m, dict) and m.get("k") == "iso":
            e = dict(self.iso_of(i)); e["in"] = at; e["fx"] = "rise"; e["dur"] = .9
            return [e]
        return [dict(x, **{"in": at if x.get("in") is None else x["in"]}) for x in self.local(i, m)]

    def local(self, i, els):
        """Elements written in niche-local units (0,0 = the middle of the shelf) moved into place."""
        c = self.cells[i]; ox, oy = c["cx"], self.floor(i)
        out = []
        for e in els:
            e = copy.deepcopy(e)
            for k in ("x", "x0", "x1", "x2", "tx"):
                if isinstance(e.get(k), (int, float)):
                    e[k] = round(e[k] + ox, 1)
            for k in ("y", "y0", "y1", "y2"):
                if isinstance(e.get(k), (int, float)):
                    e[k] = round(e[k] + oy, 1)
            if "p" in e:
                e["p"] = [[round(p[0] + ox, 1), round(p[1] + oy, 1)] + list(p[2:]) for p in e["p"]]
            out.append(e)
        return out

    def iso_like(self, i, items, **kw):
        """Extra iso items drawn with the niche model's own projection (a claimed layer, the builders)."""
        base = self.iso_of(i)
        e = {k: base[k] for k in ("x", "y", "s", "az", "spin", "el")}
        e.update(k="iso", items=items, **kw)
        return e

    # ---------- verdict gestures ----------
    def verdict(self, i, v, fact=None, at=.2, frame=True):
        """The niche frame traces itself in the verdict colour; a chip names the verdict (and, briefly, the fact)."""
        c = self.cells[i]; col = VCOL[v]; row = self.chips.get(i, 0); self.chips[i] = row + 1
        t = VWORD[v] if not fact else SHORT[v] + " · " + fact
        size = 17; cw = 28 + len(t) * size * .56
        if cw > self.w - 28:                                                  # a long fact: smaller type, never past the chip
            size = round((self.w - 56) / (len(t) * .56), 1); cw = self.w - 28
        out = []
        if frame:
            out.append({"k": "rect", "x": c["x"] + 4, "y": c["y"] + 4, "w": self.w - 8, "h": self.h - 8, "r": 6, "fill": "none", "c": col, "sw": 3,
                        "fx": "draw", "dur": 1.1, "in": at, "style": {"awaiting": "inferred", "open": "inferred", "plausible": "inferred"}.get(v, "known")})
        out += [{"k": "rect", "x": c["x"] + 14, "y": c["y"] + 14 + row * 42, "w": cw, "h": 32, "r": 16, "fill": "rgba(18,13,10,.86)", "c": col, "sw": 1.8, "in": at + .35, "fx": "pop"},
                {"k": "label", "x": c["x"] + 14 + cw / 2, "y": c["y"] + 36 + row * 42, "t": t, "st": "small", "c": col, "size": size, "scl": True, "halo": False, "in": at + .45}]
        return out

    def note(self, i, t, dx=None, dy=None, c=BONE, at=.8, size=30, a=None, stack=False):
        """A passing remark: shown while the camera is on this niche, gone when it leaves. By default it sits under the chips."""
        self.nid += 1; cc = self.cells[i]
        if dy is None:
            rows = self.chips.get(i, 0)
            base = max(cc["y"] + 34 + max(rows, getattr(self, "note_min_rows", 0)) * 42 + 12, self.cur.get(i, 0) + 34)   # note_min_rows keeps room for chips still to come
            k = 0
            if stack:                                          # stack under the notes already showing on this niche
                alive = {e.get("id") for e in (self.shots[-1]["els"] if self.shots else [])}
                k = sum(1 for nid, ci in getattr(self, "note_cell", {}).items() if ci == i and nid in alive)
            dx = cc["x"] + 22 - cc["cx"]; dy = base + k * (36 * self.w / 920) - self.floor(i); a = a or "start"
        self.note_cell = getattr(self, "note_cell", {}); self.note_cell["note%d" % self.nid] = i
        return self.local(i, [{"k": "label", "x": dx or 0, "y": dy, "t": t, "st": "small", "c": c, "size": size, "a": a or "middle", "in": at, "id": "note%d" % self.nid}])

    def struck(self, i, t, dx=0, dy=None, at=.5, size=22, rows=None):
        """A claim, shown dim with a dotted underline, then struck through in red. It stays (scaled with the cabinet).
        By default it sits just under the niche's chips."""
        if dy is None:
            dy = self.cells[i]["y"] + 14 + (self.chips.get(i, 0) if rows is None else rows) * 42 + 30 - self.floor(i)
        w = len(t) * size * .5
        self.cur[i] = self.floor(i) + dy + 14
        return self.local(i, [{"k": "rect", "x": dx - w / 2 - 16, "y": dy - size - 2, "w": w + 32, "h": size + 20, "r": (size + 20) / 2, "fill": "rgba(18,13,10,.78)", "c": "none", "sw": 0, "in": at, "dur": .5},
                              {"k": "label", "x": dx, "y": dy, "t": t, "st": "small", "c": "#cbbca8", "size": size, "scl": True, "in": at},
                              {"k": "line", "p": [[dx - w / 2, dy + 9], [dx + w / 2, dy + 9]], "c": "#cbbca8", "w": 2, "style": "claimed", "in": at + .1},
                              {"k": "line", "p": [[dx - w / 2 - 12, dy - 4], [dx + w / 2 + 12, dy - 12]], "c": VCOL["ruled"], "w": 5, "fx": "draw", "dur": .6, "in": at + .9}])

    def claim(self, i, t, dx=0, dy=None, at=.3, size=22, rows=None):
        """A claim written dim with a dotted underline (the verdict may strike it later: strike_claim)."""
        if dy is None:
            dy = self.cells[i]["y"] + 14 + (self.chips.get(i, 0) if rows is None else rows) * 42 + 30 - self.floor(i)
        w = len(t) * size * .5
        self.cur[i] = self.floor(i) + dy + 14
        self._claim = getattr(self, "_claim", {}); self._claim[i] = (dx, dy, w)
        return self.local(i, [{"k": "rect", "x": dx - w / 2 - 16, "y": dy - size - 2, "w": w + 32, "h": size + 20, "r": (size + 20) / 2, "fill": "rgba(18,13,10,.78)", "c": "none", "sw": 0, "in": at, "dur": .5},
                              {"k": "label", "x": dx, "y": dy, "t": t, "st": "small", "c": "#cbbca8", "size": size, "scl": True, "in": at},
                              {"k": "line", "p": [[dx - w / 2, dy + 9], [dx + w / 2, dy + 9]], "c": "#cbbca8", "w": 2, "style": "claimed", "in": at + .1}])

    def strike_claim(self, i, at=.2):
        dx, dy, w = self._claim[i]
        return self.local(i, [{"k": "line", "p": [[dx - w / 2 - 12, dy - 4], [dx + w / 2 + 12, dy - 12]], "c": VCOL["ruled"], "w": 5, "fx": "draw", "dur": .6, "in": at}])

    def question(self, i, dx=0, dy=-200, at=.3, size=90, c=None, id=None):
        """A question mark rising in the niche (id: so a later step can take it away)."""
        g = {"k": "glow", "x": dx, "y": dy - 26, "r": 100, "kind": "lamp", "op": .55, "keepop": True, "in": at}
        q = {"k": "label", "x": dx, "y": dy, "t": "?", "st": "big", "c": c or VCOL["open"], "size": size, "scl": True, "in": at, "fx": "pop", "dur": .8}
        if id:
            g["id"], q["id"] = id + "g", id
        return self.local(i, [g, q])

    def wash(self, i, col="#8fd9b0", at=.3, op=.16):
        """A soft coloured light over the whole niche (the land turns green, the fire, the flood)."""
        c = self.cells[i]
        return [{"k": "rect", "x": c["x"] + 6, "y": c["y"] + 6, "w": self.w - 12, "h": self.h * .8 - 8, "r": 6, "fill": col, "c": col, "sw": 0, "op": op, "keepop": True, "in": at, "dur": 1.2}]

    def sea(self, i, at=.3, frac=.34, op=.34, dur=1.8):
        """Water filling the niche from the shelf up (the sea rising over a coast). It stays."""
        c = self.cells[i]; fl = self.floor(i) + 6; h = (fl - c["y"] - 8) * frac
        return [{"k": "rect", "x": c["x"] + 6, "y": round(fl - h, 1), "w": self.w - 12, "h": round(h, 1), "r": 3, "fill": "#3f86a8", "c": "#3f86a8", "sw": 0,
                 "op": op, "keepop": True, "in": at, "dur": dur, "fx": "fill"},
                {"k": "line", "p": [[c["x"] + 8, round(fl - h, 1)], [c["x"] + self.w - 8, round(fl - h, 1)]], "c": "#9fd0ff", "w": 2, "op": .8, "keepop": True, "in": at + dur * .8, "dur": .8}]

    def route(self, i, j, col="#f2c98e", at=.3, style="known", bend=-80):
        """A line from one niche to another (trade, a journey, a borrowed idea)."""
        a, b = self.cells[i], self.cells[j]
        p0 = [a["cx"], a["cy"] - self.h * .1]; p1 = [b["cx"], b["cy"] - self.h * .1]
        mid = [(p0[0] + p1[0]) / 2 + bend, (p0[1] + p1[1]) / 2]
        return [{"k": "arrow", "p": [p0, mid, p1], "curve": True, "c": col, "w": 3, "style": style, "fx": "draw", "dur": 1.2, "in": at}]

    def people(self, i, n=3, x0=None, at=.3, h=36, gap=22):
        x0 = -self.w * .40 if x0 is None else x0
        return self.local(i, [{"k": "person", "x": x0 + k * gap, "y": -2, "h": h, "t": False, "color": "#e8d6b8", "in": at + k * .12, "fx": "rise"} for k in range(n)])

    # ---------- the shot chain ----------
    def step(self, cam=None, add=(), keep_notes=False, drop=()):
        """The next shot of the one continuous take: the camera glides to `cam`, `add` plays; passing notes (and any `drop` ids) leave."""
        gone = set(drop_ids(drop))
        if not keep_notes:
            gone |= {e.get("id") for e in self.shots[-1]["els"] if str(e.get("id", "")).startswith("note")}
        s = like(self.shots[-1], add=list(add), cam=cam or self.shots[-1]["cam"], drop=gone)
        s["cont"] = True; s["dir"] = {"move": "hold"}
        self.shots.append(s)
        return len(self.shots) - 1


# ---------- re-timing an existing script onto the cabinet ----------
import re as _re


def sentences(line):
    """Split a scripted line where a new acted sentence starts ([act:...], with any [d:]/[p:]/[go:] markup just before it)."""
    line = _re.sub(r"\[k:[^\]]*\]", "", line)                         # no big kicker titles over the cabinet
    line = _re.sub(r"\[go:[^\]]*\]", "", line)
    cuts = [m.start() for m in _re.finditer(r"(?:\[(?:d|p|gap|sfx):[^\]]*\])*\[act:", line)]
    if not cuts or cuts[0] != 0:
        cuts = [0] + cuts
    parts = [line[a:b] for a, b in zip(cuts, cuts[1:] + [len(line)])]
    return [p for p in parts if p]


def retime(beats, plan):
    """plan: {beat_index: (from_shot, {(line_index, sentence_index): 'N|glide'})}. Returns new beats with no cuts."""
    out = []
    for bi, b in enumerate(beats):
        frm, marks = plan[bi]
        lines = []
        for li, ln in enumerate(b["lines"]):
            ss = sentences(ln)
            lines.append("".join(("[go:%s]" % marks[(li, si)] if (li, si) in marks else "") + s for si, s in enumerate(ss)))
        out.append({"role": b["role"], "visual": {"from": frm}, "lines": lines})
    return out
