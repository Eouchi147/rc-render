"""Dark Corners film kit: the machinery of the approved Bamberg v3 film (timeline from the voice, shots with cameras,
hard cuts and crossfades, flashes, labels on a dark band, captions, title and end cards, film look, parallel frame
rendering), shared by every later episode. A film module calls configure(), defines its shots with Shot(), and ends
with main(). Scenes: Look (a look/scenes.py 2.5D scene in painted depth layers), Cell (a document written by
candlelight, from shot_cell), Black.
    python film_<name>.py info | still T out.jpg | frames A B out.mp4"""
from darkroot import ROOT, ffmpeg_exe
import sys, os, json, math, copy, subprocess, importlib
sys.path.insert(0, ROOT + '/film')
sys.path.insert(0, ROOT + '/look')
import numpy as np
import cv2
import soundfile as sf
import engine as E
import pages as PG

FPS, W, H = 24, 1080, 1920
C = dict()                    # the film's configuration (see configure)
S = V = TM = None
TOTAL = NF = 0
ORDER, QUOTE = [], {}
GAP = {}


# ------------------------------------------------------------------ configuration and timeline
def configure(name, direct, vo_dir, gap=None, gap_default=0.5, limit=179.4, end_card=2.6, title=('DARK CORNERS', ['']),
              end=None, labels=None, build=None, pages=None, tempo_fit=True):
    """name: film id; direct: script module name; vo_dir: folder of <line>.wav + timing.json; gap: {line: pause before};
    title: (series, [title lines]); end: [(lines, font, size, colour, y)]; labels: fn() -> label list; build: fn() -> shots;
    pages: fn() -> {page id: built page} for Cell shots."""
    global S, V, TM, TOTAL, NF, ORDER, QUOTE
    D = importlib.import_module(direct)
    C.update(name=name, direct=D, vo=vo_dir.rstrip('/') + '/', limit=limit, end_card=end_card, title=title, end=end or [],
             labels=labels or (lambda: []), build=build, pages=pages)
    ORDER[:] = [l[0] for l in D.LINES]
    QUOTE.clear(); QUOTE.update({l[0]: l[4] for l in D.LINES})
    GAP.clear(); GAP.update({lid: (gap or {}).get(lid, gap_default) for lid in ORDER})
    S, V, TM, TOTAL = _timeline()
    NF = int(math.ceil(TOTAL * FPS))
    if pages:
        PG.pages_for_film = pages_for_film


def _timeline(fitted=False):
    tm = json.load(open(C['vo'] + 'timing.json'))
    S_, V_ = {}, {}
    t = 0.0
    for lid in ORDER:
        x, sr = sf.read(C['vo'] + lid + '.wav', dtype='float32')
        e = np.abs(x) > 0.01
        on, off = np.argmax(e) / sr, (len(x) - np.argmax(e[::-1])) / sr
        t += GAP[lid]
        S_[lid] = t - on
        V_[lid] = (t, S_[lid] + off)
        t = V_[lid][1]
    total = t + 0.7 + C['end_card']
    if total > C['limit'] and not fitted:
        over = total - C['limit']
        k = max(0.6, 1 - over / sum(GAP.values()))
        for lid in GAP:
            GAP[lid] *= k
        return _timeline(True)
    return S_, V_, tm, total


def find_word(lid, w):
    w = w.lower()
    for k, (wd, a, b) in enumerate(TM[lid]['words']):
        if wd.lower().strip('.,:;!?"“”') == w:
            return S[lid] + a, S[lid] + b
    raise KeyError((lid, w, [x[0] for x in TM[lid]['words']]))


def S0(l):
    return V[l][0]


def E0(l):
    return V[l][1]


def Wd(l, w):
    """Start of word w in line l; falls back to the line start if the voice dropped the word."""
    try:
        return find_word(l, w)[0]
    except KeyError:
        return V[l][0]


_PAGES = {}


def pages_for_film():
    if not _PAGES and C.get('pages'):
        _PAGES.update(C['pages']())
    return _PAGES


