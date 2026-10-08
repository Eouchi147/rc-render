"""Dark Corners, episode 1: A Hundred Thousand Good Nights (Bamberg, 1628). The whole film.
Timeline from the narration (voice D: vo/timing.json and vo/*.wav), shots with their cameras, transitions, title and end
cards, captions, and a frame renderer that any machine can run on any range of frames:
    python film_bamberg.py info                      the timeline
    python film_bamberg.py frames A B out.mp4        render frames [A, B) to an mp4 (workers: $FILM_WORKERS)
    python film_bamberg.py still T out.jpg           one frame at film time T (seconds)
"""
from darkroot import ROOT, ffmpeg_exe
import sys, os, json, math, subprocess
sys.path.insert(0, ROOT + '/film')
import numpy as np
import cv2
import soundfile as sf
import engine as E
import pages as PG
from script_bamberg import LINES

FPS, W, H = 24, 1080, 1920
VO = ROOT + '/film/vo/'
ORDER = [l[0] for l in LINES]
QUOTE = {l[0]: l[4] for l in LINES}
# pause before each line (seconds of silence after the previous line's last word): the film's breathing
GAP = dict(h1=1.3, h2=.35, h3=.4, h4=.9, q1=.5, q2=.6, w1=2.7, w2=.35, w3=.8, w4=.4, w5=.4, j1=.85, j2=.45, t1=.85,
           t2=.6, t3=.5, t4=.5, t5=.5, t6=1.35, p1=.95, p2=.4, l1=.8, l2=.4, l3=.5, l4=.85, l5=.4, l6=.35, l7=.5,
           e1=.9, e2=.5, e3=.6, c1=1.15, c2=.7, c3=.7)
END_CARD = 2.6


# ------------------------------------------------------------------ timeline
def _timeline():
    tm = json.load(open(VO + 'timing.json'))
    S, V = {}, {}
    t = 0.0
    for lid in ORDER:
        x, sr = sf.read(VO + lid + '.wav', dtype='float32')
        e = np.abs(x) > 0.01
        on, off = np.argmax(e) / sr, (len(x) - np.argmax(e[::-1])) / sr
        t += GAP[lid]
        S[lid] = t - on                       # where the wav starts
        V[lid] = (t, S[lid] + off)            # voiced span
        t = V[lid][1]
    total = t + 0.7 + END_CARD
    return S, V, tm, total


S, V, TM, TOTAL = _timeline()
NF = int(math.ceil(TOTAL * FPS))


def word_t(lid, k):
    """Film time of word k of line lid (start)."""
    return S[lid] + TM[lid]['words'][k][1]


def find_word(lid, w):
    for k, (wd, a, b) in enumerate(TM[lid]['words']):
        if wd.lower().strip('.,:;!?"“”') == w:
            return S[lid] + a, S[lid] + b
    raise KeyError(w)


# ------------------------------------------------------------------ the letter's pages, written in time with the voice
def pages_for_film():
    P = getattr(pages_for_film, '_P', None)
    if P is not None:
        return P
    P = {}
    q1, q2 = V['q1'], V['q2']
    P['p1'] = PG.build_page('p1_d', [(PG.LETTER_P1.split('. ')[0] + '.', q1[0] + 0.2, q1[1] - 0.1),
                                     ("Vnschuldig bin ich in das gefengnus kommen, vnschuldig bin ich gemarttert worden, vnschuldig muss ich sterben.",
                                      q2[0] + 0.1, q2[1] + 0.3)], seed=11)
    P['p1_full'] = PG.build_page('p1_full', [(PG.LETTER_P1, -1, -1)], seed=11, width=880)
    P['p1_margin'] = PG.margin_note('p1_margin', PG.MARGIN_P1)
    l2 = V['l2']
    P['p3'] = PG.build_page('p3_d', [(PG.LETTER_P3_PRE, -1, -1), (PG.LETTER_P3_TRUE, -1, -1),
                                     (PG.LETTER_P3_LIES, find_word('l2', 'follows')[0] - 0.1, l2[1] + 0.2)], seed=31)
    e1, e2, e3 = V['e1'], V['e2'], V['e3']
    P['p4'] = PG.build_page('p4_d', [(PG.LETTER_P4_PRE, -1, -1), (PG.LETTER_P4_HIDE, e1[0] + 0.1, e1[0] + 2.3),
                                     (PG.LETTER_P4_MARTYR, e2[0] + 0.2, e2[1]), (PG.LETTER_P4_NIGHT, e3[0] + 0.1, e3[1] + 0.4)], seed=41)
    P['record'] = PG.build_page('record', [(PG.RECORD, -1, -1)], style=PG.CLERK, seed=51, x0=96, y0=135, width=945)
    P['record2'] = PG.build_page('record2', [(PG.RECORD2, -1, -1)], style=PG.CLERK, seed=53, x0=96, y0=135, width=945)
    pages_for_film._P = P
    return P


PG.pages_for_film = pages_for_film


