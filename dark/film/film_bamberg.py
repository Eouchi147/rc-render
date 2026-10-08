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
from direct_bamberg2 import LINES

FPS, W, H = 24, 1080, 1920
VO = os.environ.get('VO_DIR', ROOT + '/film/vo').rstrip('/') + '/'
ORDER = [l[0] for l in LINES]
QUOTE = {l[0]: l[4] for l in LINES}
# pause before each line (seconds of silence after the previous line's last word): the film's breathing
GAP = dict(o1=0.6, o2=0.5, o3=0.5, x1=3.0, x2=0.5, x3=0.7, x4=0.6, x5=0.5, a1=0.9, a2=0.5, a3=0.4, t1=0.9, t2=0.6,
           t3=0.6, t4=0.5, k1=2.8, k2=0.4, k3=0.3, l1=1.0, l2=0.6, l3=0.4, l4=0.5, e1=1.0, e2=0.5, e3=0.5, e4=0.5,
           f1=1.8, f2=0.8, f3=0.5)
END_CARD = 2.6
LIMIT = 179.4


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
    if total > LIMIT and not getattr(_timeline, 'fitted', False):
        # keep the film under three minutes: shorten every pause by the same factor (never below 60%)
        over = total - LIMIT
        k = max(0.6, 1 - over / sum(GAP.values()))
        for lid in GAP:
            GAP[lid] *= k
        _timeline.fitted = True
        return _timeline()
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
    o2, o3 = V['o2'], V['o3']
    P['p1'] = PG.build_page('p1_v3', [(PG.LETTER_P1.split('. ')[0] + '.', o2[0] - 0.4, o3[1] + 0.2),
                                      ("Vnschuldig bin ich in das gefengnus kommen, vnschuldig bin ich gemarttert worden, vnschuldig muss ich sterben.",
                                       o3[1] + 0.6, o3[1] + 6.0)], seed=11)
    P['p1_full'] = PG.build_page('p1_full', [(PG.LETTER_P1, -1, -1)], seed=11, width=880)
    P['p1_margin'] = PG.margin_note('p1_margin', PG.MARGIN_P1)
    l1 = V['l1']
    P['p3'] = PG.build_page('p3_v3', [(PG.LETTER_P3_PRE, -1, -1), (PG.LETTER_P3_TRUE, -1, -1),
                                      (PG.LETTER_P3_LIES, find_word('l1', 'lied')[0] - 0.2, l1[1] - 0.3)], seed=31)
    e1, e2, e3, e4 = V['e1'], V['e2'], V['e3'], V['e4']
    P['p4'] = PG.build_page('p4_v3', [(PG.LETTER_P4_PRE, -1, -1), (PG.LETTER_P4_HIDE, e2[0] - 0.1, e2[1] + 0.2),
                                      (PG.LETTER_P4_MARTYR, e3[0] + 0.1, e3[1] + 0.4), (PG.LETTER_P4_NIGHT, e4[0] + 0.1, e4[1] - 0.6)], seed=41)
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
        T = dict(V)                      # the sheet's ink follows these lines of the plain telling
        T['w3'], T['w4'], T['w5'] = V['x3'], V['x4'], V['x5']
        mid = (V['l3'][0] + V['l3'][1]) / 2
        T['l5'], T['l6'], T['l7'] = (V['l3'][0], mid), (mid, V['l3'][1]), V['l4']
        self.s = SH.SheetShot(kind, T)

    def render(self, t, cam, frame):
        return self.s.render(t, cam, frame)


class Cabinet:
    def __init__(self):
        import cabinet as CB
        self.s = CB.CabinetShot()

    def render(self, t, cam, frame):
        return self.s.render(t, cam, frame)


class Black:
    def render(self, t, cam, frame):
        return np.zeros((H, W, 3), np.float32)


