"""The cell shots: the letter written by candlelight (cold open, the lie, the last lines)."""
import math
import numpy as np
import cv2
import engine as E
import cell as C
import plates as PL
import quill as Q
import pages as PG
import hand

INK = np.array([0.075, 0.055, 0.05], np.float32)


def prepare(variant, height, zoom=1.0, center=None, force=False):
    name = f'cell_{variant}' + ('' if zoom == 1.0 else f'_z{zoom:g}_{int(center[0])}_{int(center[1])}')
    z = None if force else PL.load(name)
    if z is not None:
        return z
    L = C.build(height=height, zoom=zoom, center=center)
    sc = 1.5 * zoom / (1.0 if zoom == 1.0 else 1.7)      # a detail plate's strokes match the wide plate's at f = 1.7
    if zoom != 1.0:                                       # the wall plate of a detail view covers more (parallax margin)
        Lw = C.build(height=height, zoom=zoom / 1.4, center=center)
        wall, _ = PL.paint_layer(Lw['wall'], None, sc / 1.4, seed=11, grade='warm')
        window = Lw['window']
    else:
        wall, _ = PL.paint_layer(L['wall'], None, sc, seed=11, grade='warm')
        window = L['window']
    desk, da = PL.paint_layer(L['desk'], L['desk_a'], sc, seed=12, grade='warm')
    cand, ca = PL.paint_layer(L['candle'], L['candle_a'], sc, seed=13, detail=1.4, grade='warm')
    PL.save(name, wall=wall, desk=desk, desk_a=da, candle=cand, candle_a=ca, window=window.astype(np.float32),
            paper_H=L['paper_H'], paper_a=L['paper_a'])
    return PL.load(name)


def quill_painted():
    z = PL.load('quill')
    if z is None:
        qr, qa, nib = Q.build()
        pr, pa = PL.paint_layer(qr * np.array([0.8, 0.68, 0.52], np.float32), qa, 1.0, seed=17, display=True, detail=1.5, grade='warm')
        PL.save('quill', rgb=pr, a=pa, nib=np.array(nib))
        z = PL.load('quill')
    return z['rgb'], z['a'], tuple(z['nib'])


def flicker(t, seed=2):
    return 1 + 0.07 * E.noise1(t, seed, 2.1) + 0.04 * E.noise1(t, seed + 1, 7.3)