# ------------------------------------------------------------------ camera
def smooth_keys(t, ks):
    ts = [k[0] for k in ks]
    if t <= ts[0]:
        return np.array(ks[0][1], float)
    if t >= ts[-1]:
        return np.array(ks[-1][1], float)
    i = max(0, int(np.searchsorted(ts, t)) - 1)
    P = [np.array(ks[max(0, min(len(ks) - 1, j))][1], float) for j in (i - 1, i, i + 1, i + 2)]
    u = (t - ts[i]) / (ts[i + 1] - ts[i])
    u = u * u * (3 - 2 * u) * 0.35 + u * 0.65
    p0, p1, p2, p3 = P
    return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)


def cam_world(u, v, f, PWc=1620, PHc=2880, dens=1.5, ap=0.0, focus=1.0, t=0.0, hand=1.0, roll=0.0):
    """Camera looking at plate point (u, v) at zoom f, with a breath of hand-held drift."""
    jx = hand * (2.2 * E.noise1(t, 51, 0.31) + 0.8 * E.noise1(t, 52, 1.1))
    jy = hand * (2.2 * E.noise1(t, 53, 0.27) + 0.8 * E.noise1(t, 54, 0.9))
    rl = roll + hand * 0.12 * E.noise1(t, 55, 0.2)
    return E.Cam(x=(u - PWc / 2) / dens + jx, y=(v - PHc / 2) / dens + jy, f=f, ap=ap, focus=focus, roll=rl)