# ------------------------------------------------------------------ the shot list
class Shot:
    def __init__(self, name, t0, t1, make, keys, xin=0.8, xout=0.8, grade=None, PWc=1620, ap=0.0, focus=1.0, hand=1.0,
                 shake=None, kin='x', kout='x', roll=0.0, key=None):
        self.name, self.t0, self.t1, self.make, self.keys = name, t0, t1, make, keys
        self.roll, self.key = roll, key or name
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
        c = cam_world(u, v, f, PWc=self.PWc, ap=self.ap, focus=self.focus, t=t, hand=self.hand, roll=self.roll)
        if self.shake:
            for ts, amp in self.shake:
                if ts <= t < ts + 0.9:
                    d = math.exp(-(t - ts) * 6.0) * amp
                    c.x += d * math.sin((t - ts) * 71); c.y += d * math.cos((t - ts) * 53) * 1.4
        return c

    def render(self, t, frame):
        if self.obj is None:
            self.obj = scene(self.key, self.make)
        return self.obj.render(t, self.cam(t), frame)


_SCENES = {}


def scene(key, make):
    """One instance per scene setup, shared by every shot (camera setup) that films it."""
    if key not in _SCENES:
        _SCENES[key] = make()
    return _SCENES[key]


def ob(s):
    """The scene object a shot films (shared between camera setups)."""
    if s.obj is None:
        s.obj = scene(s.key, s.make)
    return s.obj


FLASH = []      # (time, strength, colour): lightning, impacts