# ------------------------------------------------------------------ camera
def smooth_keys(t, ks):
    ts = [k[0] for k in ks]
    if t <= ts[0]:
        return np.array(ks[0][1], float)
    if t >= ts[-1]:
        return np.array(ks[-1][1], float)
    i = max(0, int(np.searchsorted(ts, t)) - 1)
    P = [np.array(ks[max(0, min(len(ks) - 1, j))][1], float) for j in (i - 1, i, i + 1, i + 2)]
    u = (t - ts[i]) / max(ts[i + 1] - ts[i], 1e-6)
    u = u * u * (3 - 2 * u) * 0.35 + u * 0.65
    p0, p1, p2, p3 = P
    return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)


def cam_world(u, v, f, PWc=1620, PHc=2880, dens=1.5, ap=0.0, focus=1.0, t=0.0, hand=1.0, roll=0.0):
    jx = hand * (2.2 * E.noise1(t, 51, 0.31) + 0.8 * E.noise1(t, 52, 1.1))
    jy = hand * (2.2 * E.noise1(t, 53, 0.27) + 0.8 * E.noise1(t, 54, 0.9))
    rl = roll + hand * 0.12 * E.noise1(t, 55, 0.2)
    return E.Cam(x=(u - PWc / 2) / dens + jx, y=(v - PHc / 2) / dens + jy, f=f, ap=ap, focus=focus, roll=rl)


# ------------------------------------------------------------------ scenes
def zoom_scene(sc, zoom, center):
    """Scale a look scene around `center` (design px) so it renders as a detail plate."""
    if zoom == 1.0:
        return sc
    s2 = copy.deepcopy(sc)
    c = np.array(center, np.float32)
    m = np.array([540.0, 960.0], np.float32)
    f = lambda p: (p - c) * zoom + m
    for it in s2.items:
        it.polys = [f(p) for p in it.polys]
        it.lines = [(f(p), w * zoom) for p, w in it.lines]
        if it.wline is not None:
            it.wline = (it.wline - c[1]) * zoom + m[1]
    for L in s2.lights:
        L.x, L.y = (L.x - c[0]) * zoom + m[0], (L.y - c[1]) * zoom + m[1]
        L.r *= zoom
    sk = s2.sky
    if 'glow' in sk:
        sk['glow'] = [((gx - c[0]) * zoom + m[0], (gy - c[1]) * zoom + m[1], r * zoom, col, a) for gx, gy, r, col, a in sk['glow']]
    if 'moon' in sk:
        mx, my, mr, mc = sk['moon']
        sk['moon'] = ((mx - c[0]) * zoom + m[0], (my - c[1]) * zoom + m[1], mr * zoom, mc)
    if 'bright' in sk:
        sk['bright'] = [((x - c[0]) * zoom + m[0], (y - c[1]) * zoom + m[1], r * zoom ** 0.5) for x, y, r in sk['bright']]
    if s2.sun is not None:
        s2.sun = ((s2.sun[0] - c[0]) * zoom + m[0], (s2.sun[1] - c[1]) * zoom + m[1])
    for fg in s2.fog:
        fg['y0'] = (fg['y0'] - c[1]) * zoom + m[1]; fg['y1'] = (fg['y1'] - c[1]) * zoom + m[1]
    return s2


PW, PH = 1620, 2880


def prepare_look(key, make, groups, zoom=1.0, center=(540, 960), expo=1.3, contrast=1.1, sat=1.25, detail=None):
    """Paint (once, then cached) the depth layers of a look scene. groups: [(name, z0, z1)], the first one opaque."""
    import plates as PL
    from core import base_render, filmic
    name = key + ('' if zoom == 1.0 else f'_z{zoom:g}_{int(center[0])}_{int(center[1])}')
    z = PL.load(name)
    if z is not None:
        return z
    sc = zoom_scene(make(), zoom, center)
    sc_ = 1.5 * zoom / (1.0 if zoom == 1.0 else 1.6)
    arrs = {}
    for i, (g, z0, z1) in enumerate(groups):
        s2 = copy.copy(sc)
        s2.items = [it for it in sc.items if z0 <= it.z < z1]
        if i > 0:
            s2.fog = []
        buf = base_render(s2, PW, PH)
        img = filmic(buf['img'], exposure=expo, contrast=contrast, sat=sat)
        a = None if i == 0 else np.clip(buf['cover'], 0, 1)
        pr, pa = PL.paint_layer(img.astype(np.float32), a, sc_, seed=31 + i, display=True, detail=(detail or {}).get(g, 1.0))
        arrs[g] = pr
        if pa is not None:
            arrs[g + '_a'] = pa
    lights = [(L.x * PW / 1080, L.y * PW / 1080, L.r * PW / 1080, L.I, *L.col) for L in sc.lights]
    arrs['lights'] = np.array(lights if lights else np.zeros((0, 7)), np.float32).reshape(-1, 7)
    PL.save(name, **arrs)
    return PL.load(name)