# ------------------------------------------------------------------ scenes
class Cell:
    """The cell (letter, candle, rain at the window): a wide plate and a macro plate of the desk, blended by zoom."""
    MACRO = dict(zoom=2.5, center=(700, 1800))

    def __init__(self, page, blot_t=None, quill_until=None, gutter=None, blots=()):
        import shot_cell as SC
        self.base = SC.CellShot('tall', 19.0, page, blot_t=blot_t, quill_until=quill_until, gutter=gutter)
        self.mac = SC.CellShot('tall', 19.0, page, blot_t=blot_t, quill_until=quill_until, gutter=gutter, **self.MACRO)
        self.blots = blots
        if blots:
            for s in (self.base, self.mac):
                s._extra_blots = blots
                s.ink_dyn_orig = s.ink_dyn
                s.desk.dyn = self._blot_dyn(s)

    def _blot_dyn(self, shot):
        """Several drops falling on the page (dark, like blood dried brown), each spreading as it lands."""
        import shade as SH
        cache = {}

        def dyn(t, rgb, a):
            rgb, a = shot.ink_dyn_orig(t, rgb, a)
            for k, (tb, (px, py)) in enumerate(self.blots):
                if t < tb:
                    continue
                if k not in cache:
                    n = SH.fbm(160, 160, 9, 3, 30 + k)
                    yy, xx = np.mgrid[0:160, 0:160].astype(np.float32)
                    cache[k] = (np.sqrt((xx - 80) ** 2 + ((yy - 80) * 1.1) ** 2), n)
                d, n = cache[k]
                rad = (3 + 10 * min(1.0, (t - tb) / 0.3) ** 0.5) * (0.8 + 0.4 * ((k * 37) % 5) / 5)
                m = np.clip((rad + (n - 0.5) * 8 - d) / 1.5, 0, 1)
                q = shot.Hp @ np.array([px, py, 1.0])
                x0, y0 = int(q[0] / q[2]) - 80, int(q[1] / q[2]) - 80
                sc = shot.zoom
                if sc != 1.0:
                    m = cv2.resize(m, None, fx=sc, fy=sc)
                    x0, y0 = int(q[0] / q[2] - 80 * sc), int(q[1] / q[2] - 80 * sc)
                h, w = m.shape
                ys, xs = slice(max(y0, 0), min(y0 + h, rgb.shape[0])), slice(max(x0, 0), min(x0 + w, rgb.shape[1]))
                mm = m[ys.start - y0:ys.stop - y0, xs.start - x0:xs.stop - x0]
                reg = rgb[ys, xs]
                reg[:] = reg * (1 - 0.9 * mm[..., None]) + np.array([0.09, 0.025, 0.02], np.float32) * mm[..., None] * 0.9
            return rgb, a
        return dyn

    def pen_plate(self, t):
        p, _, _ = PG.pen_at(self.base.page, t)
        q = self.base.Hp @ np.array([p[0], p[1], 1.0])
        return q[:2] / q[2]

    def page_plate(self, px, py):
        q = self.base.Hp @ np.array([px, py, 1.0])
        return q[:2] / q[2]

    def macro_mask(self, cam, t):
        M = E.layer_matrix(self.mac.desk, cam, t)[:2]
        one = np.ones((self.mac.z['desk'].shape[0] // 4, self.mac.z['desk'].shape[1] // 4), np.float32)
        one[:3] = 0; one[-3:] = 0; one[:, :3] = 0; one[:, -3:] = 0
        M4 = M.copy(); M4[:, :2] *= 4
        m = cv2.warpAffine(one, M4, (W, H), flags=cv2.INTER_LINEAR)
        m = cv2.GaussianBlur(m, (0, 0), 40)
        return np.clip((m - 0.5) * 2.2 + 0.5, 0, 1)

    def render(self, t, cam, frame):
        k = float(np.clip((cam.f - 1.75) / 0.6, 0, 1))
        if k <= 0.0:
            return self.base.render(t, cam, frame)[0]
        mm = self.macro_mask(cam, t)
        if k >= 1.0 and mm.min() > 0.999:
            return self.mac.render(t, cam, frame)[0]
        a = self.mac.render(t, cam, frame)[0]
        b = self.base.render(t, cam, frame)[0]
        m = mm * k
        return a * m[..., None] + b * (1 - m[..., None])


class Archive:
    def __init__(self, zoom=1.0, center=None):
        import shot_archive as SA
        self.s = SA.ArchiveShot(zoom, center)

    def render(self, t, cam, frame):
        return self.s.render(t, cam, frame)


class City:
    """Bamberg by night in rain (the approved look-test scene) in four depth layers; 'dawn' regrades it to the grey
    morning of the execution, without rain, with smoke beyond the wall."""
    ZS = dict(far=3.2, wall=1.8, house=1.25, figures=1.06)

    def __init__(self, variant='rain', zoom=1.0, center=(560, 1200)):
        import city as CY
        self.z = CY.prepare(zoom, center)
        self.variant, self.zoom = variant, zoom
        cx, cy = center[0] * 1.5, center[1] * 1.5
        anchor = (810.0, 1440.0) if zoom == 1.0 else (810.0 + zoom * (810.0 - cx), 1440.0 + zoom * (1440.0 - cy))
        self.layers = []
        for k in ('far', 'wall', 'house', 'figures'):
            if variant == 'dawn' and k == 'figures':
                continue
            self.layers.append(E.Layer(self.z[k], self.z.get(k + '_a'), Z=self.ZS[k], d=1.5 * zoom, anchor=anchor, name=k))
        self.house = [l for l in self.layers if l.name == 'house'][0]
        self.lights = self.z['lights']

    def render(self, t, cam, frame):
        img = E.compose(self.layers, cam, t)
        if self.variant == 'rain':
            g = np.zeros((H // 4, W // 4), np.float32)
            for i, (x, y, r, I) in enumerate(self.lights):
                sx, sy, sc = E.layer_point(self.house, cam, t, x, y)
                fl = 1 + 0.18 * E.noise1(t, 60 + i, 3.0) + 0.08 * E.noise1(t, 80 + i, 9.0)
                cv2.circle(g, (int(sx * 4), int(sy * 4)), max(1, int(r * sc * 0.5)), float(min(I, 1.5) * 0.3 * (fl - 0.8)), -1, cv2.LINE_AA, 4)
            g = cv2.GaussianBlur(cv2.resize(g, (W, H)), (0, 0), 30)
            img += g[..., None] * np.array([1.0, 0.6, 0.28], np.float32)
            E.rain(img, t, seed=7, n=650, angle=9, speed=2300, length=(30, 95), alpha=0.16, col=(0.62, 0.68, 0.82))
            E.rain(img, t, seed=8, n=120, angle=9, speed=3200, length=(110, 220), alpha=0.07, col=(0.7, 0.75, 0.9), depth=(0.9, 1.0))
        else:
            lum = img.mean(-1, keepdims=True)
            img = (lum * 0.7 + img * 0.3) * np.array([0.82, 0.88, 1.02], np.float32) * 1.25 + np.array([0.035, 0.04, 0.05], np.float32)
            yy = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
            wsh = np.clip(1 - yy / 0.36, 0, 1) ** 1.1 * 0.9          # a pale overcast morning sky hides the night's moon
            img = img * (1 - wsh) + np.array([0.5, 0.51, 0.55], np.float32) * wsh
            sm = E.smoke(t, 480, 270, seed=21, rise=24, scale=40, turb=1.4)
            col = np.exp(-((np.linspace(-1, 1, 270)[None, :] / 0.28) ** 2)) * np.linspace(0.2, 1, 480)[:, None] ** 0.6
            plume = cv2.resize((sm * col).astype(np.float32), (W, H))
            sx, sy, sc = E.layer_point(self.layers[0], cam, t, 1180, 1300)
            Mx = np.float32([[1, 0, sx - W / 2], [0, 1, sy - H * 0.95]])
            plume = cv2.warpAffine(plume, Mx, (W, H))
            img = img * (1 - 0.5 * plume[..., None]) + plume[..., None] * np.array([0.5, 0.5, 0.52], np.float32) * 0.5
        return img


class Shadow:
    def __init__(self, kind, events):
        import shadow as SHD
        self.s = SHD.ShadowShot(kind)
        self.s.events = events
        self.PW = self.s.PW

    def render(self, t, cam, frame):
        return self.s.render(t, cam, frame)


class Sheet:
    def __init__(self, kind):
        import sheet as SH
        self.s = SH.SheetShot(kind, V)

    def render(self, t, cam, frame):
        return self.s.render(t, cam, frame)


class Black:
    def render(self, t, cam, frame):
        return np.zeros((H, W, 3), np.float32)


# ------------------------------------------------------------------ the shot list
class Shot:
    def __init__(self, name, t0, t1, make, keys, xin=0.8, xout=0.8, grade=None, PWc=1620, ap=0.0, focus=1.0, hand=1.0,
                 shake=None, kin='x', kout='x'):
        self.name, self.t0, self.t1, self.make, self.keys = name, t0, t1, make, keys
        self.xin, self.xout, self.grade, self.PWc, self.ap, self.focus, self.hand = xin, xout, grade or {}, PWc, ap, focus, hand
        self.shake = shake
        self.kin, self.kout = kin, kout        # x = crossfade, b = through black
        self.obj = None

    def weight(self, t):
        if t < self.t0 or t > self.t1:
            return 0.0
        a = 1.0 if self.xin <= 0 else np.clip((t - self.t0) / self.xin, 0, 1)
        b = 1.0 if self.xout <= 0 else np.clip((self.t1 - t) / self.xout, 0, 1)
        w = min(a, b)
        return float(w * w * (3 - 2 * w))

    def cam(self, t):
        ks = self.keys(self) if callable(self.keys) else self.keys
        u, v, f = smooth_keys(t, ks)
        c = cam_world(u, v, f, PWc=self.PWc, ap=self.ap, focus=self.focus, t=t, hand=self.hand)
        if self.shake:
            for ts, amp in self.shake:
                if ts <= t < ts + 0.9:
                    d = math.exp(-(t - ts) * 6.0) * amp
                    c.x += d * math.sin((t - ts) * 71); c.y += d * math.cos((t - ts) * 53) * 1.4
        return c

    def render(self, t, frame):
        if self.obj is None:
            self.obj = self.make()
        return self.obj.render(t, self.cam(t), frame)


def build_shots():
    sh = []
    v = V
    # 1. COLD OPEN: the archive, the two records
    t0 = 0.0
    t1 = v['h4'][0] - 0.2
    sh.append(Shot('archive_open', t0, t1, lambda: Archive(),
                   [(0.0, (790, 1520, 1.12)), (v['h2'][0], (700, 1380, 1.22)), (v['h3'][0], (740, 1660, 1.3)),
                    (t1, (770, 1830, 1.42))], xin=1.4, xout=0.9, grade=dict(expo=1.0), ap=6, focus=1.0))
    # 2. THE CELL: he writes the first lines (the approved test shot, re-timed to the new voice)
    c0, c1 = t1 - 0.9, v['q2'][1] + 3.6
    def cell_open_keys(s):
        cell = s.obj or s.make()
        s.obj = cell
        b = cell.base
        pq = lambda tt: cell.pen_plate(tt)
        a0, m0, z0 = pq(v['q1'][0] + 0.9), pq((v['q1'][0] + v['q1'][1]) / 2), pq(v['q2'][0] + 0.3)
        fl = b.flame_plate
        return [(c0, (a0[0] + 170, a0[1] + 20, 4.1)), (v['h4'][0] + 0.8, (a0[0] + 160, a0[1] + 18, 3.95)),
                ((v['q1'][0] + v['q1'][1]) / 2, (m0[0] + 30, m0[1] + 22, 3.5)), (v['q2'][0] + 0.3, (z0[0] - 60, z0[1] + 60, 2.8)),
                (v['q2'][0] + 2.6, (980, 1620, 1.8)), (v['q2'][1] - 1.2, (920, 1470, 1.24)), (v['q2'][1] + 1.2, (1105, fl[1] + 110, 1.58)),
                (c1, (1110, fl[1] + 60, 1.9))]
    sh.append(Shot('cell_open', c0, c1, lambda: Cell('p1', blot_t=v['q1'][0] + 2.0), cell_open_keys, xin=0.9, xout=1.0,
                   ap=9.0, focus=1.0))
    # 3. THE CITY in rain: the house, then the witch house portal
    k0, k1 = c1 - 1.0, v['w2'][0] + 0.3
    sh.append(Shot('city_wide', k0, k1 + 0.9, lambda: City('rain'),
                   [(k0, (800, 1200, 1.12)), (v['w1'][0] + 2.0, (810, 1500, 1.25)), (k1 + 0.9, (850, 1760, 1.75))],
                   xin=1.0, xout=0.9, hand=0.6))
    k2 = v['w2'][1] + 0.6
    sh.append(Shot('city_portal', k1, k2, lambda: City('rain', 2.4, (560, 1200)),
                   [(k1, (845, 1745, 2.45)), (k2, (840, 1790, 2.75))], xin=0.9, xout=0.8, hand=0.5))
    # 4. THE CHAIN of names
    m0, m1 = k2 - 0.8, v['w5'][1] + 0.8
    def names_keys(s):
        sh_ = s.obj or s.make(); s.obj = sh_
        at = sh_.s.at
        gens = sh_.s.info['gens']
        root, wife, jun = at(gens[0][0]), at(sh_.s.info['wife']), at(sh_.s.info['junius'])
        return [(m0, (root[0], root[1] + 300, 1.75)), (v['w3'][0] + 2.5, (810, root[1] + 650, 1.28)),
                (v['w3'][1], (810, 1250, 1.12)), (v['w4'][0] + 0.6, (wife[0] + 120, wife[1] + 60, 1.9)),
                (v['w4'][1], (wife[0] + 60, wife[1] + 140, 1.75)), (v['w5'][0] + 0.4, (810, jun[1] - 330, 1.3)),
                (m1, (810, jun[1] - 250, 1.22))]
    sh.append(Shot('names', m0, m1, lambda: Sheet('names'), names_keys, xin=0.8, xout=0.8, hand=0.8))
    # 5. 28 JUNE: the witness (the second court record, close)
    import archive as A
    j0, j1 = m1 - 0.8, v['j2'][1] + 0.6
    rr = (972.9, 1240.5)
    sh.append(Shot('record_witness', j0, j1, lambda: Archive(2.2, rr),
                   [(j0, (rr[0] - 60, rr[1] - 240, 2.35)), (v['j2'][0], (rr[0] - 20, rr[1] - 60, 2.6)), (j1, (rr[0] - 10, rr[1] - 20, 2.8))],
                   xin=0.8, xout=0.6, kout='b', grade=dict(expo=0.95)))
    # 6. 30 JUNE: the torture room (shadows), the record against the letter, the fall
    r0, r1 = j1 - 0.1, v['t1'][1] + 0.5
    def ex_walk(t, ta, tb, xa, xb):
        u = np.clip((t - ta) / max(tb - ta, 1e-3), 0, 1)
        u = u * u * (3 - 2 * u)
        return xa + (xb - xa) * u, u
    def room_figs(t):
        X, u = ex_walk(t, r0 + 0.4, v['t1'][1] - 0.4, 930, 720)
        moving = 0.0 < u < 1.0
        return [('exec', X, 2900, 640, 380, (t * 5.2) if moving else 0.0, 0.0, 0.0)]
    rope_still = lambda t: (2950, 6 * math.sin(t * 0.8), 1.0)
    sh.append(Shot('room', r0, r1, lambda: Shadow('room', dict(figures=room_figs, rope=rope_still)),
                   [(r0, (760, 1350, 1.18)), (r1, (840, 1420, 1.3))], xin=0.6, xout=0.5, kin='b', hand=0.7))
    rl = (596.5, 1249.0)
    sh.append(Shot('record_screws', r1 - 0.5, v['t2'][1] + 0.5, lambda: Archive(2.2, rl),
                   [(r1 - 0.5, (rl[0] - 40, rl[1] + 120, 2.4)), (v['t2'][1] + 0.5, (rl[0] - 20, rl[1] + 200, 2.55))],
                   xin=0.5, xout=0.5, grade=dict(expo=0.95, sat=0.75)))
    # the letter, close: his account (drops fall on the page)
    tl0 = v['t2'][1]
    page4 = pages_for_film()['p4']
    def drops_for(tt):
        ws = find_word('t3', 'nails')[0]
        pts = [(380, 1290), (520, 1330), (640, 1270)]
        return [(ws + 0.05 + 0.35 * i, pts[i]) for i in range(1)]
    sh.append(Shot('letter_nails', tl0, v['t3'][1] + 0.5, lambda: Cell('p4', quill_until=-100, blots=drops_for(0)),
                   lambda s: [(tl0, tuple(s.obj_plate(560, 1150)) + (2.9,)), (v['t3'][1] + 0.5, tuple(s.obj_plate(500, 1290)) + (3.2,))],
                   xin=0.5, xout=0.5, ap=9.0))
    sh.append(Shot('record_legs', v['t3'][1], v['t4'][1] + 0.5, lambda: Archive(2.2, rl),
                   [(v['t3'][1], (rl[0] + 30, rl[1] + 260, 2.5)), (v['t4'][1] + 0.5, (rl[0] + 40, rl[1] + 330, 2.65))],
                   xin=0.5, xout=0.5, grade=dict(expo=0.92, sat=0.7)))
    # the hoist: the rope taut over the pulley, the drop at "fall", then darkness and the count in sound only
    tf = find_word('t5', 'fall')[0]
    h0, h1 = v['t4'][1], v['t6'][1] + 1.0
    def hoist_rope(t):
        if t < tf:
            u = np.clip((t - h0) / max(tf - h0, 1e-3), 0, 1)
            return (2950, 3 * math.sin(t * 2.0), 1.0 - 0.0 * u)
        d = t - tf
        return (2950 + 140 * math.exp(-d * 3) * math.sin(d * 9), 70 * math.exp(-d * 1.2) * math.sin(d * 6.5), 0.0)
    def hoist_figs(t):
        arm = np.clip((t - h0) / max(tf - h0, 1e-3), 0, 1) if t < tf else max(0.0, 1 - (t - tf) * 3)
        return [('exec', 760, 2900, 640, 380, 0.0, 0.25 * arm, arm)]
    sh.append(Shot('hoist', h0, h1, lambda: Shadow('room', dict(figures=hoist_figs, rope=hoist_rope)),
                   [(h0, (900, 1050, 1.35)), (tf, (900, 900, 1.45)), (tf + 0.4, (900, 1000, 1.4)), (h1, (880, 1150, 1.28))],
                   xin=0.5, xout=2.2, kout='b', shake=[(tf, 26.0)], hand=0.8, grade=dict(expo=1.05)))
    # 7. THE PLEA: the corridor, a lantern, two shadows
    p0, p1 = v['t6'][1] + 0.9, v['p2'][1] + 0.7
    stop = v['p2'][0] - 0.2
    def lx(t):
        u = np.clip((t - p0) / max(stop - p0, 1e-3), 0, 1)
        return 820 + 900 * (1 - (1 - u) ** 1.6)
    def corr_figs(t):
        x = lx(t)
        walking = t < stop
        ph = (t - p0) * 3.6 if walking else (stop - p0) * 3.6
        bow = float(np.clip((t - stop) / 1.2, 0, 1))
        return [('prisoner', x + 160, 2380, 470, 360, ph * 0.8, 0.0, 0.0), ('exec', x - 70, 2380, 500, 330, ph, bow, 0.0)]
    sh.append(Shot('corridor', p0, p1, lambda: Shadow('corridor', dict(lx=lx, figures=corr_figs)),
                   lambda s: [(p0, (lx(p0) + 330, 1500, 1.2)), (stop, (lx(stop) + 380, 1460, 1.26)), (p1, (lx(stop) + 360, 1420, 1.36))],
                   PWc=2700, xin=1.0, xout=0.8, kin='b', hand=0.7))
    # 8. THE LIE: the cell, page three, "nothing but lies"
    l0, l1e = p1 - 0.8, v['l3'][1] + 0.7
    def lie_keys(s):
        cell = s.obj or s.make(); s.obj = cell
        a = cell.pen_plate(find_word('l2', 'follows')[0] + 0.3)
        b = cell.pen_plate(v['l2'][1])
        fl = cell.base.flame_plate
        return [(l0, (960, 1500, 1.3)), (v['l1'][1], (a[0] + 80, a[1] - 40, 1.9)), (v['l2'][0] + 1.2, (a[0] + 40, a[1] + 10, 2.9)),
                (v['l2'][1], (b[0] - 40, b[1] + 30, 3.1)), (v['l3'][0] + 0.6, (1020, fl[1] + 300, 1.7)), (l1e, (1100, fl[1] + 120, 1.6))]
    sh.append(Shot('lie', l0, l1e, lambda: Cell('p3'), lie_keys, xin=0.8, xout=0.8, ap=9.0))
    # 9. STREET BY STREET: the town plan
    s0, s1 = l1e - 0.8, v['l7'][1] + 0.8
    def streets_keys(s):
        o = s.obj or s.make(); s.obj = o
        at = o.s.at
        mk = o.s.info['marks']
        a, b = at(mk[0]), at(mk[-1])
        nn1, nn2 = at((960, 300)), at((905, 1560))
        return [(s0, (810, 1440, 1.12)), (v['l5'][0], (810, 1400, 1.16)), (v['l6'][0] + 1.0, (a[0] + 40, a[1] + 80, 1.55)),
                (v['l6'][1], ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 1.3)), (v['l7'][0] + 1.2, (nn1[0] - 100, nn1[1] + 120, 1.8)),
                (s1, (nn2[0] - 120, nn2[1] - 60, 1.75))]
    sh.append(Shot('streets', s0, s1, lambda: Sheet('streets'), streets_keys, xin=0.8, xout=0.8, hand=0.8))
    # 10. THE LAST LINES: the cell, page four, the candle gutters and dies
    e0, e1 = s1 - 0.8, v['e3'][1] + 1.6
    def end_keys(s):
        cell = s.obj or s.make(); s.obj = cell
        a = cell.pen_plate(v['e1'][0] + 1.0)
        b = cell.pen_plate(v['e2'][0] + 0.8)
        c = cell.pen_plate(v['e3'][0] + 1.5)
        fl = cell.base.flame_plate
        return [(e0, (a[0] + 120, a[1] - 80, 2.1)), (v['e1'][0] + 1.0, (a[0] + 60, a[1], 2.9)), (v['e2'][0] + 0.8, (b[0], b[1] + 20, 3.0)),
                (v['e3'][0] + 1.5, (c[0] + 40, c[1] + 30, 2.4)), (v['e3'][1] - 0.6, (1000, 1500, 1.4)), (e1, (1080, fl[1] + 160, 1.3))]
    sh.append(Shot('last_lines', e0, e1, lambda: Cell('p4', gutter=(v['e3'][1] - 1.4, v['e3'][1] + 0.8)), end_keys,
                   xin=0.8, xout=1.2, kout='b', ap=9.0))
    # 11. CODA: the morning of the execution; the file; the printed page
    d0, d1 = e1 - 0.2, v['c1'][1] + 0.9
    sh.append(Shot('dawn', d0, d1, lambda: City('dawn'), [(d0, (820, 1520, 1.18)), (d1, (800, 1470, 1.24))],
                   xin=1.0, xout=0.8, kin='b', hand=0.5))
    a0, a1 = d1 - 0.8, v['c2'][1] + 0.8
    sh.append(Shot('archive_end', a0, a1, lambda: Archive(), [(a0, (770, 1850, 1.9)), (a1, (790, 1560, 1.12))],
                   xin=0.8, xout=0.8, ap=6))
    b0, b1 = a1 - 0.8, TOTAL
    sh.append(Shot('spee', b0, v['c3'][1] + 1.2, lambda: Sheet('spee'), [(b0, (810, 1200, 1.55)), (v['c3'][1] + 1.2, (810, 1480, 1.18))],
                   xin=0.8, xout=1.0, kout='b', hand=0.6))
    sh.append(Shot('endcard', v['c3'][1] + 0.4, TOTAL, lambda: Black(), [(0, (810, 1440, 1.0))], xin=0.6, xout=0.0, hand=0.0))
    return sh


SHOTS = None


def shots():
    global SHOTS
    if SHOTS is None:
        SHOTS = build_shots()
        for s in SHOTS:            # page-anchored cameras on the letter (macro on a page point)
            s.obj_plate = (lambda s_: (lambda px, py: (s_.obj or _mk(s_)).page_plate(px, py)))(s)
    return SHOTS


def _mk(s):
    s.obj = s.make()
    return s.obj


# ------------------------------------------------------------------ titles and captions
def _caps():
    out = []

    def split(ws):
        txt = ' '.join(w for w, _, _ in ws)
        if len(txt) <= 64:
            return [ws]
        cuts = [k for k, (w, _, _) in enumerate(ws[:-1]) if w.endswith(('.', '?', '!', ':'))]
        if not cuts:
            cuts = [k for k, (w, _, _) in enumerate(ws[:-1]) if w.endswith((',', ';'))]
        if not cuts:
            cuts = [len(ws) // 2 - 1]
        mid = len(txt) / 2
        pos = lambda k: len(' '.join(w for w, _, _ in ws[:k + 1]))
        k = min(cuts, key=lambda c: abs(pos(c) - mid))
        return split(ws[:k + 1]) + split(ws[k + 1:])
    for lid in ORDER:
        it = QUOTE[lid]
        for ch in split(TM[lid]['words']):
            a, b = S[lid] + ch[0][1] - 0.06, S[lid] + ch[-1][2] + 0.3
            lines, ln = [], ''
            for wd in ' '.join(w for w, _, _ in ch).split():
                if len(ln) + len(wd) + 1 > 30 and ln:
                    lines.append(ln); ln = wd
                else:
                    ln = (ln + ' ' + wd).strip()
            lines.append(ln)
            fn = 'Newsreader-Italic[opsz,wght].ttf' if it else 'Newsreader[opsz,wght].ttf'
            out.append([a, b, lines, fn])
    for i in range(len(out) - 1):
        out[i][1] = min(out[i][1], out[i + 1][0] - 0.02)
    return out


CAPS = None
_TXT = {}


def text(lines, fn, size, col=(0.97, 0.94, 0.87), spacing=1.2, tracking=0):
    k = (tuple(lines), fn, size, col, tracking)
    if k not in _TXT:
        _TXT[k] = E.text_image(list(lines), fn, size, col=col, spacing=spacing, tracking=tracking)
    return _TXT[k]


def overlays(img, t):
    global CAPS
    if CAPS is None:
        CAPS = _caps()
    for i, (a, b, lines, fn) in enumerate(CAPS):
        fi = 0.2 if i == 0 or a - CAPS[i - 1][1] > 0.3 else 0.0      # captions that follow on switch cleanly
        fo = 0.2 if i == len(CAPS) - 1 or CAPS[i + 1][0] - b > 0.3 else 0.0
        if a - fi <= t < b + fo:
            op = min(1.0, (t - (a - fi)) / fi if fi else 1.0, ((b + fo) - t) / fo if fo else 1.0)
            rgb, al = text(lines, fn, 54)
            E.put(img, rgb, al, W / 2, 1500, opacity=op, shadow=0.95)
    # title card, after his first lines
    ta = V['q2'][1] + 0.5
    if ta < t < ta + 3.4:
        u = t - ta
        op = min(1.0, u / 0.8, (3.4 - u) / 0.7)
        rgb, al = text(['DARK CORNERS'], 'Cinzel[wght].ttf', 34, col=(0.86, 0.72, 0.5), tracking=9)
        E.put(img, rgb, al, W / 2, 760, opacity=op * 0.9, glow=0.25)
        rgb, al = text(['A Hundred Thousand', 'Good Nights'], 'Newsreader-Italic[opsz,wght].ttf', 92, spacing=1.08)
        E.put(img, rgb, al, W / 2, 920, opacity=op, shadow=0.9, glow=0.18)
        rgb, al = text(['BAMBERG  ·  1628'], 'Cinzel[wght].ttf', 30, col=(0.8, 0.76, 0.68), tracking=6)
        E.put(img, rgb, al, W / 2, 1090, opacity=op * 0.85)
    # the inscription over the portal, translated
    ia, ib = V['w2'][0] + 0.2, V['w2'][1] + 0.5
    if ia < t < ib:
        op = min(1.0, (t - ia) / 0.5, (ib - t) / 0.4)
        rgb, al = text(['“Be warned: learn justice.”'], 'Newsreader-Italic[opsz,wght].ttf', 40, col=(0.9, 0.86, 0.78))
        E.put(img, rgb, al, W / 2, 330, opacity=op * 0.9, shadow=0.9)
        rgb, al = text(['the inscription over the door of the witch house'], 'Newsreader[opsz,wght].ttf', 26, col=(0.75, 0.72, 0.66))
        E.put(img, rgb, al, W / 2, 385, opacity=op * 0.8, shadow=0.9)
    # dates, small and top
    for lid, label in (('j1', 'WEDNESDAY, 28 JUNE 1628'), ('t1', 'FRIDAY, 30 JUNE 1628'), ('c1', 'AUGUST 1628'), ('c3', 'RINTELN, 1631')):
        a = V[lid][0] - 0.5
        if a < t < a + 3.6:
            op = min(1.0, (t - a) / 0.5, (a + 3.6 - t) / 0.6)
            rgb, al = text([label], 'Cinzel[wght].ttf', 30, col=(0.85, 0.78, 0.66), tracking=5)
            E.put(img, rgb, al, W / 2, 300, opacity=op * 0.9, shadow=0.9)
    # end card
    ea = V['c3'][1] + 0.9
    if t > ea:
        op = min(1.0, (t - ea) / 0.7)
        rgb, al = text(['DARK CORNERS'], 'Cinzel[wght].ttf', 44, col=(0.86, 0.72, 0.5), tracking=11)
        E.put(img, rgb, al, W / 2, 800, opacity=op, glow=0.3)
        rgb, al = text(['Johannes Junius', '1573 – 1628'], 'Newsreader-Italic[opsz,wght].ttf', 50, col=(0.92, 0.89, 0.82), spacing=1.25)
        E.put(img, rgb, al, W / 2, 960, opacity=op)
        rgb, al = text(['His letter of 24 July 1628 is kept in the', 'Staatsbibliothek Bamberg. Trial record after Burr (1896).',
                        'F. von Spee, Cautio Criminalis (1631).'], 'Newsreader[opsz,wght].ttf', 31, col=(0.7, 0.67, 0.62), spacing=1.35)
        E.put(img, rgb, al, W / 2, 1200, opacity=op * 0.9)
    return img


# ------------------------------------------------------------------ frame
def post(img, frame, t, grade):
    img = E.bloom(img, thr=0.78, strength=0.4)
    img = E.streak(img, thr=1.3, strength=0.05)
    img = E.aberration(img, 0.0012)
    img = E.vignette(img, 0.5)
    img = E.tonemap(img, 1.06 * grade.get('expo', 1.0), lift=(0.012, 0.008, 0.006), gamma=(1.04, 1.0, 0.97), sat=grade.get('sat', 1.0))
    img = E.grain(img, frame, 0.028)
    img = E.weave(img, frame, 0.35)
    return img


def render_frame(frame):
    t = frame / FPS
    act = [(s, s.weight(t)) for s in shots()]
    act = [(s, w) for s, w in act if w > 0.001]
    img = np.zeros((H, W, 3), np.float32)
    grade = {}
    if act:
        tot = sum(w for _, w in act)
        # crossfade between overlapping shots; a shot alone fades through black
        norm = max(tot, 1.0)
        for s, w in act:
            img += s.render(t, frame) * (w / norm)
        for k in ('expo', 'sat'):
            grade[k] = sum((w / norm) * s.grade.get(k, 1.0) for s, w in act) + (1 - sum(w / norm for _, w in act))
    img = post(img, frame, t, grade)
    img = overlays(img, t)
    if t < 0.6:
        img *= t / 0.6
    return np.clip(img, 0, 1)


def worker(args):
    wid, frames, path = args
    p = subprocess.Popen([ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    for fi in frames:
        img = render_frame(fi)
        p.stdin.write((img * 255 + 0.5).astype(np.uint8).tobytes())
        if fi % 24 == 0:
            print(wid, 'frame', fi, round(fi / FPS, 1), flush=True)
    p.stdin.close(); p.wait()
    return path


def frames_main(a, b, out):
    import multiprocessing as mp
    b = min(b, NF)
    n = int(os.environ.get('FILM_WORKERS', '2'))
    n = max(1, min(n, b - a))
    chunks = [(i, list(range(a + (b - a) * i // n, a + (b - a) * (i + 1) // n)), f'{out}.part{i}.mp4') for i in range(n)]
    ctx = mp.get_context('spawn')
    with ctx.Pool(n) as pl:
        parts = pl.map(worker, chunks)
    lst = out + '.txt'
    with open(lst, 'w') as f:
        for p_ in parts:
            f.write(f"file '{os.path.abspath(p_)}'\n")
    subprocess.run([ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out], check=True)
    for p_ in parts:
        os.remove(p_)
    os.remove(lst)


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'info'
    if what == 'info':
        for lid in ORDER:
            print(lid, round(V[lid][0], 2), round(V[lid][1], 2))
        print('total', round(TOTAL, 2), 'frames', NF)
        for s in build_shots():
            print(f'{s.name:16s} {s.t0:7.2f} {s.t1:7.2f}')
    elif what == 'still':
        t = float(sys.argv[2])
        img = render_frame(int(round(t * FPS)))
        cv2.imwrite(sys.argv[3], (img[..., ::-1] * 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 88])
    elif what == 'frames':
        frames_main(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
