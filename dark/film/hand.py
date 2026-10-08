"""Handwriting with a quill, written stroke by stroke.

Glyph paths come from the Hershey script fonts (public domain). The pen is simulated: a broad nib held at an angle
(thick downstrokes, hairline upstrokes), ink that runs dry between dips, a hand that trembles (Junius) or does not
(the court clerk), and a clock: every inked pixel knows the moment it was written, so a frame at time T shows exactly
what the pen has written by then, the last second of it still wet."""
import math
import numpy as np
import cv2
from HersheyFonts import HersheyFonts

_FONTS = {}


def font(name):
    if name not in _FONTS:
        f = HersheyFonts(); f.load_default_font(name); f.normalize_rendering(100)
        _FONTS[name] = f
    return _FONTS[name]


def _word_strokes(word, fname, size):
    f = font(fname)
    st = [np.array(s, np.float32) for s in f.strokes_for_text(word) if len(s) > 1]
    if not st:
        return [], size * 0.35
    k = size / 100.0
    st = [np.stack([s[:, 0] * k, (100 - s[:, 1]) * k], 1) for s in st]
    allp = np.vstack(st)
    return st, float(allp[:, 0].max())


def _resample(p, step):
    d = np.sqrt(((p[1:] - p[:-1]) ** 2).sum(1))
    s = np.concatenate([[0], np.cumsum(d)])
    if s[-1] < 1e-6:
        return p[:1].copy()
    n = max(2, int(s[-1] / step) + 1)
    t = np.linspace(0, s[-1], n)
    return np.stack([np.interp(t, s, p[:, 0]), np.interp(t, s, p[:, 1])], 1).astype(np.float32)


