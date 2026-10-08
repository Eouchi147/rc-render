"""The written pages: Junius's letter (24 July 1628, text after Leitschuh 1883 / Bauer 1911, public domain) and the
court record, in quill hands. Each page: ink coverage, ink amount and the time each pixel was written (global film
seconds), so the film shows exactly what the pen has written at any moment. Pre-written lines carry time -1."""
from darkroot import ROOT
import os
import pickle
import numpy as np
import hand

PWID, PHEI = 1134, 1728          # paper texture (21 x 32 cm at 54 px/cm)
CACHE = ROOT + '/film/plates/pages/'
os.makedirs(CACHE, exist_ok=True)


def _save(obj, p):
    """Write, then rename: an interrupted run never leaves a broken cache file behind."""
    with open(p + f'.{os.getpid()}.part', 'wb') as f:
        pickle.dump(obj, f)
    os.replace(p + f'.{os.getpid()}.part', p)

LETTER_P1 = ("Zu viel hundert tausend guter nacht hertzliebe dochter Veronica. "
             "Vnschuldig bin ich in das gefengnus kommen, vnschuldig bin ich gemarttert worden, vnschuldig muss ich sterben. "
             "Denn wer in das haus kompt, der muss ein Drudner werden oder wird so lange gemarttert, biss das er etwas aus "
             "seinem Kopff erdachte weiss, vnd sich erst, das got erbarme, vf etwas bedencke. Wil dir erzehlen, wie es mir "
             "ergangen ist. Als ich das erste mahl bin vf die Frag gestelt worden, war Doctor Braun, Doctor Kotzendorffer "
             "vnd die zween frembde Doctor da, da fragt mich Doctor Braun: schwager, wie kompt ir daher, Ich antwortt: durch "
             "die valsheit, vngluck. Hort, Ir, sagt er, Ir seyt ein Drutner, wolt Ir es gutwillig gestehen, wo nit, so wird "
             "man euch Zeugen herstellen vnd den Hencker an die seyten.")
MARGIN_P1 = ("Liebes Kindt 6 haben auf einmahl auf mich bekennt, als der Cantzler, sein sohn, Neudecker, Zaner, Hoffmaisters "
             "Ursel vnd Hopffen Els alle falsch aus zwang")
LETTER_P3_PRE = ("Nun folgt, hertzliebes kindt, was ich hab ausgesagt, das ich der grossen marter vnd harten tortur bin "
                 "entgangen, welche mir vnmoglich lenger also auszustehen gewesen were. Nemblich als ich anno 1624 oder 1625 "
                 "ein commission von Rottweyl gehab, hab ich dem Doctor vf die Commission in meiner Rottweylisch "
                 "Rechtfertigung vf die 600 fl. geben muss, also das ich viel ehrliche leut angesprochen, die mir ausgeholfen.")
LETTER_P3_TRUE = "Das ist alles war."
LETTER_P3_LIES = "Itzunder volgt mein aussag mit lauter lugen"
LETTER_P4_PRE = ("Hat mich wohl angesonnen allein weyle ich es nicht thun wolln, hat er mich geschlagen. Ziehet den schelm auf. "
                 "Nun, hertzliebes kindt, da hastu alle meine Aussag vnd verlauf, darauf ich sterben muss vnd seint lautter lug "
                 "vnd erdichte sach, so war mir gott helff. Kompt auch keiner heraus, wenn er gleich ein graf war. Ich hab "
                 "etliche tag an dem schreiben geschrieben; es seint meine hendt alle lam, ich bin haltd gar ubel zugericht.")
LETTER_P4_HIDE = "Liebes kindt dieses schreiben halt verborgen"
LETTER_P4_MARTYR = "das ich kein trudner sondern ein mertirer bin"
LETTER_P4_NIGHT = "Guter Nacht denn dein vatter Johannes Junius sieht dich nimmermehr."
RECORD = ("Mittwoch den 28. Junij 1628 ist Johannes Junius Burgermeister alhier ohne tortur examinirt worden, alt 55 jahr, "
          "geburtig zu Niederwaysich in der Wetterau. Sagt, er sey gantz vnschuldig, wisse von dem laster nichts, habe "
          "sein lebtag Gott nicht verleugnet. Freytag den 30. Junij. Daumenstock angelegt: empfindt keinen schmertzen. "
          "Beinschrauben: empfindt gleichfalls keinen schmertzen. Ausgezogen vnd besichtiget. Aufgezogen.")

RECORD2 = ("Ist ihm Doctor Georg Adam Haan vorgestellt worden, der sagt, er habe ihn vor anderthalb jahren bey einem "
           "Hexentantz in der Rahtstuben gesehen, alda sie gessen vnd getruncken. Beharrt Junius, er wisse nichts. Ist ihm "
           "Hopffens Elsse vorgestellt worden, sagt, sie habe ihn vf dem Hauptsmohr bey einem Hexentantz gesehen. Bleibt "
           "beim leugnen. Ist ihm bedenckzeit gegeben worden.")
JUNIUS = dict(fname='scripts', size=57, slant=0.3, xs=0.72, angular=1.5, lead=1.22, tremble=1.9, wmax=5.0, wmin=0.65)
CLERK = dict(fname='scripts', size=51, slant=0.22, xs=0.68, angular=1.0, lead=1.3, tremble=0.0, wmax=4.2, wmin=0.6)