def build_shots():
    """Bamberg v3, the plain telling. Cinema grammar: hard cuts on the beat (xin=xout=0), punch-ins between camera
    setups of one scene, push-ins on the lines that matter, a Dutch angle in the torture room, a camera hit and a white
    flash on the drop, black on 'Eight times', lightning on 'storms'."""
    sh = []
    v = V
    S0 = lambda l: v[l][0]
    E0 = lambda l: v[l][1]
    W = lambda l, w: find_word(l, w)[0]
    FLASH.clear()
    rr, rl = (972.9, 1240.5), (596.5, 1249.0)
    city = lambda: City('rain')
    cut = dict(xin=0.0, xout=0.0)

    # 1. OPEN: Bamberg in a storm; the witch house waits
    c1 = S0('o2') - 0.15
    sh.append(Shot('open_city', 0.0, c1, city, [(0.0, (800, 1150, 1.08)), (S0('o1') + 1.0, (815, 1350, 1.2)), (c1, (835, 1640, 1.55))],
                   xin=1.0, xout=0.0, key='city', hand=0.7))
    FLASH.extend([(0.35, 1.3, (0.75, 0.82, 1.0)), (0.55, 0.6, (0.75, 0.82, 1.0))])
    # 2. HARD CUT: the quill on the letter, very close; then the candle (title)
    c2 = S0('o3') - 0.1
    pen_keys = lambda s: (lambda c: [(c1, tuple(c.pen_plate(c1 + 0.3) + np.array([160, 20])) + (4.2,)),
                                     (c2, tuple(c.pen_plate(c2) + np.array([60, 30])) + (3.6,))])(ob(s))
    sh.append(Shot('quill', c1, c2, lambda: Cell('p1'), pen_keys, ap=9.0, key='cell_p1', **cut))
    c3 = S0('x1') - 0.5
    cand_keys = lambda s: (lambda fl: [(c2, (980, 1600, 1.7)), (E0('o3'), (1080, fl[1] + 160, 1.55)), (c3, (1105, fl[1] + 90, 1.75))])(ob(s).base.flame_plate)
    sh.append(Shot('candle', c2, c3, lambda: Cell('p1'), cand_keys, ap=9.0, key='cell_p1', xin=0.0, xout=0.7))
    # 3. WHO AND WHERE: the city, a crane down to the house; lightning on "storms"; hard cut to the witch house
    hx = W('x2', 'hunt') - 0.35
    cs = S0('x2') - 0.05
    sh.append(Shot('city_who', c3 - 0.7, cs, city, [(c3 - 0.7, (790, 900, 1.12)), (cs, (805, 1250, 1.2))],
                   xin=0.7, xout=0.0, key='city', hand=0.6))
    sh.append(Shot('city_storm', cs, hx, city, [(cs, (700, 1500, 1.55)), (hx, (760, 1640, 1.75))], key='city', hand=0.8, **cut))
    FLASH.append((W('x2', 'storms') - 0.05, 1.1, (0.75, 0.82, 1.0)))
    c4 = S0('x3') - 0.25
    sh.append(Shot('witch_house', hx, c4, lambda: City('rain', 2.4, (560, 1200)), [(hx, (845, 1700, 2.5)), (c4, (842, 1800, 2.85))],
                   xin=0.0, xout=0.5, key='portal', hand=0.5))
    # 4. THE METHOD: the chain of names (three camera setups, cut on the beat)
    names = lambda: Sheet('names')

    def nk(which):
        def k(s):
            o = ob(s).s
            root, wife, jun = o.at(o.info['gens'][0][0]), o.at(o.info['wife']), o.at(o.info['junius'])
            if which == 'a':
                return [(c4 - 0.5, (root[0], root[1] + 260, 1.8)), (W('x3', 'torture'), (810, root[1] + 520, 1.35)), (S0('x4'), (810, root[1] + 700, 1.18))]
            if which == 'b':
                return [(S0('x4'), (wife[0] + 110, wife[1] + 50, 2.3)), (S0('x5'), (wife[0] + 90, wife[1] + 70, 2.45))]
            return [(S0('x5'), (810, jun[1] - 420, 1.25)), (E0('x5') + 0.8, (810, jun[1] - 300, 1.4))]
        return k
    sh.append(Shot('names_a', c4 - 0.5, S0('x4') - 0.05, names, nk('a'), xin=0.5, xout=0.0, key='names', hand=0.7))
    sh.append(Shot('names_b', S0('x4') - 0.05, S0('x5') - 0.05, names, nk('b'), key='names', hand=0.8, **cut))
    sh.append(Shot('names_c', S0('x5') - 0.05, E0('x5') + 0.8, names, nk('c'), key='names', hand=0.8, xin=0.0, xout=0.4,
                   shake=[(W('x5', 'him') - 0.05, 9.0)]))
    # 5. THE WITNESS: the court record of 28 June, close; the judges, a cold pull back
    w0, w1 = E0('x5') + 0.6, S0('a3') - 0.1
    wk = W('a2', 'said') - 0.3
    sh.append(Shot('witness', w0, wk, lambda: Archive(2.2, rr), [(w0, (rr[0] - 60, rr[1] - 260, 2.35)), (wk, (rr[0] - 30, rr[1] - 140, 2.5))],
                   xin=0.4, xout=0.0, key='rec_r'))
    sh.append(Shot('witness_close', wk, w1, lambda: Archive(2.2, rr), [(wk, (rr[0] + 40, rr[1] - 60, 3.3)), (w1, (rr[0] + 50, rr[1] - 40, 3.55))],
                   key='rec_r', **cut))
    sh.append(Shot('judges', w1, E0('a3') + 0.5, lambda: Archive(), [(w1, (800, 1260, 1.5)), (E0('a3') + 0.5, (800, 1420, 1.08))],
                   xin=0.0, xout=0.5, key='archive', ap=6))
    # 6. TWO DAYS LATER: the torture room (Dutch angle), the record, the letter, the drop
    r0, r1 = E0('a3') + 0.3, S0('t2') - 0.1
    def ex_walk(t, ta, tb, xa, xb):
        u = float(np.clip((t - ta) / max(tb - ta, 1e-3), 0, 1))
        return xa + (xb - xa) * u * u * (3 - 2 * u), u
    def room_figs(t):
        X, u = ex_walk(t, r0 + 0.2, r1 - 0.2, 930, 720)
        return [('exec', X, 2900, 640, 380, (t * 5.2) if 0 < u < 1 else 0.0, 0.0, 0.0)]
    sh.append(Shot('room', r0, r1, lambda: Shadow('room', dict(figures=room_figs, rope=lambda t: (2950, 6 * math.sin(t * 0.8), 1.0))),
                   [(r0, (760, 1350, 1.16)), (r1, (840, 1420, 1.32))], xin=0.4, xout=0.0, key='room', hand=0.8, roll=-4.0, grade=dict(expo=1.18)))
    r2 = S0('t3') - 0.1
    sh.append(Shot('record_pain', r1, r2, lambda: Archive(2.2, rl), [(r1, (rl[0] - 40, rl[1] + 120, 2.4)), (r2, (rl[0] - 10, rl[1] + 220, 2.75))],
                   key='rec_l', grade=dict(expo=0.95, sat=0.75), **cut))
    r3 = S0('t4') - 0.1
    nails = W('t3', 'nails')
    sh.append(Shot('letter_nails', r2, r3, lambda: Cell('p4', quill_until=-100, blots=[(nails + 0.05, (380, 1290))]),
                   lambda s: [(r2, tuple(ob(s).page_plate(560, 1150)) + (2.9,)), (r3, tuple(ob(s).page_plate(420, 1290)) + (3.4,))],
                   key='cell_nails', ap=9.0, **cut))
    drop = W('t4', 'dropped')
    eight = W('t4', 'eight') - 0.08
    def hoist_rope(t):
        if t < drop:
            return (2950, 3 * math.sin(t * 2.0), 1.0)
        d = t - drop
        return (2950 + 140 * math.exp(-d * 3) * math.sin(d * 9), 70 * math.exp(-d * 1.2) * math.sin(d * 6.5), 0.0)
    def hoist_figs(t):
        arm = float(np.clip((t - r3) / max(drop - r3, 1e-3), 0, 1)) if t < drop else max(0.0, 1 - (t - drop) * 3)
        return [('exec', 760, 2900, 640, 380, 0.0, 0.25 * arm, arm)]
    sh.append(Shot('hoist', r3, eight, lambda: Shadow('room', dict(figures=hoist_figs, rope=hoist_rope)),
                   [(r3, (900, 1060, 1.3)), (drop, (900, 900, 1.5)), (drop + 0.3, (900, 1000, 1.42)), (eight, (890, 1080, 1.38))],
                   key='hoist', shake=[(drop, 30.0)], hand=0.8, roll=-3.0, grade=dict(expo=1.2), **cut))
    FLASH.append((drop + 0.02, 1.6, (1.0, 0.95, 0.88)))
    # 7. BLACK: "Eight times." (the count is in the sound)
    k0 = S0('k1') - 0.7
    sh.append(Shot('black_eight', eight, k0, lambda: Black(), [(0, (810, 1440, 1.0))], key='black', hand=0.0, **cut))
    # 8. THE TURN: the corridor, a lantern, two shadows; the plea
    stop = S0('k3') - 0.2
    def lx(t):
        u = float(np.clip((t - k0) / max(stop - k0, 1e-3), 0, 1))
        return 820 + 900 * (1 - (1 - u) ** 1.6)
    def corr_figs(t):
        x = lx(t)
        ph = (min(t, stop) - k0) * 3.6
        bow = float(np.clip((t - stop) / 1.2, 0, 1))
        return [('prisoner', x + 160, 2380, 470, 360, ph * 0.8, 0.0, 0.0), ('exec', x - 70, 2380, 500, 330, ph, bow, 0.0)]
    p1 = E0('k3') + 0.6
    corr = lambda: Shadow('corridor', dict(lx=lx, figures=corr_figs))
    sh.append(Shot('corridor', k0, stop, corr, [(k0, (lx(k0) + 330, 1500, 1.18)), (stop, (lx(stop) + 380, 1460, 1.26))],
                   PWc=2700, xin=1.0, xout=0.0, key='corridor', hand=0.7, grade=dict(expo=1.2)))
    sh.append(Shot('plea', stop, p1, corr, [(stop, (lx(stop) + 330, 1250, 1.75)), (p1, (lx(stop) + 320, 1200, 1.95))],
                   PWc=2700, xin=0.0, xout=0.5, key='corridor', hand=0.6, grade=dict(expo=1.25)))
    # 9. THE LIE: his letter, "nothing but lies", written now
    q0, q1 = p1 - 0.5, E0('l1') + 0.5
    def lie_keys(s):
        c = ob(s)
        a = c.pen_plate(W('l1', 'lied') + 0.2); b = c.pen_plate(E0('l1') - 0.4)
        return [(q0, (a[0] + 160, a[1] - 60, 2.2)), (S0('l1') + 0.6, (a[0] + 60, a[1], 3.1)), (q1, (b[0] - 30, b[1] + 30, 3.4))]
    sh.append(Shot('lie', q0, q1, lambda: Cell('p3'), lie_keys, xin=0.5, xout=0.0, key='cell_p3', ap=9.0))
    # 10. NAMES, STREET BY STREET: the town plan (cut wide, then in on the given name)
    streets = lambda: Sheet('streets')
    def sk(which):
        def k(s):
            o = ob(s).s
            mk = o.info['marks']
            a, b = o.at(mk[0]), o.at(mk[-1])
            n1, n2 = o.at((960, 300)), o.at((905, 1560))
            if which == 'a':
                return [(q1, (810, 1440, 1.25)), (S0('l3'), (810, 1400, 1.12)), (E0('l3'), ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 1.3))]
            return [(S0('l4'), (n1[0] - 90, n1[1] + 110, 1.9)), (E0('l4') - 1.0, (n2[0] - 120, n2[1] - 60, 1.85)), (E0('l4') + 0.8, (n2[0] - 110, n2[1] - 40, 2.05))]
        return k
    sh.append(Shot('streets_a', q1, S0('l4') - 0.05, streets, sk('a'), key='streets', hand=0.8, **cut))
    sh.append(Shot('streets_b', S0('l4') - 0.05, E0('l4') + 0.8, streets, sk('b'), key='streets', hand=0.8, xin=0.0, xout=0.6))
    # 11. THE LETTER: written over days; hide it; innocent; good night. The candle dies.
    g0, g1 = E0('l4') + 0.3, E0('e4') + 1.8
    def end_keys(s):
        c = ob(s)
        a = c.pen_plate(S0('e2') + 0.4); b = c.pen_plate(S0('e3') + 0.6); d = c.pen_plate(S0('e4') + 1.0)
        fl = c.base.flame_plate
        return [(g0, (1000, 1500, 1.35)), (S0('e1') + 2.0, (a[0] + 160, a[1] - 100, 2.2)), (S0('e2') + 0.4, (a[0] + 60, a[1], 3.0)),
                (S0('e3') + 0.6, (b[0], b[1] + 20, 3.1)), (S0('e4') + 1.0, (d[0] + 40, d[1] + 30, 2.6)), (E0('e4') - 0.4, (1000, 1500, 1.45)),
                (g1, (1080, fl[1] + 160, 1.3))]
    ge = S0('e2') - 0.05
    lastc = lambda: Cell('p4', gutter=(E0('e4') - 1.0, E0('e4') + 1.2))
    sh.append(Shot('last_lines', g0, ge, lastc, lambda s: [k for k in end_keys(s) if k[0] <= ge] + [(ge, end_keys(s)[1][1])],
                   xin=0.5, xout=0.0, key='cell_p4', ap=9.0))
    sh.append(Shot('last_lines_b', ge, g1, lastc, lambda s: [(ge, tuple(ob(s).pen_plate(ge + 0.3) + np.array([90, -10])) + (3.4,))] +
                   [k for k in end_keys(s) if k[0] > ge + 0.3], key='cell_p4', ap=9.0, xin=0.0, xout=1.0))
    # 12. AUGUST: grey morning, a bell; the file; the letter today
    d0, d1 = S0('f1') - 0.7, E0('f1') + 0.9
    sh.append(Shot('dawn', d0, d1, lambda: City('dawn'), [(d0, (820, 1520, 1.18)), (d1, (800, 1470, 1.26))], xin=0.9, xout=0.7,
                   key='dawn', hand=0.5))
    a0 = d1 - 0.7
    a1 = S0('f3') - 0.1
    sh.append(Shot('the_file', a0, a1, lambda: Archive(), [(a0, (790, 1300, 1.12)), (a1, (775, 1700, 1.35))], xin=0.7, xout=0.0,
                   key='archive', ap=6))
    a2 = E0('f3') + 1.4
    sh.append(Shot('today', a1, a2, lambda: Archive(), [(a1, (770, 1800, 1.5)), (a2, (762, 1880, 2.05))], key='archive', ap=6,
                   xin=0.0, xout=0.9))
    sh.append(Shot('endcard', E0('f3') + 1.0, TOTAL, lambda: Black(), [(0, (810, 1440, 1.0))], key='black', hand=0.0, xin=0.5, xout=0.0))
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


