"""A sheet of paper on the archive table, filled by ink as the story speaks (no hand, no quill: the ink draws itself).
  names    the chain of accusations: marks that name marks, his wife's name struck through, six lines converging on Junius
  streets  the town plan he walks in his mind: streets re-inked one by one, the long street, eight names, then "N. N."
  spee     the title page of the Cautio Criminalis (Rinteln, 1631), printed
The paper and table are a painted plate; the ink is a time map (each pixel knows when it was written)."""
from darkroot import ROOT
import math
import numpy as np
import cv2
import engine as E
import shade as S
import tex as TX
import plates as PL
import hand
import pages as PG

PW, PH = 1620, 2880
DENS = 1.5
SW, SH = 1134, 1728           # sheet px (same paper scale as the letter)
INK = np.array([0.16, 0.10, 0.06], np.float32)
PRINT = np.array([0.07, 0.06, 0.055], np.float32)


def sheet_H(rot=-1.6, scale=1.3, cx=810.0, cy=1440.0):
    a = math.radians(rot)
    c, s = math.cos(a) * scale, math.sin(a) * scale
    return np.array([[c, -s, cx - c * SW / 2 + s * SH / 2], [s, c, cy - s * SW / 2 - c * SH / 2], [0, 0, 1]], np.float64)


def prepare(kind, force=False):
    name = 'sheet_' + kind
    z = None if force else PL.load(name)
    if z is not None:
        return z
    yy, xx = np.mgrid[0:PH, 0:PW].astype(np.float32)
    wood, _, _ = TX.surface('dark_wooden_planks', PH, PW, scale=1.1, tint=(0.8, 0.62, 0.45))
    seed = {'names': 3, 'streets': 5, 'spee': 9}[kind]
    col = (0.9, 0.86, 0.76) if kind == 'spee' else (0.86, 0.79, 0.64)
    alb, hgt, pa = S.paper(SH, SW, seed=seed, col=col, age=0.35 if kind == 'spee' else 0.6,
                           folds=() if kind == 'spee' else ((0.5, 'h'), (0.5, 'v')))
    Hs = sheet_H(rot={'names': -1.6, 'streets': 1.2, 'spee': -0.6}[kind])
    pw = cv2.warpPerspective(np.dstack([alb * pa[..., None], pa]), Hs, (PW, PH), flags=cv2.INTER_LINEAR)
    a = pw[..., 3:]
    # the sheet's shadow on the table
    sh = cv2.GaussianBlur(cv2.warpAffine(a[..., 0], np.float32([[1, 0, 14], [0, 1, 22]]), (PW, PH)), (0, 0), 14)
    img = wood * (1 - 0.6 * sh)[..., None]
    img = img * (1 - a) + pw[..., :3]
    # candle from the upper left, cool night air from the right
    d = np.sqrt((xx + 150) ** 2 + (yy - 700) ** 2)
    warm = 1.25 / (1 + (d / 900) ** 2.2)
    img = img * (warm[..., None] * np.array([1.0, 0.7, 0.42], np.float32) + np.array([0.035, 0.04, 0.06], np.float32))
    lum = img.mean(-1, keepdims=True)
    img = lum + (img - lum) * 0.8
    pr, _ = PL.paint_layer(img, None, 1.5, seed=70 + seed, grade='warm', expo=1.45)
    PL.save(name, img=pr, H=Hs)
    return PL.load(name)


# ------------------------------------------------------------------ ink content (sheet px, global film seconds)
def _line(p0, p1, t0, t1, w=3.2, n=None, wob=1.2, seed=0):
    r = np.random.default_rng(seed)
    p0, p1 = np.array(p0, np.float32), np.array(p1, np.float32)
    L = float(np.linalg.norm(p1 - p0))
    n = n or max(8, int(L / 6))
    u = np.linspace(0, 1, n)[:, None]
    pts = p0 + (p1 - p0) * u
    nrm = np.array([-(p1 - p0)[1], (p1 - p0)[0]], np.float32) / max(L, 1)
    pts += nrm * (np.sin(u * math.pi * r.uniform(1, 2.5)) * wob + r.normal(0, 0.25, (n, 1)))
    wid = (w * (0.75 + 0.25 * np.sin(u[:, 0] * math.pi))).astype(np.float32)
    ink = np.clip(1.0 - u[:, 0] * 0.4, 0.4, 1).astype(np.float32)
    tm = (t0 + (t1 - t0) * u[:, 0]).astype(np.float32)
    return (pts.astype(np.float32), wid, ink, tm)


