"""Sound tools of the Bamberg mix, shared by later films: real recordings (BigSoundBank CC0) placed and looped, beds
that follow the picture's crossfades, a sampled string score (VSCO-2-CE / VCSL, CC0), the narrator's chain, and the
master to -14 LUFS with peaks under -1 dBFS. Plus synthetic sea and splash (the library has no surf)."""
from darkroot import ROOT
import sys, glob
sys.path.insert(0, ROOT + '/film')
import numpy as np
import pedalboard as pb
import pyloudnorm as pyln
import soundfile as sf

SR = 48000
SFX = ROOT + '/sfx/'
_C = {}
N = 0


def setup(total):
    global N
    N = int((total + 0.2) * SR)
    return N


def load(path):
    if path in _C:
        return _C[path]
    x, sr = sf.read(path, dtype='float32', always_2d=True)
    x = x.mean(1)
    if sr != SR:
        from scipy.signal import resample_poly
        x = resample_poly(x, SR, sr).astype(np.float32)
    _C[path] = x
    return x


def fx(name):
    return load(SFX + name + '.wav')


def db(x):
    return 10 ** (x / 20)


def place(bus, x, t, g=0.0, fi=0.0, fo=0.0, length=None, start=0.0):
    x = x[int(start * SR):]
    if length is not None:
        x = x[:int(length * SR)]
    x = x.copy() * db(g)
    if fi > 0:
        n = min(len(x), int(fi * SR)); x[:n] *= np.linspace(0, 1, n) ** 2
    if fo > 0:
        n = min(len(x), int(fo * SR)); x[-n:] *= np.linspace(1, 0, n) ** 2
    i0 = int(t * SR)
    i1 = min(len(bus), i0 + len(x))
    if i1 > max(i0, 0):
        bus[max(i0, 0):i1] += x[max(0, -i0):i1 - i0]


def loop(x, dur):
    n = int(dur * SR)
    if len(x) >= n:
        return x[:n]
    L = int(0.5 * SR)
    out = x.copy()
    while len(out) < n:
        out[-L:] = out[-L:] * np.linspace(1, 0, L) + x[:L] * np.linspace(0, 1, L)
        out = np.concatenate([out, x[L:]])
    return out[:n]


def onset(x, thr=0.08):
    i = int(np.argmax(np.abs(x) > thr * np.abs(x).max()))
    return x[max(0, i - 200):]


def lp(x, f):
    return pb.Pedalboard([pb.LowpassFilter(f)])(x, SR)


def hp(x, f):
    return pb.Pedalboard([pb.HighpassFilter(f)])(x, SR)


def held(x, dur, xf=0.6):
    a, b = int(0.6 * SR), len(x) - int(0.8 * SR)
    mid = x[a:b]
    out = x[:a].copy()
    L = int(xf * SR)
    while len(out) < dur * SR:
        out[-L:] = out[-L:] * np.linspace(1, 0, L) ** 0.5 + mid[:L] * np.linspace(0, 1, L) ** 0.5
        out = np.concatenate([out, mid[L:]])
    return out[:int(dur * SR)]


def note(kind, n):
    pats = {'cello': ROOT + f'/vsco/Strings/Cello Section/susvib/susvib_{n}_v1_1.wav',
            'cb': ROOT + f'/samples/Strings/Solo Contrabass/SusNV/BKCtbss_SusNV_{n}_v1_rr1.wav',
            'vln': ROOT + f'/samples/Strings/Violin Section/susVib/VlnEns_susVib_{n}_v1.wav',
            'vla': ROOT + f'/samples/Strings/Viola Section/susvib/ViolaEns_susvib_{n}_v1_1.wav'}
    if kind == 'trem':
        fs = sorted(glob.glob(ROOT + '/samples/Strings/Violin Section/Trem/*' + n + '*'))
        return load(fs[0])
    return load(pats[kind])


def env_of(shots, names, res=100):
    ts = np.arange(0, N / SR, 1 / res)
    e = np.zeros(len(ts), np.float32)
    for s in shots:
        if s.name in names:
            e = np.maximum(e, np.array([s.weight(t) for t in ts], np.float32))
    return np.interp(np.arange(N) / SR, ts, e).astype(np.float32)


