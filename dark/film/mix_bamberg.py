"""The sound of the Bamberg film: narration (voice D, close 'nocturne' chain), real recorded foley and ambience per scene
(BigSoundBank CC0), a sampled string score (VSCO-2-CE / VCSL, CC0), mixed to -14 LUFS with peaks under -1 dBFS.
    python mix_bamberg.py out.wav"""
from darkroot import ROOT
import sys, os, glob
sys.path.insert(0, ROOT + '/film')
sys.path.insert(0, ROOT + '/voice')
import numpy as np
import pedalboard as pb
import pyloudnorm as pyln
import soundfile as sf
import film_bamberg as F
import pages as PG

SR = 48000
N = int((F.TOTAL + 0.2) * SR)
SFX = ROOT + '/sfx/'
_C = {}


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
    """Gain envelope (0..1) of the named shots' screen weights, at SR."""
    ts = np.arange(0, N / SR, 1 / res)
    e = np.zeros(len(ts), np.float32)
    for s in shots:
        if s.name in names:
            e = np.maximum(e, np.array([s.weight(t) for t in ts], np.float32))
    return np.interp(np.arange(N) / SR, ts, e).astype(np.float32)


def pen_env(page, t0, t1):
    """Quill scratch envelope following the nib: sound only while it touches the paper, louder when it moves fast."""
    env = np.zeros(N, np.float32)
    hop = SR // 200
    prev = None
    for i in range(int(t0 * SR), min(int(t1 * SR), N), hop):
        p, down, _ = PG.pen_at(page, i / SR)
        sp = 0.0 if prev is None else float(np.linalg.norm(p - prev)) * 200
        prev = p
        env[i:i + hop] = (1.0 if down else 0.0) * np.clip(sp / 260.0, 0.25, 1.4)
    return np.convolve(env, np.ones(SR // 60) / (SR // 60), mode='same').astype(np.float32)


def seg_env(segs, t0, t1):
    env = np.zeros(N, np.float32)
    for pts, wid, ink, tm in segs:
        a, b = float(tm[0]), float(tm[-1])
        if b < t0 or a > t1 or a < 0:
            continue
        env[int(a * SR):int(min(b, t1) * SR)] = np.maximum(env[int(a * SR):int(min(b, t1) * SR)], 0.8)
    return np.convolve(env, np.ones(SR // 50) / (SR // 50), mode='same').astype(np.float32)


def voice_chain(kind, x):
    """The narrator, finished: warm and present; his letter a little closer and darker, in a small room; the court
    record drier and colder, like a clerk reading."""
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


def main(out):
    V, S = F.V, F.S
    shots = F.build_shots()
    sh = {s.name: s for s in shots}
    fxb = np.zeros(N, np.float32)       # foley (dry, then a small stone room)
    ambL = np.zeros(N, np.float32); ambR = np.zeros(N, np.float32)
    mus = np.zeros(N, np.float32)
    vo = np.zeros(N, np.float32)

    def amb(x, t, g, fi=1.0, fo=1.0, length=None, start=0.0, width=0.0):
        place(ambL, x, t, g, fi, fo, length, start)
        place(ambR, x, t, g, fi, fo, length, start + width)

    # ---------------------------------------------------------------- beds (follow the picture's crossfades)
    rain = fx('rain_concrete')
    cells = env_of(shots, {'cell_open', 'lie', 'last_lines', 'letter_nails'})
    rain_in = lp(hp(rain, 120), 2400)
    ambL += loop(rain_in, N / SR) * cells * db(-23)
    ambR += loop(np.roll(rain_in, 20 * SR), N / SR) * cells * db(-23)
    cand = hp(loop(fx('candle_sparkle_1'), N / SR), 250)
    fxb += cand * cells * db(-29)
    city = env_of(shots, {'city_wide', 'city_portal'})
    ambL += loop(hp(rain, 90), N / SR) * city * db(-17)
    ambR += loop(np.roll(hp(rain, 90), 31 * SR), N / SR) * city * db(-17)
    ambL += loop(lp(fx('rain_puddle'), 6000), N / SR) * city * db(-25)
    arch = env_of(shots, {'archive_open', 'record_witness', 'record_screws', 'record_legs', 'archive_end', 'spee', 'names', 'streets'})
    room = lp(loop(fx('wind_inside_2'), N / SR), 700)
    ambL += room * arch * db(-30); ambR += np.roll(room, 7 * SR) * arch * db(-30)
    ambL += loop(lp(hp(rain, 150), 900), N / SR) * arch * db(-33); ambR += loop(np.roll(lp(hp(rain, 150), 900), 9 * SR), N / SR) * arch * db(-33)
    tort = env_of(shots, {'room', 'hoist'})
    fire = loop(fx('fireplace_2'), N / SR)
    ambL += fire * tort * db(-22); ambR += np.roll(fire, 5 * SR) * tort * db(-22)
    cav = lp(loop(fx('cave_1'), N / SR), 1800)
    ambL += cav * np.maximum(tort, env_of(shots, {'corridor'})) * db(-28)
    ambR += np.roll(cav, 3 * SR) * np.maximum(tort, env_of(shots, {'corridor'})) * db(-28)
    dawn = env_of(shots, {'dawn'})
    wind = lp(loop(fx('strong_wind_village'), N / SR), 3000)
    ambL += wind * dawn * db(-24); ambR += np.roll(wind, 4 * SR) * dawn * db(-24)
    # ---------------------------------------------------------------- the quill and the ink
    P = F.pages_for_film()
    scr = np.concatenate([fx('pencil_3'), fx('pencil_2'), fx('pencil_4')])
    scr = pb.Pedalboard([pb.HighpassFilter(1400), pb.PeakFilter(4200, 4, 1.0), pb.LowpassFilter(11000)])(scr, SR)
    scr = loop(scr, N / SR)
    e = pen_env(P['p1'], sh['cell_open'].t0, sh['cell_open'].t1) + pen_env(P['p3'], sh['lie'].t0, sh['lie'].t1) + \
        pen_env(P['p4'], sh['last_lines'].t0, sh['last_lines'].t1)
    fxb += scr * e * db(-13)
    import sheet as SHT
    segs_n, _ = SHT.names_segs(V)
    segs_s, _ = SHT.streets_segs(V)
    e2 = seg_env(segs_n, sh['names'].t0, sh['names'].t1) + seg_env(segs_s, sh['streets'].t0, sh['streets'].t1)
    fxb += np.roll(scr, 3 * SR) * e2 * db(-19)
    # ---------------------------------------------------------------- events
    place(fxb, fx('paper'), 0.4, -26, fo=1.0, length=2.5)
    place(fxb, onset(fx('drops_1')), V['q1'][0] + 2.0 - 0.02, -24, length=0.5, fo=0.2)            # ink drop
    place(ambL, lp(fx('thunder_4'), 900), V['q2'][1] + 0.6, -14, fo=3.0, length=9.0)            # under the title
    place(ambR, lp(fx('thunder_4'), 800), V['q2'][1] + 0.65, -15, fo=3.0, length=9.0)
    bell = lp(onset(fx('church_bell_1')), 2500)
    place(ambL, bell, V['q2'][1] + 1.0, -24, fo=3.0, length=7.0)                                    # a far bell under the title
    place(ambR, bell, V['q2'][1] + 1.05, -25, fo=3.0, length=7.0)
    place(fxb, lp(fx('steps_concrete'), 3000), sh['city_wide'].t0 + 1.5, -30, fi=1.0, fo=1.5, length=6.0)
    place(ambL, lp(fx('thunder_8'), 1200), V['w1'][0] - 0.5, -20, fo=3.0, length=8.0)
    place(fxb, onset(fx('heartbeat_4')), V['w5'][0] - 0.2, -22, fi=0.3, fo=1.0, length=3.6)
    place(fxb, fx('page_turned'), sh['record_witness'].t0 + 0.3, -24, length=1.6)
    place(fxb, lp(onset(fx('creak_metal_door')), 5000), V['t1'][0] + 1.4, -18, fo=0.8, length=3.0)   # "The executioner comes"
    place(fxb, lp(fx('steps_stone_stair'), 4000), V['t1'][0] + 2.0, -22, fi=0.2, fo=0.8, length=3.0)
    place(fxb, onset(fx('heavy_chain')), sh['room'].t1 - 1.6, -22, length=1.8, fo=0.6)
    place(fxb, onset(fx('winder_1')), F.find_word('t2', 'thumbscrews')[0] - 0.1, -21, length=1.6, fo=0.5)
    place(fxb, onset(fx('drops_2')), F.find_word('t3', 'nails')[0] + 0.05, -23, length=0.6, fo=0.2)
    place(fxb, onset(fx('winder_2')), F.find_word('t4', 'leg')[0] - 0.1, -21, length=1.8, fo=0.5)
    tf = F.find_word('t5', 'fall')[0]
    place(fxb, onset(fx('rope_big')), sh['hoist'].t0 + 0.6, -17, fi=0.2, length=tf - sh['hoist'].t0 - 0.6, fo=0.3)
    place(fxb, onset(fx('wind_tree_squeaks')), sh['hoist'].t0 + 1.4, -27, length=tf - sh['hoist'].t0 - 1.4, fo=0.2)
    place(fxb, onset(fx('rope_slide_5')), tf - 0.35, -14, length=0.5, fo=0.1)
    thud = onset(fx('body_fall_2'))
    place(fxb, thud, tf + 0.05, -6, length=1.2, fo=0.4)
    # the other seven, as consciousness goes: duller, further, like a pulse
    t8 = V['t5'][1] + 0.3
    for k in range(7):
        x = lp(onset(fx('body_fall_1' if k % 2 else 'body_fall_5')), 1600 - 160 * k)
        place(fxb, x, t8 + k * 0.52, -12 - 2.2 * k, length=0.8, fo=0.3)
    # the corridor
    steps = lp(fx('steps_stone_stair'), 3500)
    place(fxb, steps, sh['corridor'].t0 + 0.4, -21, fi=0.6, fo=0.8, length=F.V['p2'][0] - sh['corridor'].t0 - 0.2)
    place(fxb, onset(fx('breathless_man')), sh['corridor'].t0 + 1.0, -30, fi=0.5, fo=1.0, length=5.0)
    place(fxb, onset(fx('keys_hand')), V['p2'][1] - 0.1, -24, length=1.4, fo=0.5)
    place(fxb, onset(fx('lock_big_key')), sh['corridor'].t1 - 0.3, -19, length=2.0, fo=0.6)
    # the lie: a goat, very far, as an absurd memory
    gb = pb.Pedalboard([pb.LowpassFilter(1800), pb.Reverb(room_size=0.9, wet_level=0.6, dry_level=0.3)])(onset(fx('goat_bleat_1')), SR)
    place(ambL, gb, F.find_word('l3', 'goat')[0], -27, length=2.5, fo=1.0)
    place(fxb, onset(fx('ice_crack_2')), F.find_word('l3', 'pottery')[0] - 0.05, -27, length=0.8, fo=0.3)
    # streets: the town he walks in his mind, far away
    sq = lp(fx('church_square'), 2500)
    place(ambL, sq, V['l5'][0] - 0.5, -31, fi=1.5, fo=2.0, length=V['l6'][1] - V['l5'][0] + 1.0)
    place(ambR, np.roll(sq, 2 * SR), V['l5'][0] - 0.5, -31, fi=1.5, fo=2.0, length=V['l6'][1] - V['l5'][0] + 1.0)
    # the candle dies
    place(fxb, onset(fx('sigh_nose')), V['e3'][1] + 0.1, -31, length=1.4, fo=0.5)
    # dawn: crows, a bell for the dead, a fire far off
    place(ambL, fx('crows_1'), sh['dawn'].t0 + 0.2, -24, fi=0.5, fo=1.5, length=4.0)
    place(ambR, fx('carrion_crow_4'), sh['dawn'].t0 + 1.2, -26, fo=1.0, length=3.0)
    place(ambL, lp(onset(fx('church_bell')), 3000), V['c1'][0] - 0.3, -20, fo=4.0, length=8.0)
    place(ambR, lp(onset(fx('church_bell')), 2800), V['c1'][0] - 0.25, -21, fo=4.0, length=8.0)
    place(ambR, lp(fx('fire_branching_1'), 1500), sh['dawn'].t0, -30, fi=1.0, fo=1.0, length=4.0)
    place(fxb, onset(fx('book_closed_2')), F.find_word('c2', 'filed')[0] - 0.1, -17, length=1.5, fo=0.5)
    place(fxb, fx('great_page_1'), sh['spee'].t0 + 0.5, -24, length=2.0, fo=0.6)
    place(ambL, lp(onset(fx('church_bell_1')), 2200), V['c3'][1] + 0.9, -23, fo=2.0, length=F.TOTAL - V['c3'][1] - 0.9)
    fxb = pb.Pedalboard([pb.Reverb(room_size=0.32, damping=0.55, wet_level=0.2, dry_level=0.9, width=0.6)])(fxb, SR)
    # ---------------------------------------------------------------- score
    def hold(kind, n, t0, t1, g, fi=3.0, fo=2.5):
        place(mus, held(note(kind, n), t1 - t0), t0, g, fi=fi, fo=fo)
    hold('cb', 'D1', 0.3, V['h4'][0] + 1.0, -15, fi=3.5)
    hold('cello', 'D2', V['h3'][0] - 0.5, V['h4'][1] + 1.0, -19)
    hold('cello', 'D2', V['q1'][0] - 0.4, V['q2'][0] + 3.0, -13, fi=3.5)
    hold('cello', 'A2', V['q2'][0] - 0.3, V['q2'][1] + 3.5, -17)
    hold('cb', 'D1', V['q2'][0] - 0.5, V['q2'][1] + 4.0, -12)
    hold('vla', 'D3', V['q2'][1] + 0.4, V['w1'][0] + 2.0, -19, fi=1.2)
    hold('vln', 'A3', V['q2'][1] + 0.6, V['w1'][0] + 1.5, -22, fi=1.2)
    hold('cello', 'F2', V['w1'][0] - 0.5, V['w4'][1] + 1.0, -19)
    hold('cb', 'D1', V['w2'][0], V['w5'][1] + 1.5, -16)
    hold('cello', 'A2', V['w4'][0], V['w5'][1] + 2.0, -18)
    hold('vln', 'D5', V['j1'][0], V['j2'][1] + 1.0, -30, fi=2.0, fo=1.0)
    hold('cb', 'A#0', V['t1'][0] - 1.0, tf + 0.1, -12, fi=2.5, fo=0.15)
    hold('cello', 'A2', V['t2'][0], tf + 0.1, -21, fi=3.0, fo=0.15)
    place(mus, held(note('trem', 'D'), tf - V['t5'][0] + 1.0), V['t5'][0] - 1.0, -23, fi=2.0, fo=0.12)
    hold('vla', 'D3', V['p1'][0] - 0.8, V['p2'][1] + 1.5, -21)
    hold('cello', 'D2', V['p2'][0] - 0.5, V['l2'][1] + 1.0, -18)
    hold('cello', 'F2', V['l1'][0], V['l3'][1] + 1.5, -21)
    hold('cb', 'D1', V['l4'][0] - 0.5, V['l7'][1] + 1.0, -16)
    hold('vla', 'A3', V['l6'][0], V['l7'][1] + 1.0, -21)
    hold('cello', 'D2', V['e1'][0] - 1.0, V['e3'][1] + 2.0, -15)
    hold('vln', 'A3', V['e2'][0] - 0.3, V['e3'][1] + 2.0, -19)
    hold('vln', 'D5', V['e3'][0], V['e3'][1] + 2.0, -25)
    hold('cb', 'D1', V['c1'][0] - 1.5, F.TOTAL, -15, fo=2.0)
    hold('cello', 'D2', V['c2'][0], F.TOTAL, -17, fo=2.0)
    hold('vla', 'A3', V['c3'][0], F.TOTAL, -20, fo=2.0)
    hold('vln', 'D5', V['c3'][0] + 2.0, F.TOTAL, -24, fo=2.0)
    mus = pb.Pedalboard([pb.Reverb(room_size=0.85, damping=0.4, wet_level=0.32, dry_level=0.75, width=1.0), pb.LowpassFilter(9000)])(mus, SR)
    # ---------------------------------------------------------------- narration
    for lid in F.ORDER:
        x = load(F.VO + lid + '.wav')
        kind = 'letter' if F.QUOTE[lid] else ('record' if lid in ('t2', 't4', 'l3') else 'narr')
        place(vo, voice_chain(kind, x), S[lid], 0.0)
    meter = pyln.Meter(SR)
    vo *= db(-16.5 - meter.integrated_loudness(vo.astype(np.float64)[:, None]))
    venv = np.convolve(np.abs(vo), np.ones(SR // 10) / (SR // 10), mode='same')
    duck = 1 - 0.35 * np.clip(venv / (venv.max() + 1e-9) * 3, 0, 1)
    mst = pb.Pedalboard([pb.Reverb(room_size=0.5, wet_level=0.0, dry_level=1.0, width=1.0)])(np.stack([mus, np.roll(mus, 311)]), SR)
    L = vo + (fxb + ambL) * duck * db(2) + mst[0] * duck
    R = vo + (fxb + ambR) * duck * db(2) + mst[1] * duck
    st = np.stack([L, R], 1).astype(np.float64)
    st *= db(-14.0 - meter.integrated_loudness(st))
    lim = pb.Pedalboard([pb.Limiter(threshold_db=-2.0, release_ms=150)])(st.T.astype(np.float32), SR).T
    pk = np.abs(lim).max()
    lim = lim * (db(-1.2) / pk if pk > db(-1.2) else 1.0)
    fade = np.ones(N, np.float32); fade[-int(1.0 * SR):] = np.linspace(1, 0, int(1.0 * SR)) ** 2
    st = lim * fade[:, None]
    lf = meter.integrated_loudness(st.astype(np.float64))
    if lf > -14.0:
        st = st * db(-14.0 - lf)
    sf.write(out, st, SR, subtype='PCM_24')
    print('loudness', round(meter.integrated_loudness(st.astype(np.float64)), 2), 'peak dB', round(20 * np.log10(np.abs(st).max()), 2),
          'length', round(len(st) / SR, 2))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else ROOT + '/out/bamberg_audio.wav')
