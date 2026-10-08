"""The witch house, inside: a stone wall lit by fire, told in shadows only (no bodies on screen).
  room      the torture room: a torch on the wall, a beam with a pulley and a rope; the executioner's shadow crosses.
  corridor  the way back to the cell: a lantern carried along the wall; two shadows, one held up by the other.
The wall is a painted plate (photographic stone relit once, then the oil painter); fire light and shadows are
computed per frame from the stone's normals, so the painting is relit live as the flame moves."""
import math
import numpy as np
import cv2
import engine as E
import shade as S
import tex as TX
import plates as PL

DENS = 1.5
LZ = 520.0            # distance of the fire from the wall (plate px)


def _silhouette(kind, phase, bow=0.0, arm=0.0):
    """Polygons of a figure in figure units (feet at y=0, head near y=-1, x right), walking phase in radians."""
    polys = []
    sw = math.sin(phase)
    bob = 0.012 * abs(math.cos(phase))
    lean = 0.08 if kind == 'prisoner' else 0.02 + bow * 0.18
    def P(pts, dx=0.0, dy=0.0, piv=(0.0, -0.55), ang=0.0):
        a = math.radians(ang)
        c, s = math.cos(a), math.sin(a)
        q = []
        for x, y in pts:
            x, y = x - piv[0], y - piv[1]
            q.append((piv[0] + x * c - y * s + dx, piv[1] + x * s + y * c + dy - bob))
        return q
    tilt = -lean * 60
    if kind == 'exec':
        # hooded executioner: pointed hood, broad shoulders, apron, heavy boots
        body = [(-0.17, -0.5), (-0.2, -0.7), (-0.15, -0.8), (-0.09, -0.86), (-0.07, -0.95), (-0.02, -1.04), (0.03, -1.08),
                (0.05, -0.98), (0.09, -0.9), (0.15, -0.82), (0.2, -0.72), (0.19, -0.5), (0.15, -0.46), (-0.14, -0.46)]
        polys.append(P(body, ang=tilt))
        polys.append(P([(-0.14, -0.5), (0.15, -0.5), (0.13, -0.32), (-0.12, -0.32)], ang=tilt))
        armang = -20 - 50 * arm
        polys.append(P([(0.13, -0.8), (0.19, -0.79), (0.22, -0.55), (0.17, -0.53)], piv=(0.16, -0.79), ang=armang + tilt))
    else:
        # the prisoner: bare head bowed, thin, shirt, one arm held across the other's shoulder
        body = [(-0.13, -0.5), (-0.14, -0.72), (-0.1, -0.82), (-0.04, -0.85), (-0.04, -0.89), (0.0, -0.96), (0.06, -0.97),
                (0.1, -0.92), (0.09, -0.86), (0.05, -0.84), (0.11, -0.8), (0.14, -0.7), (0.13, -0.5)]
        polys.append(P(body, ang=tilt))
        polys.append(P([(-0.11, -0.52), (0.12, -0.52), (0.1, -0.4), (-0.1, -0.4)], ang=tilt))
        polys.append(P([(-0.12, -0.78), (-0.07, -0.79), (-0.28, -0.74), (-0.3, -0.7)], piv=(-0.1, -0.78), ang=10 + tilt))
    # legs: two quads swinging about the hip
    for k, sgn in ((0, 1), (1, -1)):
        ang = sgn * sw * (24 if kind == 'exec' else 14)
        w0, w1 = (0.075, 0.06) if kind == 'exec' else (0.055, 0.045)
        leg = [(-w0, -0.42), (w0, -0.42), (w1, -0.03), (w1 + 0.06, 0.0), (-w1, 0.0)]
        polys.append(P(leg, piv=(0.0, -0.42), ang=ang))
    return polys


def _project_polys(polys, X, Y, Hf, df, L, sc):
    """Figure polygons (figure units) at world (X feet, Y feet) with height Hf px, distance df from the wall, to the
    shadow on the wall cast by point light L = (x, y, z). Returns polygons at plate px * sc."""
    lx, ly, lz = L
    k = lz / max(lz - df, 1.0)
    out = []
    for poly in polys:
        q = []
        for x, y in poly:
            px, py = X + x * Hf, Y + y * Hf
            q.append(((lx + (px - lx) * k) * sc, (ly + (py - ly) * k) * sc))
        out.append(np.array(q, np.float32))
    return out, k


