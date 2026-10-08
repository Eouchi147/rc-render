"""A goose quill, cut to a nib, lit from behind by the candle. Sprite in its own pixels, with the nib position.
The shaft runs from the nib towards the bottom right of the frame (back towards the writer, who is off screen)."""
import math
import numpy as np
import cv2
import shade as S

QW, QH = 900, 900
NIB = (60.0, 60.0)


def build(seed=7, length=980.0, angle=-0.72, curve=0.11):
    """angle: direction from the nib to the tail (radians, screen space: 0 = right, positive = down)."""
    h, w = QH, QW
    r = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nib = np.array(NIB, np.float64)
    d = np.array([math.cos(-angle), math.sin(-angle)])     # towards the tail (down-right)
    d = np.array([abs(d[0]), abs(d[1])]); d /= np.linalg.norm(d)
    n = np.array([-d[1], d[0]])
    # a gently curved spine
    ts = np.linspace(0, 1, 200)
    spine = np.array([nib + d * (t * length) + n * (curve * length * (t ** 2)) for t in ts])
    # shaft width: thin at the nib, thicker (calamus) then tapering into the rachis
    def width(t):
        return 2.2 + 7.5 * min(1, t / 0.08) - 3.5 * max(0, (t - 0.3) / 0.7)
    left = np.array([p + n * width(t) / 2 for p, t in zip(spine, ts)])
    right = np.array([p - n * width(t) / 2 for p, t in zip(spine, ts)])
    m_shaft = S.poly_mask(h, w, np.vstack([left, right[::-1]]))
    # vane: starts a third of the way up, asymmetric (narrow leading edge, broad trailing edge)
    vl, vr = [], []
    for p, t in zip(spine, ts):
        if t < 0.3:
            continue
        u = (t - 0.3) / 0.7
        prof = math.sin(math.pi * min(1.0, u * 1.08)) ** 0.55
        wl = (26 + 18 * u) * prof * (1 + 0.06 * r.normal())
        wr_ = (52 + 22 * u) * prof * (1 + 0.06 * r.normal())
        if r.random() < 0.05:
            wr_ *= 0.75                                      # a split in the vane
        vl.append(p + n * wl)
        vr.append(p - n * wr_)
    m_vane = S.poly_mask(h, w, np.vstack([np.array(vl), np.array(vr)[::-1]]))
    # barbs: fine striations angled towards the tip
    along = (xx - nib[0]) * d[0] + (yy - nib[1]) * d[1]
    across = (xx - nib[0]) * n[0] + (yy - nib[1]) * n[1]
    barb = 0.5 + 0.5 * np.sin((along * 0.55 + np.abs(across) * 1.25) * 1.3 + S.fbm(h, w, 14, 3, seed) * 5)
    side = np.clip(0.5 + across / 70.0, 0, 1)                # the light comes from the upper side
    vane_col = np.array([0.74, 0.66, 0.55], np.float32)
    mott = S.fbm(h, w, 40, 4, seed + 2)
    vane = vane_col[None, None] * (0.5 + 0.3 * barb + 0.3 * mott)[..., None] * (0.2 + 0.8 * side)[..., None]
    edge_glow = np.clip(1 - np.abs(np.abs(across) - 40) / 30, 0, 1) * 0.0
    rgb = vane + edge_glow[..., None]
    a = m_vane * (0.78 + 0.22 * barb)
    # translucent rim where the candle shines through the vane
    rim = np.clip(cv2.GaussianBlur(m_vane, (0, 0), 3) - cv2.erode(m_vane, np.ones((7, 7), np.uint8)), 0, 1)
    rgb += (rim * side * 0.6)[..., None] * np.array([1.0, 0.72, 0.4], np.float32)
    # shaft: horn-coloured, a highlight down one side
    sh_u = np.clip(0.5 + across / 5.0, 0, 1)
    shaft = np.array([0.72, 0.62, 0.46], np.float32)[None, None] * (0.35 + 0.7 * sh_u)[..., None]
    rgb = rgb * (1 - m_shaft[..., None]) + shaft * m_shaft[..., None]
    a = np.maximum(a, m_shaft)
    # inked nib
    tip = np.clip(1 - along / 38.0, 0, 1) * m_shaft
    rgb = rgb * (1 - tip[..., None]) + np.array([0.02, 0.02, 0.03], np.float32) * tip[..., None]
    return rgb.astype(np.float32), np.clip(a, 0, 1).astype(np.float32), NIB


def bandage(h=420, w=520, seed=9):
    """A bandaged fingertip edge (out-of-focus foreground element): linen strip with a dried blood stain."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    shape = S.catmull([(0, 140), (120, 90), (260, 70), (420, 110), (520, 190), (520, 420), (0, 420)], 12)
    m = S.poly_mask(h, w, shape)
    al, hg = S.cloth(h, w, seed, col=(0.78, 0.72, 0.6), fold_cell=40, folds=8)
    hh = S.inflate(m, 120, 0.5) + hg * 0.2
    n = S.normals(hh, strength=60)
    lit = np.clip(n[..., 0] * 0.4 + n[..., 1] * -0.6 + n[..., 2] * 0.5, 0, 1)
    stain = np.clip(S.fbm(h, w, 60, 4, seed + 3) * 1.8 - 0.95, 0, 1) * np.exp(-((xx - 160) / 140) ** 2 - ((yy - 140) / 90) ** 2)
    col = al * (0.15 + 0.9 * lit)[..., None]
    col = col * (1 - stain[..., None] * 0.8) + np.array([0.3, 0.09, 0.06], np.float32) * stain[..., None] * 0.8
    return col.astype(np.float32), m