def _poly(pts, t0, t1, w=2.6, seed=0):
    pts = np.array(pts, np.float32)
    seg = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    dense = []
    for i in range(len(pts) - 1):
        k = max(2, int((seg[i + 1] - seg[i]) / 5))
        for u in np.linspace(0, 1, k, endpoint=False):
            dense.append(pts[i] + (pts[i + 1] - pts[i]) * u)
    dense.append(pts[-1])
    dense = np.array(dense, np.float32)
    s2 = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(dense, axis=0), axis=1))])
    u = s2 / max(s2[-1], 1)
    r = np.random.default_rng(seed)
    dense += r.normal(0, 0.3, dense.shape).astype(np.float32)
    return (dense, (w * (0.8 + 0.2 * np.sin(u * 9))).astype(np.float32), np.clip(1 - u * 0.35, 0.5, 1).astype(np.float32),
            (t0 + (t1 - t0) * u).astype(np.float32))


def _cross(c, t0, s=16, w=2.8, seed=0):
    x, y = c
    return [_line((x - s, y - s * 0.9), (x + s, y + s * 1.1), t0, t0 + 0.09, w, wob=0.6, seed=seed),
            _line((x + s * 0.9, y - s), (x - s * 1.1, y + s), t0 + 0.12, t0 + 0.21, w, wob=0.6, seed=seed + 1)]


def _words(text, x, y, t0, t1, style=PG.JUNIUS, size=None, seed=0, center=True):
    st = dict(style)
    if size:
        st['size'] = size
    words = hand.layout([text], st['fname'], size=st['size'], width=2000, x0=0, y0=0, seed=seed, slant=st['slant'],
                        xs=st['xs'], angular=st['angular'], lead=st['lead'])
    xs = np.concatenate([np.concatenate(w['strokes']) for w in words])[:, 0]
    dx = x - (xs.min() + xs.max()) / 2 if center else x - xs.min()
    for w in words:
        w['strokes'] = [s + np.array([dx, y], np.float32) for s in w['strokes']]
    return hand.pen(words, t0, t1, tremble=st['tremble'] * 0.7, wmax=st['wmax'] * 0.8, wmin=st['wmin'], seed=seed + 5)


def names_segs(T):
    """T: dict of line start/end times (global). The chain: w3 (a mark names marks), w4 (his wife), w5 (six on Junius)."""
    segs = []
    r = np.random.default_rng(11)
    a, b = T['w3'][0] + 0.2, T['w3'][1]
    gens = [[(567.0, 190.0)]]
    counts = [3, 7, 12]
    ys = [400, 640, 900]
    for g, (n, y) in enumerate(zip(counts, ys)):
        xs = np.linspace(150, 984, n) + r.uniform(-30, 30, n)
        gens.append([(float(x), float(y + r.uniform(-30, 30))) for x in xs])
    span = (b - a)
    tg = [a, a + 0.18 * span, a + 0.45 * span, a + 0.72 * span]
    segs += _cross(gens[0][0], tg[0], s=18, seed=1)
    parents = {}
    for g in range(1, 4):
        prev = gens[g - 1]
        for i, c in enumerate(gens[g]):
            pj = min(range(len(prev)), key=lambda j: abs(prev[j][0] - c[0]) + r.uniform(0, 120))
            parents[(g, i)] = pj
            t0 = tg[g] + i * (0.26 * span / max(len(gens[g]), 1)) * 0.9
            p = prev[pj]
            segs.append(_line((p[0], p[1] + 22), (c[0], c[1] - 24), t0, t0 + 0.28, 2.0, seed=100 + g * 20 + i))
            segs += _cross(c, t0 + 0.3, s=14, seed=200 + g * 20 + i)
    # w4: his wife, named, then struck through
    wa, wb = T['w4']
    wife = gens[2][2]
    segs += _words('des Junius Hausfraw', wife[0] + 10, wife[1] + 40, wa + 0.25, wa + 1.9, style=PG.CLERK, size=42, seed=31)
    segs.append(_line((wife[0] - 140, wife[1] + 50), (wife[0] + 165, wife[1] + 44), wb - 1.6, wb - 1.25, 3.4, wob=0.8, seed=33))
    # w5: Johannes Junius written low on the sheet, then six lines converge on him
    ja, jb = T['w5']
    jx, jy = 567.0, 1330.0
    segs += _words('Johannes Junius', jx, jy, ja - 0.9, ja + 0.4, style=PG.CLERK, size=56, seed=41)
    six = [gens[3][k] for k in (1, 3, 5, 7, 9, 11)]
    for k, c in enumerate(six):
        t0 = ja + 0.55 + k * 0.32
        ex = jx + (c[0] - jx) * 0.18
        segs.append(_line((c[0], c[1] + 22), (ex, jy - 46), t0, t0 + 0.4, 2.4, seed=60 + k))
    # a circle round his name at the end of the line
    ang = np.linspace(-0.4, 2 * math.pi - 0.2, 60)
    ring = np.stack([jx + 225 * np.cos(ang), jy - 8 + 62 * np.sin(ang)], 1)
    segs.append(_poly(ring, jb - 0.3, jb + 0.5, 2.2, seed=71))
    return segs, dict(gens=gens, wife=wife, junius=(jx, jy))


