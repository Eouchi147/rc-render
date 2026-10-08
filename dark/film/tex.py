"""Photographic surface textures (Poly Haven, CC0): albedo, normal and height maps, tiled to any size and relit."""
from darkroot import ROOT
import numpy as np
import cv2

DIR = ROOT + '/tex/'
_C = {}


def load(name):
    if name in _C:
        return _C[name]
    d = cv2.imread(DIR + f'tex_{name}_diff.jpg', cv2.IMREAD_COLOR)
    alb = (d[..., ::-1].astype(np.float32) / 255.0) ** 2.2 if d is not None else None
    n = cv2.imread(DIR + f'tex_{name}_nor_gl.jpg', cv2.IMREAD_COLOR)
    if n is not None:
        n = n[..., ::-1].astype(np.float32) / 255.0 * 2 - 1
        n[..., 1] *= -1                      # GL (y up) to image (y down)
    h = cv2.imread(DIR + f'tex_{name}_disp.jpg', cv2.IMREAD_GRAYSCALE)
    h = h.astype(np.float32) / 255.0 if h is not None else None
    _C[name] = (alb, n, h)
    return _C[name]


def tile(img, h, w, scale=1.0, off=(0, 0), rot=0.0):
    """Sample a tiling texture into h x w; scale = texture px per output px."""
    th, tw = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    if rot:
        c, s = np.cos(rot), np.sin(rot)
        xx, yy = xx * c - yy * s, xx * s + yy * c
    mx = np.mod(xx * scale + off[0], tw).astype(np.float32)
    my = np.mod(yy * scale + off[1], th).astype(np.float32)
    return cv2.remap(img, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)


def surface(name, h, w, scale=1.0, off=(0, 0), rot=0.0, tint=None, sat=1.0, gain=1.0):
    alb, n, hg = load(name)
    A = tile(alb, h, w, scale, off, rot)
    if sat != 1.0:
        l = A.mean(axis=2, keepdims=True)
        A = np.clip(l + (A - l) * sat, 0, 1)
    if tint is not None:
        A = A * np.array(tint, np.float32)
    A = A * gain
    N = tile(n, h, w, scale, off, rot) if n is not None else None
    if N is not None:
        if rot:
            c, s = np.cos(-rot), np.sin(-rot)
            nx, ny = N[..., 0] * c - N[..., 1] * s, N[..., 0] * s + N[..., 1] * c
            N = np.stack([nx, ny, N[..., 2]], -1)
        N = N / (np.linalg.norm(N, axis=-1, keepdims=True) + 1e-6)
    Hh = tile(hg, h, w, scale, off, rot) if hg is not None else None
    return A.astype(np.float32), N, Hh


def flatten_normals(N, k):
    """Soften relief: k=0 flat, 1 as scanned."""
    out = N.copy()
    out[..., :2] *= k
    return out / (np.linalg.norm(out, axis=-1, keepdims=True) + 1e-6)
