"""Junius's writing hand, seen from the desk's near edge: shirt sleeve, a bandaged thumb and fingers, a goose quill.
Built from inflated parts (each part a small relief), lit from behind by the candle (rim light) and faintly by the room.
Returns RGBA in sprite pixels plus the nib position, so the nib can be placed exactly on the moving pen point."""
import math
import numpy as np
import cv2
import shade as S

SW, SH = 760, 760
NIB = (96.0, 92.0)


def _part(mask, rad, power=0.6):
    return S.inflate(mask, rad, power)


def _lit(mask, hgt, base, L, rim=1.0, amb=0.05, spec=0.0, sss=None, strength=40.0):
    n = S.normals(hgt, strength=strength)
    lx, ly, lz = L
    ln = math.sqrt(lx * lx + ly * ly + lz * lz)
    ndl = np.clip((n[..., 0] * lx + n[..., 1] * ly + n[..., 2] * lz) / ln, 0, 1)
    # rim: surfaces turning away from the camera on the light side
    edge = np.clip(1 - n[..., 2], 0, 1) ** 1.5
    side = np.clip((n[..., 0] * lx + n[..., 1] * ly) / (math.hypot(lx, ly) + 1e-6), 0, 1)
    col = np.array(base, np.float32)
    out = col * (amb + 0.9 * ndl[..., None]) + (edge * side * rim)[..., None] * np.array([1.0, 0.72, 0.45], np.float32)
    if sss is not None:
        out += (edge * (1 - side) * 0.15)[..., None] * np.array(sss, np.float32)
    if spec:
        hx, hy, hz = lx / ln, ly / ln, lz / ln + 1
        hn = math.sqrt(hx * hx + hy * hy + hz * hz)
        out += ((np.clip((n[..., 0] * hx + n[..., 1] * hy + n[..., 2] * hz) / hn, 0, 1) ** 20) * spec)[..., None]
    return out