STREETS = {
    'long': [(250, 260), (330, 470), (420, 690), (500, 900), (590, 1110), (690, 1320), (800, 1520)],
    'cross1': [(120, 760), (360, 760), (620, 740), (1010, 700)],
    'cross2': [(160, 1180), (420, 1150), (640, 1130), (1000, 1080)],
    'markt': [(560, 850), (760, 830), (790, 1000), (590, 1020), (560, 850)],
    'bridge': [(140, 520), (330, 520)],
}
RIVER = [[(70, 120), (90, 400), (60, 700), (95, 1000), (70, 1300), (100, 1650)],
         [(170, 120), (190, 400), (160, 700), (195, 1000), (170, 1300), (200, 1650)]]


def streets_segs(T):
    segs = []
    # already drawn: the river, the Domberg, the streets in pale ink
    for k, rv in enumerate(RIVER):
        segs.append(_poly(rv, -10, -9.5, 2.0, seed=k))
    for k, (nm, pts) in enumerate(STREETS.items()):
        segs.append(_poly([(x + 10, y) for x, y in pts], -10, -9.5, 1.5, seed=10 + k))
        segs.append(_poly([(x - 10, y) for x, y in pts], -10, -9.5, 1.5, seed=20 + k))
    for k in range(14):                                             # the cathedral hill, hatched
        x = 260 + k * 18
        segs.append(_line((x, 130 + (k % 3) * 6), (x - 40, 230), -10, -9.6, 1.4, seed=40 + k))
    segs += _words('Regnitz', 135, 1690, -10, -9, style=PG.CLERK, size=38, seed=51)
    segs += _words('Dom', 330, 100, -10, -9, style=PG.CLERK, size=40, seed=52)
    segs += _words('Marckt', 675, 930, -10, -9, style=PG.CLERK, size=38, seed=53)
    # l5: street by street, re-inked
    a, b = T['l5'][0] + 0.2, T['l5'][1] + 0.4
    order = ['markt', 'cross1', 'cross2', 'bridge']
    for k, nm in enumerate(order):
        t0 = a + k * (b - a) / len(order)
        segs.append(_poly(STREETS[nm], t0, t0 + (b - a) / len(order) * 0.9, 3.2, seed=80 + k))
    # l6: the long street (written along it), then eight marks
    a6, b6 = T['l6']
    segs.append(_poly(STREETS['long'], a6 + 0.6 * (b6 - a6) - 0.9, a6 + 0.6 * (b6 - a6), 3.6, seed=90))
    segs += _words('Lange Gaß', 545, 610, a6 + 0.55 * (b6 - a6), a6 + 0.55 * (b6 - a6) + 0.9, style=PG.CLERK, size=42, seed=91)
    pts = np.array(STREETS['long'], np.float32)
    seg = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    t8 = a6 + 0.78 * (b6 - a6)
    marks = []
    for k in range(8):
        s = seg[-1] * (0.08 + 0.84 * k / 7)
        i = int(np.searchsorted(seg, s)) - 1
        i = max(0, min(i, len(pts) - 2))
        u = (s - seg[i]) / (seg[i + 1] - seg[i])
        p = pts[i] + (pts[i + 1] - pts[i]) * u
        side = 46 if k % 2 == 0 else -46
        c = (float(p[0] + side), float(p[1]))
        marks.append(c)
        segs += _cross(c, t8 + k * 0.2, s=12, w=2.6, seed=100 + k)
    # l7: a name given (the clerk's hand) and repeated (his)
    a7, b7 = T['l7']
    mid = a7 + 0.5 * (b7 - a7)
    segs += _words('N. N.', 960, 300, mid - 0.9, mid - 0.4, style=PG.CLERK, size=60, seed=111)
    segs += _words('N. N.', 905, 1560, b7 - 0.9, b7 - 0.3, style=PG.JUNIUS, size=62, seed=112)
    return segs, dict(marks=marks)