class CellShot:
    def __init__(self, variant='tall', height=19.0, page='p1', blot_t=None, quill_until=None, extra_pages=(), gutter=None,
                 snuff_t=None, zoom=1.0, center=None):
        self.z = prepare(variant, height, zoom, center)
        self.zoom = zoom
        cam3 = C.BASE_CAM if zoom == 1.0 else C.BASE_CAM.zoomed(zoom, center)
        self.height = height
        self.P = PG.pages_for_film()
        self.page = self.P[page]
        self.extra = [self.P[k] for k in extra_pages]
        self.Hp = self.z['paper_H'].astype(np.float64)
        self.blot_t = blot_t
        self.quill_until = quill_until
        self.gutter = gutter            # (t0, t1): the flame gutters and dies
        self.snuff_t = snuff_t
        fp, _ = cam3.project([C.flame_pos(height=height) - np.array([0, 0, 3.2])])
        self.flame_plate = fp[0]
        yy, xx = np.mgrid[0:C.PH, 0:C.PW].astype(np.float32)
        d2 = ((xx - fp[0][0]) ** 2 + (yy - fp[0][1]) ** 2)
        self.fmask = np.exp(-d2 / (2 * (520.0 * zoom) ** 2)).astype(np.float32)
        qr, qa, nib = quill_painted()
        self.q_rgb, self.q_a, self.q_nib = qr, qa, nib
        if zoom == 1.0:
            anchor = (C.PW / 2.0, C.PH / 2.0)
        else:
            anchor = (C.PW / 2.0 + zoom * (C.PW / 2.0 - center[0]), C.PH / 2.0 + zoom * (C.PH / 2.0 - center[1]))
        dens = C.DENS * zoom
        if zoom != 1.0:
            zw = zoom / 1.4
            aw = (C.PW / 2.0 + zw * (C.PW / 2.0 - center[0]), C.PH / 2.0 + zw * (C.PH / 2.0 - center[1]))
            self.wall = E.Layer(self.z['wall'], None, Z=1.3, d=C.DENS * zw, anchor=aw, name='wall')
        else:
            self.wall = E.Layer(self.z['wall'], None, Z=1.3, d=dens, anchor=anchor, name='wall')
        self.desk = E.Layer(self.z['desk'], self.z['desk_a'], Z=1.0, d=dens, anchor=anchor, name='desk')
        self.candle = E.Layer(self.z['candle'], self.z['candle_a'], Z=0.995, d=dens, anchor=anchor, name='candle')
        self.candle.zf = 1.2
        self.quill = E.Layer(qr, qa, Z=0.985, d=dens, anchor=anchor, name='quill')
        lit = lambda t: self.light(t)
        self.wall.lights = [(self.fmask, lit, None)]
        self.desk.lights = [(self.fmask, lit, None)]
        self.candle.lights = [(self.fmask, lit, None)]
        self.desk.dyn = self.ink_dyn
        self.quill.motion = self.quill_motion
        self.quill.visible = lambda t: 1.0 if (self.quill_until is None or t < self.quill_until) else max(0.0, 1 - (t - self.quill_until) / 0.6)
        self.layers = [self.wall, self.desk, self.candle, self.quill]
        r = np.random.default_rng(5)
        self.blot_shape = None

    # -------------------------------------------------------------- light
    def alive(self, t):
        if self.gutter is None:
            return 1.0
        t0, t1 = self.gutter
        return float(np.clip(1 - (t - t0) / max(t1 - t0, 1e-3), 0, 1))

    def light(self, t):
        a = self.alive(t)
        g = flicker(t) * (0.35 + 0.65 * a) if a > 0 else 0.25
        if self.gutter is not None and t > self.gutter[0]:
            g *= 1 - 0.3 * abs(E.noise1(t, 9, 6.0))
        return g

    # -------------------------------------------------------------- ink and quill
    def pen(self, t):
        p, down, lift = PG.pen_at(self.page, t)
        q = self.Hp @ np.array([p[0], p[1], 1.0])
        return np.array([q[0] / q[2], q[1] / q[2]]), down, lift

    def ink_dyn(self, t, rgb, a):
        maps = [self.page] + self.extra
        cov = np.zeros((PG.PHEI, PG.PWID), np.float32)
        wet = np.zeros_like(cov)
        for m in maps:
            s, w = hand.at_time(m['cov'], m['dark'], m['tmap'], t)
            cov = np.maximum(cov, s); wet = np.maximum(wet, w)
        if self.blot_t is not None and t > self.blot_t:
            cov = np.maximum(cov, self.blot(t))
        # warp only the paper's bounding box
        Hp = self.Hp
        cs = np.array([[0, 0, 1], [PG.PWID, 0, 1], [PG.PWID, PG.PHEI, 1], [0, PG.PHEI, 1]], np.float64)
        q = (Hp @ cs.T).T
        q = q[:, :2] / q[:, 2:]
        x0, y0 = np.floor(q.min(0)).astype(int) - 2
        x1, y1 = np.ceil(q.max(0)).astype(int) + 2
        x0, y0 = max(x0, 0), max(y0, 0)
        x1, y1 = min(x1, rgb.shape[1]), min(y1, rgb.shape[0])
        T = np.array([[1, 0, -x0], [0, 1, -y0], [0, 0, 1]], np.float64) @ Hp
        cw = cv2.warpPerspective(cov, T, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR)
        ww = cv2.warpPerspective(wet, T, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR)
        reg = rgb[y0:y1, x0:x1]
        lum = reg.mean(-1, keepdims=True)
        ink = INK * (0.6 + 0.8 * lum)
        reg[:] = reg * (1 - cw[..., None] * 0.92) + ink * cw[..., None] * 0.92
        reg += (ww * 0.5)[..., None] * np.array([0.35, 0.3, 0.32], np.float32) * lum       # wet ink catches the light
        # the quill's shadow on the paper
        if self.quill.visible(t) > 0.01:
            pp, down, lift = self.pen(t)
            d = np.array([math.cos(0.72 + 0.35), math.sin(0.72 + 0.35)])
            z = self.zoom
            p0 = pp + np.array([-6, 8]) * (0.3 + lift) * z
            p1 = pp + (d * 520 + np.array([-90, 60])) * z
            sh = np.zeros(reg.shape[:2], np.float32)
            cv2.line(sh, (int((p0[0] - x0) * 16), int((p0[1] - y0) * 16)), (int((p1[0] - x0) * 16), int((p1[1] - y0) * 16)),
                     1.0, max(1, int(5 * z)), cv2.LINE_AA, 4)
            sh = cv2.GaussianBlur(sh, (0, 0), 6 * z) * self.quill.visible(t)
            reg *= (1 - 0.28 * sh)[..., None]
        return rgb, a

    def blot(self, t):
        if self.blot_shape is None:
            p, _, _ = PG.pen_at(self.page, self.blot_t)
            yy, xx = np.mgrid[0:PG.PHEI, 0:PG.PWID].astype(np.float32)
            import shade as S
            n = S.fbm(PG.PHEI, PG.PWID, 9, 3, 21)
            d = np.sqrt((xx - p[0] - 6) ** 2 + ((yy - p[1] - 10) * 1.1) ** 2)
            self.blot_shape = (d, n)
        d, n = self.blot_shape
        rad = 4 + 13 * min(1.0, (t - self.blot_t) / 0.35) ** 0.5
        return np.clip((rad + (n - 0.5) * 9 - d) / 1.5, 0, 1)

    def quill_motion(self, t):
        pp, down, lift = self.pen(t)
        trem = 1.0 + (0.6 if t < 16 else 0.3)
        jx = trem * (E.noise1(t, 31, 9.0) * 1.2 + E.noise1(t, 32, 23.0) * 0.6)
        jy = trem * (E.noise1(t, 33, 8.0) * 1.2 + E.noise1(t, 34, 21.0) * 0.6)
        rot = 1.6 * E.noise1(t, 35, 1.3) + 0.8 * E.noise1(t, 36, 7.0)
        lift_px = -14 * lift - (0 if down else 4)
        nx, ny = self.q_nib
        z = self.zoom
        return (pp[0] - nx + jx * z, pp[1] - ny + (jy + lift_px) * z, rot, z, nx, ny)

    # -------------------------------------------------------------- frame
    def render(self, t, cam, frame, rain=True, dust=True):
        self.candle.zf = 1.2
        img = compose_zf(self.layers, cam, t)
        # rain beyond the window
        if rain:
            M = E.layer_matrix(self.wall, cam, t)[:2]
            win = cv2.warpAffine(self.z['window'], M, (E.W, E.H), flags=cv2.INTER_LINEAR)
            if win.max() > 0.01:
                E.rain(img, t, mask=win, seed=3, n=500, angle=10, speed=1500, length=(18, 46), alpha=0.35, col=(0.55, 0.62, 0.8))
        # the flame
        a = self.alive(t)
        fx, fy, sc = E.layer_point(self.candle, cam, t, *self.flame_plate)
        if a > 0:
            gut = 0.0 if self.gutter is None else float(np.clip((t - self.gutter[0]) / max(self.gutter[1] - self.gutter[0], 1e-3), 0, 1))
            E.add_flame(img, fx, fy, sc * 0.95, t, seed=2, gutter=gut, glow=1.1 * (0.4 + 0.6 * a), size=0.55 + 0.45 * a)
        # dust in the candle light
        if dust:
            if not hasattr(self, 'dust'):
                self.dust = E.Particles(260, ((-500, 500), (-700, 300), (1.02, 1.28)), seed=8, vel=(4, -6, 0), jitter=10,
                                        size=(1.2, 3.2), col=(1.0, 0.8, 0.55), bright=0.5)
            yy, xx = np.mgrid[0:E.H:4, 0:E.W:4].astype(np.float32)
            g = np.exp(-(((xx - fx) ** 2 + (yy - fy) ** 2) / (2 * (360 * sc) ** 2)))
            g = cv2.resize(g, (E.W, E.H)) * (0.3 + 0.7 * a)
            self.dust.draw(img, cam, t, light=g, gain=0.9)
        return img, (fx, fy, sc)


def compose_zf(layers, cam, t):
    """Like engine.compose, but each layer may blur at its own focus depth (zf) while keeping its draw order (Z)."""
    out = np.zeros((E.H, E.W, 3), np.float32)
    for L in sorted(layers, key=lambda l: -l.Z):
        op = 1.0 if L.visible is None else float(L.visible(t))
        if op <= 0.001:
            continue
        rgb, a = L.frame(t)
        M = E.layer_matrix(L, cam, t)[:2]
        src = rgb if a is None else np.dstack([rgb * a[..., None], a])
        wr = cv2.warpAffine(src, M, (E.W, E.H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        zf = getattr(L, 'zf', L.Z)
        coc = min(abs(cam.ap * (1.0 / max(cam.focus, 1e-3) - 1.0 / zf) * cam.f), 40.0) if cam.ap else 0.0
        if coc > 0.6:
            wr = E.blur_fast(wr, coc * 0.5)
        if a is None:
            out = wr.copy() if op >= 1 else out * (1 - op) + wr * op
        else:
            aa = wr[..., 3:] * op
            out = out * (1 - aa) + wr[..., :3] * op
    return out