def flashes(img, t):
    """Lightning and impact flashes: a short over-exposure that decays in a quarter second."""
    for ft, k, col in FLASH:
        if ft <= t < ft + 0.35:
            d = math.exp(-(t - ft) * 14.0) * k
            img = img * (1 + d) + d * 0.25 * np.array(col, np.float32)
    return img


def labels():
    """On-screen labels: (start, end, lines, y, size, font). Plain words that tell the viewer where they are."""
    v = V
    L = [
        (0.5, v['o1'][1] + 0.3, ['BAMBERG, GERMANY', '1628'], 330, 40, 'Cinzel[wght].ttf'),
        (v['x1'][0] - 0.1, v['x1'][1] + 0.4, ['JOHANNES JUNIUS', 'mayor of Bamberg'], 330, 40, 'Cinzel[wght].ttf'),
        (find_word('x2', 'hunt')[0] - 0.3, v['x3'][0] - 0.6, ['THE WITCH PRISON', 'built 1627'], 330, 36, 'Cinzel[wght].ttf'),
        (v['a1'][0] - 0.3, v['a2'][1] + 0.3, ['COURT RECORD', '28 June 1628'], 330, 36, 'Cinzel[wght].ttf'),
        (v['t1'][0] - 0.3, v['t1'][1] + 0.3, ['30 JUNE 1628'], 330, 36, 'Cinzel[wght].ttf'),
        (v['t2'][0] - 0.1, v['t2'][1] + 0.4, ['THE COURT RECORD', '“feels no pain”'], 330, 38, 'Cinzel[wght].ttf'),
        (v['t3'][0] - 0.1, v['t3'][1] + 0.3, ['HIS LETTER'], 330, 40, 'Cinzel[wght].ttf'),
        (find_word('l1', 'lied')[0] - 0.2, v['l1'][1] + 0.4, ['HIS LETTER', '“Now follows my statement:', 'nothing but lies.”'], 330, 34, 'Cinzel[wght].ttf'),
        (v['e1'][0] - 0.2, v['e1'][1] + 0.4, ['TO HIS DAUGHTER, VERONICA', '24 July 1628'], 330, 34, 'Cinzel[wght].ttf'),
        (v['f1'][0] - 0.4, v['f1'][1] + 0.6, ['AUGUST 1628'], 330, 38, 'Cinzel[wght].ttf'),
        (v['f3'][0] - 0.1, v['f3'][1] + 0.9, ['TODAY', 'Staatsbibliothek Bamberg'], 330, 36, 'Cinzel[wght].ttf'),
    ]
    return L