SPEE_LINES = [('CAVTIO', 92, 0), ('CRIMINALIS,', 64, 0), ('SEV DE', 34, 0), ('PROCESSIBVS', 58, 0), ('CONTRA SAGAS', 58, 0),
              ('LIBER.', 46, 0), ('', 24, 0), ('Ad Magistratus Germaniae', 34, 1), ('hoc tempore necessarius.', 34, 1),
              ('', 60, 0), ('RINTELII,', 40, 0), ('ANNO M. DC. XXXI.', 38, 0)]


def spee_maps():
    """Printed title page: coverage of type, rules and a small ornament (all already printed)."""
    from PIL import Image, ImageDraw, ImageFont
    ss = 2
    im = Image.new('L', (SW * ss, SH * ss), 0)
    d = ImageDraw.Draw(im)
    y = 210 * ss
    for txt, size, it in SPEE_LINES:
        if not txt:
            y += size * ss
            continue
        f = ImageFont.truetype(ROOT + '/fonts/' + ('IMFeENit28P.ttf' if it else 'IMFeENrm28P.ttf'), size * ss)
        tw = f.getlength(txt)
        d.text(((SW * ss - tw) / 2, y), txt, font=f, fill=255)
        y += int(size * 1.32 * ss)
        if txt in ('LIBER.',):
            d.line([(SW * ss * 0.32, y + 10 * ss), (SW * ss * 0.68, y + 10 * ss)], fill=255, width=2 * ss)
            y += 30 * ss
    d.rectangle([90 * ss, 140 * ss, (SW - 90) * ss, (SH - 120) * ss], outline=255, width=3 * ss)
    d.rectangle([104 * ss, 154 * ss, (SW - 104) * ss, (SH - 134) * ss], outline=255, width=1 * ss)
    a = np.asarray(im, np.float32) / 255.0
    a = cv2.resize(a, (SW, SH), interpolation=cv2.INTER_AREA)
    # uneven press: ink a little patchy
    n = S.fbm(SH, SW, 40, 3, 5)
    a = a * (0.8 + 0.3 * n)
    return np.clip(a, 0, 1).astype(np.float32)


class SheetShot:
    def __init__(self, kind, T=None):
        self.kind = kind
        self.z = prepare(kind)
        self.Hs = self.z['H'].astype(np.float64)
        self.layer = E.Layer(self.z['img'], None, Z=1.0, d=DENS, anchor=(PW / 2.0, PH / 2.0), name='sheet')
        self.layer.dyn = self.ink
        if kind == 'spee':
            self.static = spee_maps()
            self.maps = None
            self.info = {}
        else:
            segs, self.info = (names_segs if kind == 'names' else streets_segs)(T)
            cov, dark, tmap = hand.rasterize(segs, SH, SW, ss=2)
            self.maps = (cov, dark, tmap)
        self.flick = 1.0

    def at(self, p):
        """Sheet px to plate px."""
        q = self.Hs @ np.array([p[0], p[1], 1.0])
        return q[0] / q[2], q[1] / q[2]

    def ink(self, t, rgb, a):
        if self.maps is None:
            cov, wet = self.static, None
            col = PRINT
        else:
            cov, wet = hand.at_time(*self.maps, t, wet=1.2)
            col = INK
        cs = np.array([[0, 0, 1], [SW, 0, 1], [SW, SH, 1], [0, SH, 1]], np.float64)
        q = (self.Hs @ cs.T).T
        q = q[:, :2] / q[:, 2:]
        x0, y0 = np.maximum(np.floor(q.min(0)).astype(int) - 2, 0)
        x1, y1 = np.minimum(np.ceil(q.max(0)).astype(int) + 2, [rgb.shape[1], rgb.shape[0]])
        T = np.array([[1, 0, -x0], [0, 1, -y0], [0, 0, 1]], np.float64) @ self.Hs
        rgb = rgb.copy()
        reg = rgb[y0:y1, x0:x1]
        cw = cv2.warpPerspective(cov, T, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR)
        lum = reg.mean(-1, keepdims=True)
        reg[:] = reg * (1 - cw[..., None] * 0.9) + col * (0.6 + 0.8 * lum) * cw[..., None] * 0.9
        if wet is not None:
            ww = cv2.warpPerspective(wet, T, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR)
            reg += (ww * 0.6)[..., None] * np.array([0.35, 0.3, 0.3], np.float32) * lum
        g = 1 + 0.06 * E.noise1(t, 7, 2.2) + 0.03 * E.noise1(t, 8, 7.7)
        return rgb * g, a

    def render(self, t, cam, frame):
        return E.compose([self.layer], cam, t)