def _smooth(p, sig):
    if len(p) < 5 or sig <= 0:
        return p
    k = int(sig * 3) * 2 + 1
    pad = np.concatenate([np.repeat(p[:1], k // 2, 0), p, np.repeat(p[-1:], k // 2, 0)])
    g = cv2.getGaussianKernel(k, sig).ravel()
    return np.stack([np.convolve(pad[:, 0], g, 'valid'), np.convolve(pad[:, 1], g, 'valid')], 1).astype(np.float32)


def _angular(p, eps):
    """Kurrent is angular: straighten the curves of the cursive into pointed turns."""
    q = _resample(p, 0.5)
    if len(q) < 4:
        return p
    a = cv2.approxPolyDP(q.reshape(-1, 1, 2).astype(np.float32), eps, False).reshape(-1, 2)
    return a.astype(np.float32) if len(a) >= 2 else p


def layout(lines, fname='scripts', size=40, width=900, lead=1.45, slant=0.18, x0=0.0, y0=0.0, seed=0, word_gap=0.42,
           indent=0.0, xs=1.0, angular=0.0):
    """lines: list of strings (paragraphs). Returns list of words: dict(strokes=[Nx2], line=i)."""
    r = np.random.default_rng(seed)
    out = []
    y = y0
    li = 0
    for para in lines:
        x = x0 + indent
        for w in para.split():
            st, wd = _word_strokes(w, fname, size)
            if xs != 1.0:
                st = [np.stack([q[:, 0] * xs, q[:, 1]], 1) for q in st]; wd *= xs
            if angular > 0:
                st = [_angular(q, angular) for q in st]
            if x + wd > x0 + width and x > x0 + indent:
                x = x0; y += size * lead; li += 1
            base_y = y + r.normal(0, size * 0.025)
            rot = r.normal(0, 0.012)
            pts = []
            for s in st:
                q = s.copy()
                q[:, 0] -= q[:, 1] * slant * 0          # slant applied below around the baseline
                q[:, 0] = q[:, 0] + (size * 0.8 - q[:, 1]) * slant
                c, sn = math.cos(rot), math.sin(rot)
                qx, qy = q[:, 0] * c - q[:, 1] * sn, q[:, 0] * sn + q[:, 1] * c
                pts.append(np.stack([qx + x, qy + base_y], 1).astype(np.float32))
            out.append(dict(strokes=pts, line=li, word=w))
            x += wd + size * word_gap * (1 + r.normal(0, 0.12))
        y += size * lead; li += 1
    return out


def pen(words, t0, t1, tremble=0.0, nib=math.radians(35), wmax=4.0, wmin=0.7, step=0.9, seed=0, dip_every=4,
        pause_word=0.16, pause_lift=0.05, speed_var=0.25):
    """Simulate the pen over laid-out words. Returns list of segments: (pts Nx2, widths N, inks N, times N)."""
    r = np.random.default_rng(seed)
    strokes = []
    for wi, w in enumerate(words):
        for si, s in enumerate(w['strokes']):
            p = _resample(s, step)
            p = _smooth(p, 1.2)
            if tremble > 0:
                n = len(p)
                ph = r.uniform(0, 100, 4)
                u = np.arange(n) * step
                dx = (np.sin(u / 13.0 + ph[0]) * 0.6 + np.sin(u / 5.5 + ph[1]) * 0.4) * tremble
                dy = (np.sin(u / 12.4 + ph[2]) * 0.6 + np.sin(u / 6.1 + ph[3]) * 0.4) * tremble
                jit = r.normal(0, tremble * 0.25, (n, 2))
                p = p + np.stack([dx, dy], 1) + _smooth(jit, 2.0)
            strokes.append((wi, si, p.astype(np.float32)))
    # clock: arc length at a varying pen speed, plus pauses at pen lifts and between words
    seg_len = [float(np.sqrt(((p[1:] - p[:-1]) ** 2).sum(1)).sum()) if len(p) > 1 else 0.5 for _, _, p in strokes]
    pauses = []
    for k, (wi, si, p) in enumerate(strokes):
        if k == 0:
            pauses.append(0.0)
        elif si == 0:
            pauses.append(pause_word * (1 + r.normal(0, 0.3)))
        else:
            pauses.append(pause_lift * (1 + r.normal(0, 0.3)))
    speeds = np.clip(1 + r.normal(0, speed_var, len(strokes)), 0.5, 1.8)
    raw = sum(L / v for L, v in zip(seg_len, speeds)) + sum(pauses)
    budget = max(t1 - t0, 1e-3)
    pause_scale = budget / raw
    segs = []
    t = t0
    ink = 1.0
    last_word = -1
    for (wi, si, p), L, v, pz in zip(strokes, seg_len, speeds, pauses):
        t += pz * pause_scale
        if wi != last_word and wi % dip_every == 0:
            ink = 1.0
        last_word = wi
        n = len(p)
        if n < 2:
            continue
        d = np.diff(p, axis=0)
        ang = np.arctan2(d[:, 1], d[:, 0])
        ang = np.concatenate([ang, ang[-1:]])
        wid = wmin + (wmax - wmin) * np.abs(np.sin(ang - nib))
        down = np.clip(np.concatenate([d[:, 1], d[-1:, 1]]) / step, -1, 1)
        wid *= 1 + 0.18 * np.clip(down, 0, 1)
        seglen = np.concatenate([[0], np.cumsum(np.sqrt((d ** 2).sum(1)))])
        dur = (L / v) * pause_scale
        times = t + seglen / max(seglen[-1], 1e-6) * dur
        inks = np.clip(ink - seglen * 0.0012, 0.35, 1.0)
        ink = max(0.35, ink - seglen[-1] * 0.0012)
        # ink pools a little where the nib lands and lifts
        inks[:3] = np.minimum(1.0, inks[:3] + 0.15); inks[-3:] = np.minimum(1.0, inks[-3:] + 0.1)
        segs.append((p, wid.astype(np.float32), inks.astype(np.float32), times.astype(np.float32)))
        t += dur
    return segs


def rasterize(segs, H, W, ss=2, origin=(0.0, 0.0)):
    """Coverage (0..1), darkness (ink amount) and time maps of the written text, HxW."""
    cov = np.zeros((H * ss, W * ss), np.float32)
    dark = np.zeros((H * ss, W * ss), np.float32)
    tmap = np.full((H * ss, W * ss), 1e9, np.float32)
    ox, oy = origin
    for p, wid, ink, tm in segs:
        q = ((p - (ox, oy)) * ss)
        for i in range(len(q) - 1):
            a, b = q[i], q[i + 1]
            w = max(1, int(round(wid[i] * ss)))
            x0, y0 = int(a[0] * 16), int(a[1] * 16)
            x1, y1 = int(b[0] * 16), int(b[1] * 16)
            # each segment drawn into a small tile so the time/ink maps keep the earliest time
            bx0 = int(max(min(a[0], b[0]) - w - 2, 0)); by0 = int(max(min(a[1], b[1]) - w - 2, 0))
            bx1 = int(min(max(a[0], b[0]) + w + 3, W * ss)); by1 = int(min(max(a[1], b[1]) + w + 3, H * ss))
            if bx1 <= bx0 or by1 <= by0:
                continue
            tile = np.zeros((by1 - by0, bx1 - bx0), np.float32)
            cv2.line(tile, (x0 - bx0 * 16, y0 - by0 * 16), (x1 - bx0 * 16, y1 - by0 * 16), 1.0, w, cv2.LINE_AA, 4)
            sl = (slice(by0, by1), slice(bx0, bx1))
            hit = tile > 0.02
            tsub = tmap[sl]
            tsub[hit] = np.minimum(tsub[hit], tm[i])
            np.maximum(cov[sl], tile, out=cov[sl])
            dsub = dark[sl]
            dsub[hit] = np.maximum(dsub[hit], ink[i] * tile[hit])
    if ss > 1:
        cov = cv2.resize(cov, (W, H), interpolation=cv2.INTER_AREA)
        dark = cv2.resize(dark, (W, H), interpolation=cv2.INTER_AREA)
        tmap = tmap.reshape(H, ss, W, ss).min(axis=(1, 3))
    return cov, dark, tmap


def at_time(cov, dark, tmap, T, wet=0.9, soft=0.04):
    """Ink coverage at time T (what the pen has written so far) and how wet it still is."""
    shown = np.clip((T - tmap) / soft + 0.5, 0, 1) * cov
    wetness = np.clip(1 - (T - tmap) / wet, 0, 1) * (tmap <= T) * cov
    return shown * np.clip(0.55 + 0.45 * dark, 0, 1), wetness
