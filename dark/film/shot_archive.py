"""The archive shots: the two records side by side (cold open), and the file closing over the letter (coda)."""
import math
import numpy as np
import cv2
import engine as E
import archive as A
import plates as PL
import pages as PG
import hand

INK_OLD = np.array([0.20, 0.12, 0.07], np.float32)      # iron-gall ink, browned with age
INK_REC = np.array([0.10, 0.08, 0.07], np.float32)


def prepare(zoom=1.0, center=None, force=False):
    name = 'archive' + ('' if zoom == 1.0 else f'_z{zoom:g}_{int(center[0])}_{int(center[1])}')
    z = None if force else PL.load(name)
    if z is not None:
        return z
    L = A.build(zoom, center)
    sc = 1.5 * zoom / (1.0 if zoom == 1.0 else 1.7)
    img, _ = PL.paint_layer(L['img'], None, sc, seed=21, grade='warm', expo=1.9)
    PL.save(name, img=img, letter_H=L['letter_H'], rec_l_H=L['rec_l_H'], rec_r_H=L['rec_r_H'])
    return PL.load(name)


class ArchiveShot:
    def __init__(self, zoom=1.0, center=None):
        self.z = prepare(zoom, center)
        self.zoom = zoom
        P = PG.pages_for_film()
        self.sheets = [(self.z['letter_H'], [P['p1_full'], P['p1_margin']], INK_OLD),
                       (self.z['rec_l_H'], [P['record']], INK_REC),
                       (self.z['rec_r_H'], [P['record2']], INK_REC)]
        self.ink = []
        for Hs, maps, col in self.sheets:
            cov = np.zeros((PG.PHEI, PG.PWID), np.float32)
            for m in maps:
                s, _ = hand.at_time(m['cov'], m['dark'], m['tmap'], 1e6)
                cov = np.maximum(cov, s)
            self.ink.append(cov)
        img = self.z['img'].copy()
        for (Hs, maps, col), cov in zip(self.sheets, self.ink):
            cw = cv2.warpPerspective(cov, Hs.astype(np.float64), (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR)
            lum = img.mean(-1, keepdims=True)
            img = img * (1 - cw[..., None] * 0.85) + col * (0.5 + 0.9 * lum) * cw[..., None] * 0.85
        if zoom == 1.0:
            anchor = (A.PW / 2.0, A.PH / 2.0)
        else:
            anchor = (A.PW / 2.0 + zoom * (A.PW / 2.0 - center[0]), A.PH / 2.0 + zoom * (A.PH / 2.0 - center[1]))
        self.layer = E.Layer(img, None, Z=1.0, d=A.DENS * zoom, anchor=anchor, name='archive')
        lp, _ = (A.BASE_CAM if zoom == 1.0 else A.BASE_CAM.zoomed(zoom, center)).project([A.LIGHT])
        self.light_plate = lp[0]
        self.dust = E.Particles(320, ((-600, 600), (-1100, 500), (0.8, 1.2)), seed=4, vel=(3, 5, 0), jitter=12,
                                size=(1.0, 3.0), col=(1.0, 0.85, 0.62), bright=0.55)

    def render(self, t, cam, frame):
        img = E.compose([self.layer], cam, t)
        # a beam of light falling through the dust from above
        yy, xx = np.mgrid[0:E.H:4, 0:E.W:4].astype(np.float32)
        lx, ly, sc = E.layer_point(self.layer, cam, t, *self.light_plate)
        beam = np.exp(-(((xx - lx) / (520 * sc)) ** 2 + ((yy - ly) / (900 * sc)) ** 2))
        beam = cv2.resize(beam.astype(np.float32), (E.W, E.H))
        img += (beam * 0.035)[..., None] * np.array([1.0, 0.82, 0.6], np.float32)
        self.dust.draw(img, cam, t, light=beam, gain=1.0)
        return img
