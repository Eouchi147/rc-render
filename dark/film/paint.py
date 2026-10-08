"""Candlelit Oil painter for film plates (the look Sam approved in the look test, ported from styles2.style_oil).

paint(rgb, alpha=None, scale=1.0, seed=0) -> (rgb, alpha, height)
  rgb    float32 HxWx3 in 0..1, the lit reference render of one plate layer
  alpha  float32 HxW coverage (None = opaque plate)
  scale  plate pixels per frame pixel (1080-wide frame = 1.0); stroke sizes follow it
Strokes run along the structure-tensor flow of the image (and of the silhouette, for layers),
coarse to fine (Hertzmann), each stroke also painting the layer's alpha, so edges are brushy, not cut out.
The height map (impasto) is returned so the compositor can light the paint relief."""
import math
import numpy as np
import cv2
from numba import njit

RADII = (18, 10, 5, 3)          # frame pixels at 1080 wide


def luminance(img):
    return img[..., 0] * 0.2126 + img[..., 1] * 0.7152 + img[..., 2] * 0.0722


def bleed(rgb, a, levels=7):
    """Fill the uncovered area with the nearest covered colours (push-pull), so edge strokes keep the layer's palette."""
    ca = rgb * a[..., None]
    num, den = ca.copy(), a.copy()
    for lv in range(levels):
        s = 2 ** lv * 1.5
        c = cv2.GaussianBlur(ca, (0, 0), s)
        w = cv2.GaussianBlur(a, (0, 0), s)
        est = c / np.maximum(w, 1e-6)[..., None]
        wt = np.clip(w * 4, 0, 1) * np.clip(1 - den, 0, 1)
        num += est * wt[..., None]
        den += wt
    mean = ca.reshape(-1, 3).sum(0) / max(float(a.sum()), 1e-6)
    left = np.clip(1 - den, 0, 1)
    num += mean[None, None] * left[..., None]; den += left
    return (num / np.maximum(den, 1e-6)[..., None]).astype(np.float32)


@njit(cache=True)
def _paths(cys, cxs, blur, ab, theta, R, L, flips, cthr, athr):
    H, W = theta.shape
    n = cys.shape[0]
    pts = np.zeros((n * (L + 1), 2), np.float32)
    off = np.zeros(n + 1, np.int64)
    k = 0
    for i in range(n):
        cy, cx = cys[i], cxs[i]
        c0 = blur[cy, cx, 0]; c1 = blur[cy, cx, 1]; c2 = blur[cy, cx, 2]
        a0 = ab[cy, cx]
        x = float(cx); y = float(cy)
        pts[k, 0] = x; pts[k, 1] = y; k += 1
        th0 = theta[cy, cx]
        dx = math.cos(th0); dy = math.sin(th0)
        if flips[i]:
            dx = -dx; dy = -dy
        for step in range(L):
            x = x + dx * R * 0.9
            y = y + dy * R * 0.9
            xi = int(min(max(x, 0.0), W - 1.0)); yi = int(min(max(y, 0.0), H - 1.0))
            pts[k, 0] = x; pts[k, 1] = y; k += 1
            if step > 0:
                d = abs(blur[yi, xi, 0] - c0) + abs(blur[yi, xi, 1] - c1) + abs(blur[yi, xi, 2] - c2)
                if d > cthr or abs(ab[yi, xi] - a0) > athr:
                    break
            th = theta[yi, xi]
            nx = math.cos(th); ny = math.sin(th)
            if nx * dx + ny * dy < 0:
                nx = -nx; ny = -ny
            dx = 0.55 * nx + 0.45 * dx; dy = 0.55 * ny + 0.45 * dy
            nn = math.hypot(dx, dy) + 1e-9
            dx /= nn; dy /= nn
        off[i + 1] = k
    return pts[:k], off


