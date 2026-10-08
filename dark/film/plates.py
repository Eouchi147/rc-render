"""Painting and caching of plate layers (float16 .npz on disk)."""
from darkroot import ROOT
import os
import numpy as np
import cv2
import paint

DIR = ROOT + '/film/plates/'
os.makedirs(DIR, exist_ok=True)


def to_display(x, expo=1.7, gamma=1.25):
    return np.clip(1 - np.exp(-np.maximum(x, 0) * expo), 0, 1) ** (1 / gamma)


def paint_layer(rgb, alpha=None, scale=1.5, seed=0, expo=1.7, gamma=1.25, display=False, detail=1.0, grade=True):
    d = rgb if display else to_display(rgb, expo, gamma)
    if alpha is not None:
        ys, xs = np.nonzero(alpha > 0.003)
        if len(ys) == 0:
            return d.astype(np.float32), alpha.astype(np.float32)
        pad = int(40 * scale)
        y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, alpha.shape[0])
        x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, alpha.shape[1])
        pr, pa, _ = paint.paint(d[y0:y1, x0:x1], alpha[y0:y1, x0:x1], scale=scale, seed=seed, detail=detail, grade=grade)
        out = np.zeros_like(d); oa = np.zeros_like(alpha)
        out[y0:y1, x0:x1] = pr; oa[y0:y1, x0:x1] = pa
        return out.astype(np.float32), oa.astype(np.float32)
    pr, pa, _ = paint.paint(d, None, scale=scale, seed=seed, detail=detail, grade=grade)
    return pr.astype(np.float32), None


def save(name, **arrs):
    tmp = DIR + name + f'.npz.{os.getpid()}.part'          # write, then rename: an interrupted run never leaves a broken cache file
    with open(tmp, 'wb') as f:
        np.savez(f, **{k: (v.astype(np.float16) if isinstance(v, np.ndarray) and v.dtype != np.float64 else v)
                       for k, v in arrs.items()})
    os.replace(tmp, DIR + name + '.npz')


def load(name):
    p = DIR + name + '.npz'
    if not os.path.exists(p):
        return None
    z = np.load(p, allow_pickle=True)
    return {k: (z[k].astype(np.float32) if z[k].dtype == np.float16 else z[k]) for k in z.files}