def _layout(text, style, x0, y0, width, seed, indent=0.0):
    return hand.layout([text], style['fname'], size=style['size'], width=width, x0=x0, y0=y0, seed=seed,
                       slant=style['slant'], xs=style['xs'], angular=style['angular'], lead=style['lead'], indent=indent)


def _end_y(words, style, y0):
    if not words:
        return y0
    return y0 + (max(w['line'] for w in words) + 1) * style['size'] * style['lead']


def build_page(name, parts, style=JUNIUS, x0=87, y0=105, width=960, seed=1, force=False):
    """parts: [(text, t_start, t_end)] in order; t_start < 0 means already written. Returns ink maps and the pen path."""
    p = CACHE + name + '.pkl'
    if os.path.exists(p) and not force:
        return pickle.load(open(p, 'rb'))
    allsegs = []
    y = y0
    for i, (text, ta, tb) in enumerate(parts):
        words = _layout(text, style, x0, y, width, seed + i)
        if ta < 0:
            segs = hand.pen(words, -10.0, -9.0, tremble=style['tremble'], wmax=style['wmax'], wmin=style['wmin'], seed=seed + 10 + i)
        else:
            segs = hand.pen(words, ta, tb, tremble=style['tremble'], wmax=style['wmax'], wmin=style['wmin'], seed=seed + 10 + i)
        allsegs += segs
        y = _end_y(words, style, y) + style['size'] * 0.15
    cov, dark, tmap = hand.rasterize(allsegs, PHEI, PWID, ss=2)
    out = dict(cov=cov, dark=dark, tmap=tmap, segs=allsegs, end_y=y)
    _save(out, p)
    return out


def margin_note(name, text, x=1056, y0=1680, length=1500, seed=7, force=False):
    """The postscript written crosswise in the margin of page 1 (rotated 90 degrees, reading upwards)."""
    import cv2
    p = CACHE + name + '.pkl'
    if os.path.exists(p) and not force:
        return pickle.load(open(p, 'rb'))
    st = dict(JUNIUS); st['size'] = 39
    words = _layout(text, st, 0, 0, length, seed)
    segs = hand.pen(words, -10, -9, tremble=st['tremble'] * 0.8, wmax=3.9, wmin=0.6, seed=seed)
    # rotate: (x, y) -> (x_margin + y, y0 - x)
    rsegs = []
    for pts, wid, ink, tm in segs:
        q = np.stack([x - 60 + pts[:, 1], y0 - pts[:, 0]], 1).astype(np.float32)
        rsegs.append((q, wid, ink, tm))
    cov, dark, tmap = hand.rasterize(rsegs, PHEI, PWID, ss=2)
    out = dict(cov=cov, dark=dark, tmap=tmap, segs=rsegs)
    _save(out, p)
    return out


def pen_at(page, t):
    """Where the nib is at time t (paper pixels) and whether it touches the paper."""
    segs = page['segs']
    prev = None
    for pts, wid, ink, tm in segs:
        if tm[0] < 0:
            continue
        if t < tm[0]:
            if prev is None:
                return pts[0], False, 0.0
            # in the air between strokes: glide from the last point to the next stroke
            p0, t0 = prev
            u = np.clip((t - t0) / max(tm[0] - t0, 1e-3), 0, 1)
            return p0 + (pts[0] - p0) * u, False, float(np.sin(np.pi * u))
        if t <= tm[-1]:
            i = int(np.searchsorted(tm, t))
            i = min(max(i, 1), len(tm) - 1)
            f = (t - tm[i - 1]) / max(tm[i] - tm[i - 1], 1e-6)
            return pts[i - 1] + (pts[i] - pts[i - 1]) * f, True, 0.0
        prev = (pts[-1], tm[-1])
    if prev is None:
        return np.array([PWID / 2, PHEI / 2], np.float32), False, 1.0
    return prev[0], False, 1.0


def pages_for_film():
    """The pages used in the film, with their writing times (global seconds; see timeline in film.py)."""
    P = {}
    P['p1'] = build_page('p1', [("Zu viel hundert tausend guter nacht hertzliebe dochter Veronica.", 11.6, 19.2),
                                ("Vnschuldig bin ich in das gefengnus kommen, vnschuldig bin ich gemarttert worden, vnschuldig muss ich sterben.", 19.95, 25.3)],
                         seed=11)
    P['p1_full'] = build_page('p1_full', [(LETTER_P1, -1, -1)], seed=11, width=880)
    P['p1_margin'] = margin_note('p1_margin', MARGIN_P1)
    P['p3'] = build_page('p3', [(LETTER_P3_PRE, -1, -1), (LETTER_P3_TRUE, 101.7, 102.9), (LETTER_P3_LIES, 103.1, 105.6)], seed=31)
    P['p4'] = build_page('p4', [(LETTER_P4_PRE, -1, -1), (LETTER_P4_HIDE, 126.1, 128.6), (LETTER_P4_MARTYR, 131.0, 133.4),
                                (LETTER_P4_NIGHT, 134.4, 138.0)], seed=41)
    P['record'] = build_page('record', [(RECORD, -1, -1)], style=CLERK, seed=51, x0=96, y0=135, width=945)
    P['record2'] = build_page('record2', [(RECORD2, -1, -1)], style=CLERK, seed=53, x0=96, y0=135, width=945)
    return P
