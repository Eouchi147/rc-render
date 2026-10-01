"""Giza geometry for the films, in metres, drawn to scale.
   Great Pyramid section (north-south, looking west, north on the left). Sources: Petrie 1883; Lehner 1997;
   Lehner & Hawass 2017; Morishima et al. 2017 (Big Void); Procureur et al. 2023 (North Face Corridor).
   Interior positions are approximate and labelled schematic where shown."""
import math

SLOPE = math.radians(51.84)
BASE, HEIGHT = 230.33, 146.6


class Section:
    """Metres to frame pixels: x metres south of the north edge, h metres above the base."""
    def __init__(self, s=3.6, cx=500, gy=1150):
        self.s, self.cx, self.gy = s, cx, gy

    def P(self, x, h):
        return [round(self.cx + (x - BASE / 2) * self.s, 1), round(self.gy - h * self.s, 1)]

    def outline(self):
        return [self.P(0, 0), self.P(BASE / 2, HEIGHT), self.P(BASE, 0)]

    # passages and rooms (approximate, after Lehner 1997 and Petrie 1883)
    def rooms(self):
        s = self
        ent = (17 / math.tan(SLOPE), 17.0)
        d = math.radians(26.5)
        junc = (ent[0] + 28.2 * math.cos(d), ent[1] - 28.2 * math.sin(d))
        sub = (ent[0] + 105 * math.cos(d), ent[1] - 105 * math.sin(d))           # descending passage reaches bedrock chamber c. 30 m down
        a = math.radians(26.0)
        gg0 = (junc[0] + 39.3 * math.cos(a), junc[1] + 39.3 * math.sin(a))
        gg1 = (gg0[0] + 46.7 * math.cos(a), gg0[1] + 46.7 * math.sin(a))
        qc = (BASE / 2, 21.2)
        kc = (gg1[0] + 7.5, 43.0)
        return dict(ent=ent, junc=junc, sub=sub, gg0=gg0, gg1=gg1, qc=qc, kc=kc)

    def els(self, which=("desc", "asc", "gg", "qc", "kc", "sub", "reliev"), c="#f5ecdc", fill="#0d0b09"):
        s, R = self, self.rooms()
        out = []
        if "desc" in which:
            out.append({"k": "line", "p": [s.P(*R["ent"]), s.P(*R["sub"])], "c": c, "w": 2.2, "id": "desc"})
        if "sub" in which:
            x, h = R["sub"]
            out.append({"k": "poly", "p": [s.P(x - 2, h + 1), s.P(x + 12, h + 1), s.P(x + 12, h - 3.5), s.P(x - 2, h - 3.5)], "fill": fill, "c": c, "w": 1.6, "id": "sub"})
        if "asc" in which:
            out.append({"k": "line", "p": [s.P(*R["junc"]), s.P(*R["gg0"])], "c": c, "w": 2.2, "id": "asc"})
        if "gg" in which:
            a = math.radians(26.0); nx, nh = -math.sin(a) * 8.6, math.cos(a) * 8.6
            g0, g1 = R["gg0"], R["gg1"]
            out.append({"k": "poly", "p": [s.P(*g0), s.P(*g1), s.P(g1[0] + nx, g1[1] + nh), s.P(g0[0] + nx, g0[1] + nh)], "fill": fill, "c": c, "w": 1.8, "id": "gg"})
        if "qc" in which:
            x, h = R["qc"]; g0 = R["gg0"]
            out.append({"k": "line", "p": [s.P(g0[0], g0[1]), s.P(x - 2.6, h)], "c": c, "w": 2.2, "id": "qcp"})
            out.append({"k": "poly", "p": [s.P(x - 2.6, h), s.P(x + 2.6, h), s.P(x + 2.6, h + 4.7), s.P(x, h + 6.2), s.P(x - 2.6, h + 4.7)], "fill": fill, "c": c, "w": 1.8, "id": "qc"})
        if "kc" in which:
            x, h = R["kc"]; g1 = R["gg1"]
            out.append({"k": "line", "p": [s.P(*g1), s.P(x - 2.6, h)], "c": c, "w": 2.2, "id": "kcp"})
            out.append({"k": "poly", "p": [s.P(x - 2.6, h), s.P(x + 2.6, h), s.P(x + 2.6, h + 5.8), s.P(x - 2.6, h + 5.8)], "fill": fill, "c": c, "w": 1.8, "id": "kc"})
        if "reliev" in which:
            x, h = R["kc"]
            for i in range(5):
                y0 = h + 5.8 + 1.2 + i * 2.6
                out.append({"k": "line", "p": [s.P(x - 2.6, y0), s.P(x + 2.6, y0)], "c": c, "w": 1.2, "op": .6, "id": f"rl{i}"})
            out.append({"k": "poly", "p": [s.P(x - 3.4, h + 18.6), s.P(x, h + 21.5), s.P(x + 3.4, h + 18.6)], "fill": "none", "c": c, "w": 1.2, "id": "rlg"})
        return out

    def body(self):
        return {"k": "poly", "p": self.outline(), "fill": "url(#k-blocks)", "c": "#f2dcb4", "w": 2.4, "id": "body"}

    def big_void(self, style="inferred"):
        """Big Void (Morishima et al. 2017): at least 30 m long, above the Grand Gallery, cross-section like it.
           Drawn parallel to the gallery about 12-15 m above it; the paper leaves its inclination open."""
        R = self.rooms(); a = math.radians(26.0)
        g0 = R["gg0"]
        t0, L, up = 14.0, 30.0, 16.0
        nx, nh = -math.sin(a), math.cos(a)
        p0 = (g0[0] + t0 * math.cos(a) + nx * up, g0[1] + t0 * math.sin(a) + nh * up)
        p1 = (p0[0] + L * math.cos(a), p0[1] + L * math.sin(a))
        h = 7.0
        pts = [self.P(*p0), self.P(*p1), self.P(p1[0] + nx * h, p1[1] + nh * h), self.P(p0[0] + nx * h, p0[1] + nh * h)]
        cx = sum(p[0] for p in pts) / 4; cy = sum(p[1] for p in pts) / 4
        return {"k": "poly", "p": pts, "fill": "rgba(159,208,255,.18)", "c": "#9fd0ff", "w": 2.4, "style": style, "id": "bv"}, (round(cx, 1), round(cy, 1))

    def nfc(self):
        """North Face Corridor (Procureur et al. 2023): c. 9 m long, 2 x 2 m, c. 20 m up, 0.8 m behind the chevrons."""
        h = 20.0; x0 = h / math.tan(SLOPE) + 0.8
        return {"k": "poly", "p": [self.P(x0, h), self.P(x0 + 9, h), self.P(x0 + 9, h + 2), self.P(x0 + 4.5, h + 2.9), self.P(x0, h + 2)], "fill": "#0d0b09", "c": "#9fd0ff", "w": 2, "id": "nfc"}, self.P(x0 + 4.5, h + 1)


# Giza plateau plan (metres east/north of Khufu's centre); positions from published site plans, rounded.
PLAN = {
    "khufu": (0, 0, 230.3), "khafre": (-330, -350, 215.3), "menkaure": (-560, -780, 104),
    "sphinx": (340, -470), "heit": (380, -1300), "wall": (170, -1080),
}