def overlays(img, t):
    global CAPS
    if CAPS is None:
        CAPS = _caps()
    for i, (a, b, lines, fn) in enumerate(CAPS):
        fi = 0.2 if i == 0 or a - CAPS[i - 1][1] > 0.3 else 0.0
        fo = 0.2 if i == len(CAPS) - 1 or CAPS[i + 1][0] - b > 0.3 else 0.0
        if a - fi <= t < b + fo:
            op = min(1.0, (t - (a - fi)) / fi if fi else 1.0, ((b + fo) - t) / fo if fo else 1.0)
            rgb, al = text(lines, fn, 54)
            E.put(img, rgb, al, W / 2, 1500, opacity=op, shadow=0.95)
    for a, b, lines, y, size, fn in labels():
        if a < t < b:
            op = min(1.0, (t - a) / 0.25, (b - t) / 0.35)
            size = int(size * 1.45); y = 300
            band_h = int(size * (1.6 + 1.2 * (len(lines) - 1)))
            yy = np.arange(H, dtype=np.float32)[:, None]
            band = np.exp(-((yy - (y + band_h * 0.3)) / (band_h * 0.75)) ** 2) * 0.55 * op
            img *= (1 - band)[..., None]
            rgb, al = text([lines[0]], fn, size, col=(0.92, 0.84, 0.68), tracking=6)
            E.put(img, rgb, al, W / 2, y, opacity=op, shadow=0.95, glow=0.12)
            if len(lines) > 1:
                rgb, al = text(lines[1:], 'Newsreader-Italic[opsz,wght].ttf', int(size * 1.05), col=(0.9, 0.87, 0.8), spacing=1.15)
                E.put(img, rgb, al, W / 2, y + size * 1.15 + 20 * (len(lines) - 1), opacity=op * 0.95, shadow=0.95)
    # title card over the candle, after the opening promise
    ta = V['o3'][1] + 0.35
    if ta < t < V['x1'][0] - 0.3:
        u = t - ta; dur = V['x1'][0] - 0.3 - ta
        op = min(1.0, u / 0.5, (dur - u) / 0.5)
        rgb, al = text(['DARK CORNERS'], 'Cinzel[wght].ttf', 36, col=(0.86, 0.72, 0.5), tracking=10)
        E.put(img, rgb, al, W / 2, 760, opacity=op * 0.9, glow=0.25)
        rgb, al = text(['The Mayor', 'Who Was Called a Witch'], 'Newsreader-Italic[opsz,wght].ttf', 84, spacing=1.08)
        E.put(img, rgb, al, W / 2, 920, opacity=op, shadow=0.9, glow=0.18)
    # end card
    ea = V['f3'][1] + 1.3
    if t > ea:
        op = min(1.0, (t - ea) / 0.6)
        rgb, al = text(['DARK CORNERS'], 'Cinzel[wght].ttf', 44, col=(0.86, 0.72, 0.5), tracking=11)
        E.put(img, rgb, al, W / 2, 820, opacity=op, glow=0.3)
        rgb, al = text(['Johannes Junius', '1573 – 1628'], 'Newsreader-Italic[opsz,wght].ttf', 50, col=(0.92, 0.89, 0.82), spacing=1.25)
        E.put(img, rgb, al, W / 2, 980, opacity=op)
        rgb, al = text(['His letter of 24 July 1628 is kept in the', 'Staatsbibliothek Bamberg.', 'Trial record after Burr (1896).'],
                       'Newsreader[opsz,wght].ttf', 31, col=(0.72, 0.69, 0.64), spacing=1.35)
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
    img = flashes(img, t)
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


def prebuild(a, b):
    pages_for_film()
    for s in shots():
        if s.t1 >= a / FPS - 0.1 and s.t0 <= b / FPS + 0.1:
            print('preparing', s.name, flush=True)
            s.keys(s) if callable(s.keys) else None
            if s.obj is None:
                s.obj = s.make()


def frames_main(a, b, out):
    import multiprocessing as mp
    b = min(b, NF)
    n = int(os.environ.get('FILM_WORKERS', '2'))
    n = max(1, min(n, b - a))
    chunks = [(i, list(range(a + (b - a) * i // n, a + (b - a) * (i + 1) // n)), f'{out}.part{i}.mp4') for i in range(n)]
    ctx = mp.get_context('spawn')
    pre = ctx.Process(target=prebuild, args=(a, b))     # paint every plate this stretch needs once, before the workers
    pre.start(); pre.join()
    if pre.exitcode != 0:
        sys.exit('painting the plates failed')
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