class ShadowShot:
    def __init__(self, kind='room', seed=3):
        self.kind = kind
        self.PW, self.PH = (1620, 2880) if kind == 'room' else (2700, 2880)
        z = PL.load('shadow_' + kind)
        if z is None:
            z = self._prepare()
        self.alb = z['alb'].astype(np.float32)
        self.nrm = z['nrm'].astype(np.float32)
        self.layer = E.Layer(self.alb, None, Z=1.0, d=DENS, anchor=(self.PW / 2.0, self.PH / 2.0), name='wall')
        self.layer.dyn = self._light
        self.events = dict()
        self.seed = seed

    # ------------------------------------------------------------- the plate
    def _prepare(self):
        PW, PH = self.PW, self.PH
        alb, N, hgt = TX.surface('medieval_blocks_03', PH, PW, scale=0.8, tint=(0.92, 0.86, 0.78), sat=0.8)
        if N is None:
            N = np.dstack([np.zeros((PH, PW)), np.zeros((PH, PW)), np.ones((PH, PW))]).astype(np.float32)
        N = TX.flatten_normals(N, 0.9)
        yy, xx = np.mgrid[0:PH, 0:PW].astype(np.float32)
        # damp and soot: darker low on the wall and above the fire
        dirt = S.fbm(PH, PW, 160, 5, 7)
        alb = alb * (0.75 + 0.35 * dirt)[..., None]
        alb *= (1 - 0.35 * np.clip((yy - PH * 0.7) / (PH * 0.3), 0, 1))[..., None]
        if self.kind == 'room':
            pass
            # the beam across the top and the iron pulley
            b0, b1 = 230, 380
            wood, wn, _ = TX.surface('old_planks_02', PH, PW, scale=0.8, tint=(0.55, 0.42, 0.3), rot=math.pi / 2)
            beam = ((yy > b0) & (yy < b1)).astype(np.float32)
            beam = cv2.GaussianBlur(beam, (0, 0), 1.2)
            alb = alb * (1 - beam[..., None]) + wood * 0.55 * beam[..., None]
            if wn is not None:
                N = N * (1 - beam[..., None]) + wn * beam[..., None]
            # its shadow on the wall below
            alb *= (1 - 0.5 * np.exp(-np.clip(yy - b1, 0, None) / 40) * (yy > b1))[..., None]
            px, py = 900, 470
            d = np.sqrt((xx - px) ** 2 + (yy - py) ** 2)
            wheel = np.clip(1 - np.abs(d - 62) / 9, 0, 1) + np.clip(1 - d / 16, 0, 1)
            spokes = np.zeros_like(d)
            for a in range(6):
                ang = a * math.pi / 3
                dist = np.abs((xx - px) * math.sin(ang) - (yy - py) * math.cos(ang))
                spokes = np.maximum(spokes, np.clip(1 - dist / 4, 0, 1) * (d < 62))
            strap = ((np.abs(xx - px) < 7) & (yy > b1 - 10) & (yy < py)).astype(np.float32)
            iron = np.clip(wheel + spokes + strap, 0, 1)
            alb = alb * (1 - iron[..., None]) + np.array([0.05, 0.045, 0.04], np.float32) * iron[..., None]
        # paint under a soft, even raking light so the strokes follow the stone
        lit, _ = S.light(N[::2, ::2], [S.PLight(PW * 0.3 / 2, PH * 0.4 / 2, 400, (1.0, 0.9, 0.8), I=1.6, r=2000)],
                         amb=(0.35, 0.33, 0.32))
        lit = cv2.resize(lit, (PW, PH))
        rgb = alb * lit
        pr, _ = PL.paint_layer(rgb, None, 1.5, seed=61 if self.kind == 'room' else 62, grade='warm', expo=1.6)
        # store the painting divided back by that light, so the live fire light can relight it
        albp = pr / np.maximum(cv2.GaussianBlur(lit, (0, 0), 3) * 1.0, 0.25)
        PL.save('shadow_' + self.kind, alb=albp.astype(np.float32), nrm=N.astype(np.float32))
        return PL.load('shadow_' + self.kind)

    # ------------------------------------------------------------- the fire and the figures (set by the film)
    def fire(self, t):
        """(x, y, z) of the light in plate px, its intensity and whether it is a torch."""
        fl = 1 + 0.09 * E.noise1(t, self.seed, 2.3) + 0.05 * E.noise1(t, self.seed + 1, 8.1)
        if self.kind == 'room':          # a brazier on the floor, off frame: fire light from below
            return (640.0 + 10 * E.noise1(t, 4, 0.7), 2760.0, LZ), 3.3 * fl
        x = self.lantern_x(t)
        sw = 8 * math.sin(t * 2.4)
        return (x + sw, 2150.0 + 6 * math.sin(t * 4.8), LZ), 2.6 * fl

    def lantern_x(self, t):
        return float(self.events.get('lx', lambda t: self.PW / 2)(t))

    def figures(self, t):
        """[(kind, X feet, Y feet, height px, distance from wall, phase, bow, arm)]"""
        f = self.events.get('figures')
        return f(t) if f else []

    def rope(self, t):
        """Rope from the pulley down: (end y, sway px, taut 0..1) or None."""
        f = self.events.get('rope')
        return f(t) if f else None

    def _light(self, t, rgb, a):
        PW, PH = self.PW, self.PH
        q = 4
        h, w = PH // q, PW // q
        (lx, ly, lz), I = self.fire(t)
        n = self.nrm[::q, ::q]
        L = S.PLight(lx / q, ly / q, lz / q, (1.0, 0.6, 0.3), I=I, r=(1150 if self.kind == 'room' else 800) / q)
        lit, _ = S.light(n, [L], amb=(0.0, 0.0, 0.0), wrap=0.2)
        # shadows
        sh = np.zeros((h, w), np.float32)
        for kind, X, Y, Hf, df, ph, bow, arm in self.figures(t):
            polys, k = _project_polys(_silhouette(kind, ph, bow, arm), X, Y, Hf, df, (lx, ly, lz), 1.0 / q)
            m = np.zeros((h, w), np.float32)
            cv2.fillPoly(m, [np.round(p * 8).astype(np.int32) for p in polys], 1.0, cv2.LINE_AA, 3)
            soft = 1.0 + df / lz * 10
            sh = np.maximum(sh, cv2.GaussianBlur(m, (0, 0), soft) * 0.92)
        rp = self.rope(t)
        rope_pts = None
        if rp is not None:
            yend, sway, taut = rp
            px, py = 900.0, 470.0
            ys = np.linspace(py + 62, yend, 40)
            u = (ys - ys[0]) / max(yend - ys[0], 1)
            xs = px + 62 + sway * np.sin(u * math.pi * (0.5 + 0.5 * (1 - taut))) * u
            rope_pts = np.stack([xs, ys], 1)
            dr = 90.0
            kk = lz / (lz - dr)
            spx = lx + (rope_pts[:, 0] - lx) * kk
            spy = ly + (rope_pts[:, 1] - ly) * kk
            m = np.zeros((h, w), np.float32)
            cv2.polylines(m, [np.round(np.stack([spx, spy], 1) / q * 8).astype(np.int32)], False, 1.0, max(1, int(14 / q)), cv2.LINE_AA, 3)
            sh = np.maximum(sh, cv2.GaussianBlur(m, (0, 0), 2.5) * 0.85)
        lit = lit * (1 - sh)[..., None]
        lit = cv2.resize(lit, (PW, PH), interpolation=cv2.INTER_LINEAR)
        amb = np.array([0.05, 0.055, 0.075], np.float32)
        out = rgb * (lit + amb)
        if rope_pts is not None:
            m = np.zeros((PH, PW), np.float32)
            cv2.polylines(m, [np.round(rope_pts * 8).astype(np.int32)], False, 1.0, 11, cv2.LINE_AA, 3)
            m = cv2.GaussianBlur(m, (0, 0), 0.8)
            edge = np.zeros((PH, PW), np.float32)
            cv2.polylines(edge, [np.round((rope_pts - [3, 0]) * 8).astype(np.int32)], False, 1.0, 4, cv2.LINE_AA, 3)
            col = np.array([0.05, 0.035, 0.025], np.float32)
            out = out * (1 - m[..., None]) + col * m[..., None] + (edge * m)[..., None] * np.array([0.3, 0.15, 0.06], np.float32) * 0.25
        return out, a

    # ------------------------------------------------------------- frame
    def render(self, t, cam, frame):
        img = E.compose([self.layer], cam, t)
        (lx, ly, lz), I = self.fire(t)
        fx, fy, sc = E.layer_point(self.layer, cam, t, lx, ly)
        if self.kind == 'room':
            # the brazier's glow rising into the bottom of the frame, and sparks
            yy = np.linspace(0, 1, E.H, dtype=np.float32)[:, None]
            img += (np.clip((yy - 0.72) / 0.28, 0, 1) ** 2 * 0.18 * I / 3.4)[..., None] * np.array([1.0, 0.45, 0.15], np.float32)
            if not hasattr(self, 'sparks'):
                self.sparks = E.Particles(90, ((-300, 300), (-200, 900), (0.9, 1.1)), seed=12, vel=(6, -160, 0), jitter=30,
                                          size=(1.0, 2.4), col=(1.0, 0.55, 0.2), bright=1.6)
            self.sparks.draw(img, cam, t, light=None, gain=1.0)
        else:
            # the lantern: a small glass box with a flame; held low, swinging gently
            g = np.zeros((E.H, E.W), np.float32)
            cv2.circle(g, (int(fx), int(fy)), int(40 * sc), 1.0, -1, cv2.LINE_AA)
            g = cv2.GaussianBlur(g, (0, 0), 22 * sc)
            img += g[..., None] * np.array([1.0, 0.62, 0.3], np.float32) * 0.5 * I
            E.add_flame(img, fx, fy + 16 * sc, sc * 1.1, t, seed=self.seed + 3, glow=1.0, size=0.8)
        return img
