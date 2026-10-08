"""A real 3D pinhole for laying out plates: world in centimetres, projected to plate pixels; planes map by homography."""
import numpy as np
import cv2


def _n(v):
    v = np.asarray(v, np.float64)
    return v / np.linalg.norm(v)


class Cam3:
    def __init__(self, pos, target, fpx, W, H, up=(0, 0, 1)):
        self.pos = np.asarray(pos, np.float64)
        f = _n(np.asarray(target, np.float64) - self.pos)
        r = _n(np.cross(f, up))
        u = np.cross(r, f)
        self.R = np.stack([r, -u, f])
        self.fpx, self.cx, self.cy, self.W, self.H = fpx, W / 2.0, H / 2.0, W, H

    def zoomed(self, zoom, center):
        """The same camera with a longer lens, re-centred so the plate pixel `center` sits at the middle."""
        c = Cam3.__new__(Cam3)
        c.pos, c.R, c.W, c.H = self.pos, self.R, self.W, self.H
        c.fpx = self.fpx * zoom
        c.cx = self.W / 2.0 - zoom * (center[0] - self.cx)
        c.cy = self.H / 2.0 - zoom * (center[1] - self.cy)
        return c

    def project(self, P):
        P = np.asarray(P, np.float64)
        q = (P - self.pos) @ self.R.T
        x = self.cx + self.fpx * q[..., 0] / q[..., 2]
        y = self.cy + self.fpx * q[..., 1] / q[..., 2]
        return np.stack([x, y], -1), q[..., 2]

    def plane_H(self, world4, flat4):
        """Homography from flat texture pixels (4 points) to plate pixels, for 4 world points on a plane."""
        p, _ = self.project(world4)
        return cv2.getPerspectiveTransform(np.asarray(flat4, np.float32), p.astype(np.float32))

    def depth(self, P):
        return self.project(P)[1]