def pen_env(page, t0, t1):
    import pages as PG
    env = np.zeros(N, np.float32)
    hop = SR // 200
    prev = None
    for i in range(int(t0 * SR), min(int(t1 * SR), N), hop):
        p, down, _ = PG.pen_at(page, i / SR)
        sp = 0.0 if prev is None else float(np.linalg.norm(p - prev)) * 200
        prev = p
        env[i:i + hop] = (1.0 if down else 0.0) * np.clip(sp / 260.0, 0.25, 1.4)
    return np.convolve(env, np.ones(SR // 60) / (SR // 60), mode='same').astype(np.float32)


def scratch():
    scr = np.concatenate([fx('pencil_3'), fx('pencil_2'), fx('pencil_4')])
    scr = pb.Pedalboard([pb.HighpassFilter(1400), pb.PeakFilter(4200, 4, 1.0), pb.LowpassFilter(11000)])(scr, SR)
    return loop(scr, N / SR)


def voice_chain(kind, x):
    base = [pb.HighpassFilter(75), pb.LowShelfFilter(180, 1.5), pb.PeakFilter(3000, 1.5, 0.9),
            pb.PeakFilter(6800, -3.0, 2.0), pb.Compressor(threshold_db=-20, ratio=2.5, attack_ms=8, release_ms=120)]
    if kind == 'letter':
        fx_ = base + [pb.PeakFilter(400, 1.0, 1.0), pb.LowpassFilter(8500), pb.Reverb(room_size=0.22, damping=0.6, wet_level=0.13, dry_level=1.0, width=0.5)]
    elif kind == 'record':
        fx_ = base + [pb.HighpassFilter(140), pb.PeakFilter(1800, 2.0, 1.0), pb.Reverb(room_size=0.12, wet_level=0.05, dry_level=1.0)]
    else:
        fx_ = base + [pb.Reverb(room_size=0.18, damping=0.5, wet_level=0.08, dry_level=1.0, width=0.6)]
    y = pb.Pedalboard(fx_)(np.asarray(x, np.float32), SR)
    return (y / (np.abs(y).max() + 1e-9) * 0.9).astype(np.float32)


# ------------------------------------------------------------------ synthetic sea
def sea(dur, seed=0, swell=0.11, rough=1.0):
    """Open-sea wash: brown noise shaped by slow swells, with a hiss of breaking crests on each swell."""
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    w = r.standard_normal(n).astype(np.float32)
    br = np.cumsum(w); br -= np.convolve(br, np.ones(SR // 5) / (SR // 5), mode='same'); br /= np.abs(br).max() + 1e-9
    t = np.arange(n) / SR
    env = np.zeros(n, np.float32)
    for k, (f, ph) in enumerate(zip(r.uniform(0.07, 0.16, 5) * (swell / 0.11), r.uniform(0, 6.3, 5))):
        env += (0.5 + 0.5 * np.sin(2 * np.pi * f * t + ph)) ** 3
    env = env / env.max()
    low = lp(br * (0.35 + 0.65 * env), 700)
    hiss = hp(lp(w * env ** 2.5, 6000), 1200) * 0.12 * rough
    x = low + hiss
    return (x / (np.abs(x).max() + 1e-9) * 0.8).astype(np.float32)


def splash(seed=0, size=1.0):
    r = np.random.default_rng(seed)
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    w = r.standard_normal(n).astype(np.float32)
    body = lp(w, 900) * np.exp(-t * 6) * 1.2
    spray = hp(lp(w, 7000), 1500) * (np.exp(-t * 9) + 0.25 * np.exp(-t * 2.5)) * 0.5
    thump = np.sin(2 * np.pi * 70 * t) * np.exp(-t * 18) * 0.8
    x = (body + spray + thump) * size
    return (x / (np.abs(x).max() + 1e-9) * 0.9).astype(np.float32)


def master(out, vo, fxb, ambL, ambR, mus, fade=1.0):
    meter = pyln.Meter(SR)
    vo = vo * db(-16.5 - meter.integrated_loudness(vo.astype(np.float64)[:, None]))
    venv = np.convolve(np.abs(vo), np.ones(SR // 10) / (SR // 10), mode='same')
    duck = 1 - 0.35 * np.clip(venv / (venv.max() + 1e-9) * 3, 0, 1)
    mus = pb.Pedalboard([pb.Reverb(room_size=0.85, damping=0.4, wet_level=0.32, dry_level=0.75, width=1.0), pb.LowpassFilter(9000)])(mus, SR)
    mst = np.stack([mus, np.roll(mus, 311)])
    L = vo + (fxb + ambL) * duck * db(2) + mst[0] * duck
    R = vo + (fxb + ambR) * duck * db(2) + mst[1] * duck
    st = np.stack([L, R], 1).astype(np.float64)
    st *= db(-14.0 - meter.integrated_loudness(st))
    lim = pb.Pedalboard([pb.Limiter(threshold_db=-2.0, release_ms=150)])(st.T.astype(np.float32), SR).T
    pk = np.abs(lim).max()
    lim = lim * (db(-1.2) / pk if pk > db(-1.2) else 1.0)
    fd = np.ones(N, np.float32); fd[-int(fade * SR):] = np.linspace(1, 0, int(fade * SR)) ** 2
    st = lim * fd[:, None]
    lf = meter.integrated_loudness(st.astype(np.float64))
    if lf > -14.0:
        st = st * db(-14.0 - lf)
    sf.write(out, st, SR, subtype='PCM_24')
    print('loudness', round(meter.integrated_loudness(st.astype(np.float64)), 2), 'peak dB', round(20 * np.log10(np.abs(st).max()), 2),
          'length', round(len(st) / SR, 2))