def _cells(diff, R, thr, mask=None):
    H, W = diff.shape
    Rc = max(1, int(round(R)))
    hh, ww = (H // Rc) * Rc, (W // Rc) * Rc
    out = []
    # full cells (vectorised): argmax and mean per cell
    d = diff[:hh, :ww].reshape(hh // Rc, Rc, ww // Rc, Rc).transpose(0, 2, 1, 3).reshape(hh // Rc, ww // Rc, Rc * Rc)
    mean = d.mean(2)
    am = d.argmax(2)
    gy, gx = np.mgrid[0:hh // Rc, 0:ww // Rc]
    cy = gy * Rc + am // Rc
    cx = gx * Rc + am % Rc
    ok = mean > thr
    if mask is not None:
        mk = mask[:hh, :ww].reshape(hh // Rc, Rc, ww // Rc, Rc).max(axis=(1, 3))
        ok &= mk > 0
    return cy[ok].astype(np.int64), cx[ok].astype(np.int64)


def paint(rgb, alpha=None, scale=1.0, seed=0, radii=RADII, flat_angle=8.0, detail=1.0, grade=True):
    rgb = np.clip(rgb.astype(np.float32), 0, 1)
    H, W = rgb.shape[:2]
    r = np.random.default_rng(seed)
    if grade:   # the look test's grade: teal shadows, warm lights ('warm': only the warm lights, for interiors)
        lumr = luminance(rgb)[..., None]
        cool = 0.0 if grade == 'warm' else 1.2
        rgb = np.clip(rgb + (1 - lumr) * np.array([-0.02, 0.01, 0.04], np.float32) * cool
                      + lumr * np.array([0.04, 0.01, -0.03], np.float32), 0, 1)
    opaque = alpha is None
    a = np.ones((H, W), np.float32) if opaque else np.clip(alpha.astype(np.float32), 0, 1)
    ref = rgb if opaque else bleed(rgb, a)
    sig = luminance(ref) + (0 if opaque else 1.2 * a)
    lb0 = cv2.GaussianBlur(sig, (0, 0), 2 * scale)
    gx = cv2.Sobel(lb0, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(lb0, cv2.CV_32F, 0, 1, ksize=3)
    Jxx, Jyy, Jxy = [cv2.GaussianBlur(v, (0, 0), 7 * scale) for v in (gx * gx, gy * gy, gx * gy)]
    theta = 0.5 * np.arctan2(2 * Jxy, Jxx - Jyy) + math.pi / 2
    coh = np.sqrt((Jxx - Jyy) ** 2 + 4 * Jxy ** 2) / (Jxx + Jyy + 1e-6)
    noise = cv2.resize(r.random((max(2, H // 60), max(2, W // 60))).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    theta = np.where(coh < 0.25, np.radians(flat_angle) + (noise - 0.5) * 0.8, theta).astype(np.float32)
    canvas = np.empty_like(ref); canvas[:] = np.array([0.25, 0.17, 0.11], np.float32)
    acan = np.zeros((H, W), np.float32)
    height = np.zeros((H, W), np.float32)
    region = None if opaque else (cv2.dilate((a > 0.01).astype(np.uint8), np.ones((5, 5), np.uint8)))
    for li, R0 in enumerate(radii):
        R = max(1.0, R0 * scale)
        blur = cv2.GaussianBlur(ref, (0, 0), R * 0.55)
        ab = cv2.GaussianBlur(a, (0, 0), R * 0.55) if not opaque else a
        diff = np.abs(canvas - blur).sum(2)
        if not opaque:
            diff = diff * np.clip(ab * 3, 0, 1) + np.abs(acan - ab) * 2
        thr = -1 if li == 0 else (0.07 if R0 > 3 else 0.1) / detail
        cy, cx = _cells(diff, R, thr, region)
        if len(cy) == 0:
            continue
        o = r.permutation(len(cy)); cy, cx = cy[o], cx[o]
        L = 9 if R0 > 6 else (6 if R0 > 3 else 4)
        flips = r.random(len(cy)) < 0.5
        pts, off = _paths(cy, cx, blur, ab, theta, float(R), L, flips, 0.18, 0.3)
        jit = (1 + r.normal(0, 0.035, (len(cy), 1)) + r.normal(0, 0.008, (len(cy), 3))).astype(np.float32)
        cols = blur[cy, cx] * jit
        avals = ab[cy, cx]
        hv = 0.5 + 0.5 * r.random(len(cy))
        th_ = max(1, int(R * 1.25))
        P = (pts * 16).astype(np.int32)
        for i in range(len(cy)):
            q = P[off[i]:off[i + 1]]
            c = cols[i]
            cv2.polylines(canvas, [q], False, (float(c[0]), float(c[1]), float(c[2])), th_, cv2.LINE_AA, 4)
            if not opaque:
                cv2.polylines(acan, [q], False, float(avals[i]), th_, cv2.LINE_AA, 4)
            cv2.polylines(height, [q], False, float(hv[i]), max(1, th_ - 1), cv2.LINE_AA, 4)
    hb = cv2.GaussianBlur(height, (0, 0), 0.7 * max(scale, 0.6))
    hn = cv2.resize(r.random((max(2, int(H / 1.4)), max(2, int(W / 1.4)))).astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)
    hb = hb + hn * 0.18
    em = cv2.Sobel(hb, cv2.CV_32F, 1, 0, ksize=3) * -0.5 + cv2.Sobel(hb, cv2.CV_32F, 0, 1, ksize=3) * -0.5
    canvas = canvas * (1 + np.clip(em, -0.4, 0.4)[..., None] * 0.4)
    if opaque:
        acan = np.ones((H, W), np.float32)
    else:
        acan = np.clip(acan, 0, 1)
    return np.clip(canvas, 0, 1.5).astype(np.float32), acan.astype(np.float32), hb.astype(np.float32)