class Look:
    """A painted look scene as depth layers under the camera, with flickering fire light and optional live rain,
    flames, embers and fog drift. live(look, img, t, cam) adds anything else."""

    def __init__(self, key, make, groups, zs, zoom=1.0, center=(540, 960), rain=None, flames=(), embers=None, flicker=True,
                 live=None, grade=None, **kw):
        self.z = prepare_look(key, make, groups, zoom, center, **kw)
        self.zoom = zoom
        cx, cy = center[0] * 1.5, center[1] * 1.5
        self.layers = []
        for (g, _, _), Z in zip(groups, zs):
            # each depth layer anchored so the detail's centre lines up through the parallax when the camera points at it
            anchor = (810.0, 1440.0) if zoom == 1.0 else (810.0 - zoom * (cx - 810.0) / Z, 1440.0 - zoom * (cy - 1440.0) / Z)
            self.layers.append(E.Layer(self.z[g], self.z.get(g + '_a'), Z=Z, d=1.5 * zoom, anchor=anchor, name=g))
        self.ref = self.layers[-1]
        self.lights = self.z['lights']
        self.rain, self.flames, self.embers, self.flicker, self.live, self.grade = rain, flames, embers, flicker, live, grade
        self.center = center

    def plate(self, x, y):
        """Design point (1080x1920 of the wide scene) -> plate point of the camera space."""
        return (x * 1.5, y * 1.5)

    def screen(self, cam, t, x, y, layer=None):
        """Design point of the (zoomed) scene -> screen point."""
        L = layer or self.ref
        if self.zoom != 1.0:
            x = (x - self.center[0]) * self.zoom + 540; y = (y - self.center[1]) * self.zoom + 960
        return E.layer_point(L, cam, t, x * 1.5, y * 1.5)

    def clamp(self, cam, t):
        """Keep the frame inside the opaque back plate: raise the zoom if the plate is too small, then slide the
        camera back inside (a framing guard, so no move can show the plate's edge)."""
        import copy as _c
        c = _c.copy(cam)
        L = self.layers[0]
        h, w = L.rgb.shape[:2]
        ca, sa = abs(math.cos(math.radians(c.roll))), abs(math.sin(math.radians(c.roll)))
        Wm, Hm = (W * ca + H * sa) * 1.02, (W * sa + H * ca) * 1.02       # the rotated frame's bounding box
        den = max(L.Z - c.z, 1e-3)
        s = c.f * L.Z / (L.d * den)
        need = max(Wm / (s * w), Hm / (s * h), 1.0)
        if need > 1.0:
            c.f *= need; s *= need
        u0, v0 = L.anchor
        kx = c.f / den
        lo_x, hi_x = (Wm / 2 - s * u0) / kx, (s * w - s * u0 - Wm / 2) / kx
        lo_y, hi_y = (Hm / 2 - s * v0) / kx, (s * h - s * v0 - Hm / 2) / kx
        if lo_x <= hi_x:
            c.x = min(max(c.x, lo_x), hi_x)
        if lo_y <= hi_y:
            c.y = min(max(c.y, lo_y), hi_y)
        return c

    def render(self, t, cam, frame):
        cam = self.clamp(cam, t)
        img = E.compose(self.layers, cam, t)
        if self.flicker and len(self.lights):
            g = np.zeros((H // 4, W // 4), np.float32)
            gc = np.zeros((H // 4, W // 4, 3), np.float32)
            for i, (x, y, r, I, cr, cg, cb) in enumerate(self.lights):
                sx, sy, sc = E.layer_point(self.ref, cam, t, x, y)
                fl = 0.18 * E.noise1(t, 60 + i, 3.0) + 0.08 * E.noise1(t, 80 + i, 9.0)
                m = np.zeros((H // 4, W // 4), np.float32)
                cv2.circle(m, (int(sx / 4 * 16), int(sy / 4 * 16)), max(1, int(r * sc * 0.25 * 16)), float(min(I, 1.6) * 0.35), -1, cv2.LINE_AA, 4)
                gc += m[..., None] * (0.25 + fl) * np.array([cr, cg, cb], np.float32)
            gc = cv2.GaussianBlur(cv2.resize(gc, (W, H)), (0, 0), 28)
            img += gc
        for (x, y, s, seed) in self.flames:
            sx, sy, sc = self.screen(cam, t, x, y)
            E.add_flame(img, sx, sy, sc * s, t, seed=seed, glow=1.0, size=1.0)
        if self.embers:
            ember_draw(img, self, cam, t, **self.embers)
        if self.rain:
            for rr in (self.rain if isinstance(self.rain, (list, tuple)) else [self.rain]):
                E.rain(img, t, **rr)
        if self.live:
            img = self.live(self, img, t, cam)
        if self.grade:
            img = self.grade(img, t)
        return img


def ember_draw(img, look, cam, t, x, y, n=60, spread=30, rise=380, seed=0, life=2.4, col=(1.0, 0.55, 0.2), gain=1.0):
    """Sparks rising from a fire at design point (x, y), drifting and dying."""
    sx, sy, sc = look.screen(cam, t, x, y)
    r = np.random.default_rng(seed)
    ph = r.uniform(0, life, n); dx = r.normal(0, spread, n); sw = r.uniform(0.5, 2.0, n); sz = r.uniform(1.0, 2.6, n)
    buf = np.zeros((H // 2, W // 2), np.float32)
    for i in range(n):
        a = np.mod(t + ph[i], life) / life
        px = sx + (dx[i] * a + 18 * math.sin(t * sw[i] + i)) * sc * 1.5
        py = sy - rise * a * sc * 1.5
        b = (1 - a) ** 1.5 * (0.5 + 0.5 * math.sin(t * 9 * sw[i] + i)) * gain
        if 0 <= px < W and 0 <= py < H and b > 0.02:
            cv2.circle(buf, (int(px / 2 * 16), int(py / 2 * 16)), int(max(0.6, sz[i] * sc) * 16), float(b), -1, cv2.LINE_AA, 4)
    buf = cv2.resize(cv2.GaussianBlur(buf, (0, 0), 0.7), (W, H))
    img += buf[..., None] * np.array(col, np.float32) * 1.6
    return img


class Cell:
    """A page written by candlelight on the Bamberg desk: a wide plate and a macro plate of the desk, blended by zoom
    (as in Bamberg v3), so close framings on the writing stay sharp and wider ones never run off the plate."""
    MACRO = dict(zoom=2.5, center=(700, 1800))

    def __init__(self, page, quill_until=None, gutter=None):
        import shot_cell as SC
        self.base = SC.CellShot('tall', 19.0, page, quill_until=quill_until, gutter=gutter)
        self.mac = SC.CellShot('tall', 19.0, page, quill_until=quill_until, gutter=gutter, **self.MACRO)

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
            return self.base.render(t, cam, frame, rain=False)[0]
        mm = self.macro_mask(cam, t)
        if k >= 1.0 and mm.min() > 0.999:
            return self.mac.render(t, cam, frame, rain=False)[0]
        a = self.mac.render(t, cam, frame, rain=False)[0]
        b = self.base.render(t, cam, frame, rain=False)[0]
        m = mm * k
        return a * m[..., None] + b * (1 - m[..., None])


class Black:
    def render(self, t, cam, frame):
        return np.zeros((H, W, 3), np.float32)


# ------------------------------------------------------------------ shots
class Shot:
    def __init__(self, name, t0, t1, make, keys, xin=0.8, xout=0.8, grade=None, PWc=1620, ap=0.0, focus=1.0, hand=1.0,
                 shake=None, roll=0.0, key=None):
        self.name, self.t0, self.t1, self.make, self.keys = name, t0, t1, make, keys
        self.roll, self.key = roll, key or name
        self.xin, self.xout, self.grade, self.PWc, self.ap, self.focus, self.hand = xin, xout, grade or {}, PWc, ap, focus, hand
        self.shake = shake
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
        return ob(self).render(t, self.cam(t), frame)


_SCENES = {}


def scene(key, make):
    if key not in _SCENES:
        _SCENES[key] = make()
    return _SCENES[key]


def ob(s):
    if s.obj is None:
        s.obj = scene(s.key, s.make)
    return s.obj


FLASH = []
CUT = dict(xin=0.0, xout=0.0)
SHOTS = None


def shots():
    global SHOTS
    if SHOTS is None:
        FLASH.clear()
        SHOTS = C['build']()
    return SHOTS


# ------------------------------------------------------------------ captions, labels, cards
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
    for ft, k, col in FLASH:
        if ft <= t < ft + 0.35:
            d = math.exp(-(t - ft) * 14.0) * k
            img = img * (1 + d) + d * 0.25 * np.array(col, np.float32)
    return img


DOC = dict(PG.CLERK, size=64)
DOC_Y = 560
CINZEL, ITAL, ROMAN = 'Cinzel[wght].ttf', 'Newsreader-Italic[opsz,wght].ttf', 'Newsreader[opsz,wght].ttf'


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
    for a, b, lines, y, size, fn in C['labels']():
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
                rgb, al = text(lines[1:], ITAL, int(size * 1.05), col=(0.9, 0.87, 0.8), spacing=1.15)
                E.put(img, rgb, al, W / 2, y + size * 1.15 + 20 * (len(lines) - 1), opacity=op * 0.95, shadow=0.95)
    # title card after the opening promise
    first = ORDER[3] if len(ORDER) > 3 else ORDER[-1]
    ta = V['o3'][1] + 0.35
    if ta < t < V[first][0] - 0.3:
        u = t - ta; dur = V[first][0] - 0.3 - ta
        op = min(1.0, u / 0.5, (dur - u) / 0.5)
        series, tl = C['title']
        rgb, al = text([series], CINZEL, 36, col=(0.86, 0.72, 0.5), tracking=10)
        E.put(img, rgb, al, W / 2, 760, opacity=op * 0.9, glow=0.25)
        rgb, al = text(tl, ITAL, 84, spacing=1.08)
        E.put(img, rgb, al, W / 2, 920, opacity=op, shadow=0.9, glow=0.18)
    # end card
    ea = V[ORDER[-1]][1] + 1.3
    if t > ea:
        op = min(1.0, (t - ea) / 0.6)
        rgb, al = text(['DARK CORNERS'], CINZEL, 44, col=(0.86, 0.72, 0.5), tracking=11)
        E.put(img, rgb, al, W / 2, 820, opacity=op, glow=0.3)
        for lines, fn, size, col, y in C['end']:
            rgb, al = text(lines, fn, size, col=col, spacing=1.3)
            E.put(img, rgb, al, W / 2, y, opacity=op * 0.95)
    return img


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
            ob(s)
            s.keys(s) if callable(s.keys) else None


def frames_main(a, b, out):
    import multiprocessing as mp
    b = min(b, NF)
    n = int(os.environ.get('FILM_WORKERS', '2'))
    n = max(1, min(n, b - a))
    chunks = [(i, list(range(a + (b - a) * i // n, a + (b - a) * (i + 1) // n)), f'{out}.part{i}.mp4') for i in range(n)]
    ctx = mp.get_context('spawn')
    pre = ctx.Process(target=prebuild, args=(a, b))
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


def main(argv):
    what = argv[1] if len(argv) > 1 else 'info'
    if what == 'info':
        for lid in ORDER:
            print(lid, round(V[lid][0], 2), round(V[lid][1], 2))
        print('total', round(TOTAL, 2), 'frames', NF)
        for s in shots():
            print(f'{s.name:16s} {s.t0:7.2f} {s.t1:7.2f}')
    elif what == 'still':
        for tt in argv[2].split(','):
            t = float(tt)
            img = render_frame(int(round(t * FPS)))
            out = argv[3] if ',' not in argv[2] else argv[3].replace('.jpg', f'_{tt}.jpg')
            cv2.imwrite(out, (img[..., ::-1] * 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 88])
    elif what == 'frames':
        frames_main(int(argv[2]), int(argv[3]), argv[4])