def build(seed=3, light=(0.55, -0.75, 0.55), warmth=1.0):
    h, w = SH, SW
    r = np.random.default_rng(seed)
    rgb = np.zeros((h, w, 3), np.float32)
    a = np.zeros((h, w), np.float32)
    L = light
    skin = np.array([0.62, 0.42, 0.32], np.float32) * 0.9
    linen = np.array([0.72, 0.68, 0.6], np.float32)
    band = np.array([0.80, 0.74, 0.62], np.float32)

    def lay(m, col_img):
        nonlocal rgb, a
        rgb = rgb * (1 - m[..., None]) + col_img * m[..., None]
        a = np.maximum(a, m)

    # ---- the quill shaft and vane (drawn first: the fingers close over it)
    nib = np.array(NIB)
    tail = np.array([700.0, 610.0])
    d = (tail - nib) / np.linalg.norm(tail - nib)
    nrm = np.array([-d[1], d[0]])
    shaft = [nib - nrm * 2.0, nib + nrm * 2.0, tail + nrm * 5, tail - nrm * 5]
    m_sh = S.poly_mask(h, w, shaft)
    vane_pts = []
    v0 = nib + d * 300
    for t_ in np.linspace(0, 1, 40):
        p = v0 + d * (t_ * 360)
        wv = 34 * math.sin(math.pi * min(1, t_ * 1.15)) ** 0.7 + 4
        vane_pts.append(p + nrm * wv * (1 + 0.08 * r.normal()))
    for t_ in np.linspace(1, 0, 40):
        p = v0 + d * (t_ * 360)
        wv = 22 * math.sin(math.pi * min(1, t_ * 1.15)) ** 0.7 + 3
        vane_pts.append(p - nrm * wv * (1 + 0.08 * r.normal()))
    m_v = S.poly_mask(h, w, vane_pts)
    # barbs: fine diagonal striations
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    along = (xx - v0[0]) * d[0] + (yy - v0[1]) * d[1]
    across = (xx - v0[0]) * nrm[0] + (yy - v0[1]) * nrm[1]
    barbs = 0.5 + 0.5 * np.sin((along * 0.8 - np.abs(across) * 1.6) * 1.1 + S.fbm(h, w, 12, 2, seed + 4) * 4)
    vane = np.array([0.82, 0.8, 0.76], np.float32)[None, None] * (0.55 + 0.45 * barbs)[..., None]
    lit_v = 0.25 + 0.9 * np.clip(0.5 + across / 60.0 * 0.6, 0, 1)
    lay(m_v * 0.92, vane * lit_v[..., None])
    sh_col = np.array([0.85, 0.8, 0.68], np.float32) * (0.5 + 0.5 * np.clip(0.5 + across / 4.0, 0, 1))[..., None]
    lay(m_sh, sh_col)
    # ink on the nib
    m_nib = S.poly_mask(h, w, [nib - nrm * 2.2, nib + nrm * 2.2, nib + d * 28 + nrm * 3, nib + d * 28 - nrm * 3])
    lay(m_nib, np.zeros((h, w, 3), np.float32) + 0.03)

    # ---- sleeve (linen shirt, rolled), from the bottom right
    sl = S.catmull([(760, 470), (610, 420), (520, 470), (470, 560), (470, 690), (560, 770), (780, 790), (800, 600)], 10)
    m_s = S.poly_mask(h, w, sl)
    al, hg = S.cloth(h, w, seed + 10, col=tuple(linen), fold_cell=55, folds=7)
    hs = _part(m_s, 90, 0.5) * 0.7 + hg * 0.3 * m_s
    lay(m_s, al * _lit(m_s, hs, (1, 1, 1), L, rim=0.9, amb=0.08, strength=60))
    # ---- back of the hand and wrist
    back = S.catmull([(500, 460), (420, 400), (330, 330), (262, 262), (232, 222), (262, 196), (320, 196), (380, 230),
                      (450, 300), (520, 370), (548, 420)], 10)
    m_b = S.poly_mask(h, w, back)
    hb = _part(m_b, 80, 0.55)
    knuckles = np.zeros((h, w), np.float32)
    for kx, ky in [(262, 214), (292, 205), (322, 210), (350, 226)]:
        knuckles += np.exp(-(((xx - kx) / 16) ** 2 + ((yy - ky) / 14) ** 2)) * 0.25
    hb = hb + knuckles * m_b
    tend = np.zeros((h, w), np.float32)
    for kx, ky in [(262, 214), (292, 205), (322, 210), (350, 226)]:
        pass
    lay(m_b, _lit(m_b, hb, skin, L, rim=1.1, amb=0.06, sss=(0.9, 0.25, 0.15), strength=55))
    # ---- curled middle, ring and little fingers (knuckles and first joints visible)
    for i, (x0, y0, x1, y1, wd) in enumerate([(300, 214, 214, 160, 30), (330, 222, 262, 170, 28), (356, 238, 300, 196, 25)]):
        p = np.array([[x0, y0], [x1, y1]], np.float32)
        dd = (p[1] - p[0]) / np.linalg.norm(p[1] - p[0])
        nn = np.array([-dd[1], dd[0]])
        poly = S.catmull([p[0] + nn * wd / 2, p[1] + nn * wd / 2.3 + dd * 4, p[1] + dd * wd * 0.45, p[1] - nn * wd / 2.3 + dd * 4, p[0] - nn * wd / 2], 8)
        m_f = S.poly_mask(h, w, poly)
        hf = _part(m_f, wd * 0.6, 0.5)
        lay(m_f, _lit(m_f, hf, skin * (0.92 - 0.05 * i), L, rim=1.0, amb=0.05, sss=(0.9, 0.25, 0.15), strength=50))
    # ---- index finger along the quill, bent at the joints, bandaged
    idx = S.catmull([(262, 204), (232, 176), (196, 150), (160, 128), (128, 110), (110, 100), (102, 112), (118, 128),
                     (150, 148), (184, 172), (218, 200), (246, 230)], 8)
    m_i = S.poly_mask(h, w, idx)
    hi = _part(m_i, 16, 0.5)
    lay(m_i, _lit(m_i, hi, skin, L, rim=1.0, amb=0.06, sss=(0.9, 0.25, 0.15), strength=45))
    # ---- thumb (crushed: wrapped in a cloth strip), pressing the quill from the left
    th = S.catmull([(380, 330), (330, 300), (270, 262), (214, 224), (166, 186), (132, 150), (120, 130), (134, 122),
                    (166, 140), (214, 170), (270, 206), (330, 248), (392, 292)], 8)
    m_t = S.poly_mask(h, w, th)
    ht = _part(m_t, 26, 0.55)
    lay(m_t, _lit(m_t, ht, skin * 0.95, L, rim=1.0, amb=0.06, sss=(0.9, 0.25, 0.15), strength=45))
    # bandages: strips around the thumb and the index
    for (cx, cy, ang, ln, wd) in [(190, 182, -0.62, 70, 34), (236, 214, -0.68, 56, 34), (176, 140, -0.7, 52, 26)]:
        c, s = math.cos(ang), math.sin(ang)
        pts = [(cx + c * ln / 2 - s * wd / 2, cy + s * ln / 2 + c * wd / 2), (cx - c * ln / 2 - s * wd / 2, cy - s * ln / 2 + c * wd / 2),
               (cx - c * ln / 2 + s * wd / 2, cy - s * ln / 2 - c * wd / 2), (cx + c * ln / 2 + s * wd / 2, cy + s * ln / 2 - c * wd / 2)]
        m_bd = S.poly_mask(h, w, pts) * np.maximum(m_t, m_i)
        m_bd = np.clip(cv2.GaussianBlur(m_bd, (0, 0), 1.2) * 1.3, 0, 1)
        stripes = 0.5 + 0.5 * np.sin(((xx - cx) * s - (yy - cy) * c) * 0.45 + S.fbm(h, w, 9, 2, seed + int(cx)) * 3)
        stain = np.clip(S.fbm(h, w, 14, 3, seed + int(cy)) * 1.6 - 0.75, 0, 1)
        col = band[None, None] * (0.7 + 0.3 * stripes)[..., None]
        col = col * (1 - stain[..., None]) + np.array([0.35, 0.12, 0.08], np.float32) * stain[..., None]
        hbd = _part(m_bd, 14, 0.5)
        lay(m_bd, col * _lit(m_bd, hbd, (1, 1, 1), L, rim=0.8, amb=0.12, strength=40))
    # fingernail of the index, dark-rimmed (the blood ran out at the nails)
    nail = S.ellipse_pts(124, 112, 13, 8, rot=-0.62)
    m_n = S.poly_mask(h, w, nail)
    lay(m_n * 0.9, np.zeros((h, w, 3), np.float32) + np.array([0.42, 0.2, 0.16], np.float32))
    rgb *= warmth
    return rgb.astype(np.float32), np.clip(a, 0, 1).astype(np.float32), NIB
