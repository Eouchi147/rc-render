"""Quality test for Sam: the cold open's cell sequence (film time 9.6 to 25.6 s), picture + narration + real sound + score."""
import sys, os, json, math, subprocess, shutil
from darkroot import ROOT, ffmpeg_exe
sys.path.insert(0, ROOT + '/film')
import numpy as np
import cv2

T0, T1, FPS = 9.6, 25.6, 24
OUT = ROOT + '/out'
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
MACRO = dict(zoom=2.5, center=(700, 1800))


def smooth_keys(t, ks):
    """Catmull-Rom through (time, value-tuple) keys: continuous motion, no stops."""
    ts = [k[0] for k in ks]
    if t <= ts[0]:
        return np.array(ks[0][1], float)
    if t >= ts[-1]:
        return np.array(ks[-1][1], float)
    i = max(0, np.searchsorted(ts, t) - 1)
    P = [np.array(ks[max(0, min(len(ks) - 1, j))][1], float) for j in (i - 1, i, i + 1, i + 2)]
    t0, t1 = ts[i], ts[i + 1]
    u = (t - t0) / (t1 - t0)
    u = u * u * (3 - 2 * u) * 0.35 + u * 0.65
    p0, p1, p2, p3 = P
    return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)


def setup():
    import shot_cell as SC, pages as PG
    base = SC.CellShot('tall', 19.0, 'p1', blot_t=13.3)
    mac = SC.CellShot('tall', 19.0, 'p1', blot_t=13.3, **MACRO)
    page = PG.pages_for_film()['p1']

    def plate(t):
        p, _, _ = PG.pen_at(page, t)
        q = base.Hp @ np.array([p[0], p[1], 1.0])
        return q[:2] / q[2]
    s0, sm, s1 = plate(11.7), plate(15.6), plate(19.1)
    fl = base.flame_plate
    keys = [(9.6, (s0[0] + 170, s0[1] + 20, 4.1)), (11.6, (s0[0] + 160, s0[1] + 18, 3.95)),
            (15.6, (sm[0] + 30, sm[1] + 22, 3.5)), (19.2, (s1[0] - 60, s1[1] + 60, 2.8)),
            (21.4, (980, 1620, 1.8)), (23.3, (920, 1470, 1.24)), (25.6, (1105, fl[1] + 110, 1.58))]
    return base, mac, keys


def cam_at(t, keys):
    import engine as E
    u, v, f = smooth_keys(t, keys)
    focus = 1.0 + 0.2 * np.clip((t - 22.6) / 2.0, 0, 1)
    return E.Cam(x=(u - 810) / 1.5, y=(v - 1440) / 1.5, f=f, ap=9.0, focus=focus)


def captions():
    import engine as E
    tm = json.load(open(ROOT + '/film/vo/timing.json'))
    starts = dict(h4=10.8, q1=14.8, q2=19.9)
    caps = []
    for lid, st in starts.items():
        words = tm[lid]['words']
        italic = tm[lid]['q']
        chunk, c0 = [], None
        for w, a, b in words:
            if c0 is None:
                c0 = a
            chunk.append(w)
            if w.endswith(('.', '?', '!')) and (len(chunk) >= 4 or w == words[-1][0]):
                caps.append((st + c0 - 0.05, st + b + 0.35, ' '.join(chunk), italic)); chunk, c0 = [], None
        if chunk:
            caps.append((st + c0 - 0.05, st + words[-1][2] + 0.35, ' '.join(chunk), italic))
    out = []
    for a, b, txt, it in caps:
        if it:
            txt = '“' + txt + '”' if not txt.startswith('Innocent I came') else '“' + txt
        lines, cur = [], ''
        for wd in txt.split():
            if len(cur) + len(wd) + 1 > 30 and cur:
                lines.append(cur); cur = wd
            else:
                cur = (cur + ' ' + wd).strip()
        lines.append(cur)
        fn = 'Newsreader-Italic[opsz,wght].ttf' if it else 'Newsreader[opsz,wght].ttf'
        rgb, al = E.text_image(lines, fn, 52, col=(0.97, 0.94, 0.87), spacing=1.22)
        out.append((a, b, rgb, al))
    return out


def macro_mask(mac, cam, t):
    import engine as E
    M = E.layer_matrix(mac.desk, cam, t)[:2]
    one = np.ones((mac.z['desk'].shape[0] // 4, mac.z['desk'].shape[1] // 4), np.float32)
    one[:3] = 0; one[-3:] = 0; one[:, :3] = 0; one[:, -3:] = 0
    M4 = M.copy(); M4[:, :2] *= 4
    m = cv2.warpAffine(one, M4, (W, H), flags=cv2.INTER_LINEAR)
    m = cv2.GaussianBlur(m, (0, 0), 40)
    return np.clip((m - 0.5) * 2.2 + 0.5, 0, 1)


def cover_ok(mac, cam, t):
    return macro_mask(mac, cam, t).min() > 0.999


def worker(args):
    wid, frames = args
    import engine as E
    base, mac, keys = setup()
    caps = captions()
    path = f'{OUT}/part{wid}.mp4'
    p = subprocess.Popen([ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    for fi in frames:
        t = T0 + fi / FPS
        cam = cam_at(t, keys)
        k = float(np.clip((cam.f - 1.75) / 0.6, 0, 1))
        if k >= 1.0 and cover_ok(mac, cam, t):
            img, _ = mac.render(t, cam, fi)
        elif k <= 0.0:
            img, _ = base.render(t, cam, fi)
        else:
            a, _ = mac.render(t, cam, fi)
            b, _ = base.render(t, cam, fi)
            m = macro_mask(mac, cam, t) * k
            img = a * m[..., None] + b * (1 - m[..., None])
        img = E.bloom(img, thr=0.78, strength=0.42)
        img = E.streak(img, thr=1.3, strength=0.05)
        img = E.aberration(img, 0.0012)
        img = E.vignette(img, 0.5)
        fade = np.clip((t - T0) / 1.0, 0, 1) ** 1.5
        img = E.tonemap(img * fade, 1.06, lift=(0.012, 0.008, 0.006), gamma=(1.04, 1.0, 0.97))
        img = E.grain(img, fi, 0.028)
        img = E.weave(img, fi, 0.35)
        for a, b, rgb, al in caps:
            if a - 0.25 < t < b + 0.25:
                op = min(1.0, (t - (a - 0.25)) / 0.25, ((b + 0.25) - t) / 0.25)
                E.put(img, rgb, al, W / 2, 1480, opacity=op, shadow=0.9)
        p.stdin.write((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
        if fi % 24 == 0:
            print(wid, 'frame', fi, flush=True)
    p.stdin.close(); p.wait()
    return path


# ------------------------------------------------------------------ sound
SR = 48000


def load(path):
    import soundfile as sf
    x, sr = sf.read(path, dtype='float32', always_2d=True)
    x = x.mean(1)
    if sr != SR:
        from scipy.signal import resample_poly
        x = resample_poly(x, SR, sr).astype(np.float32)
    return x


def db(x):
    return 10 ** (x / 20)


def place(bus, x, t, gain_db=0.0, fade_in=0.0, fade_out=0.0, length=None):
    i0 = int(t * SR)
    if length is not None:
        x = x[:int(length * SR)]
    x = x.copy() * db(gain_db)
    if fade_in > 0:
        n = min(len(x), int(fade_in * SR)); x[:n] *= np.linspace(0, 1, n) ** 2
    if fade_out > 0:
        n = min(len(x), int(fade_out * SR)); x[-n:] *= np.linspace(1, 0, n) ** 2
    i1 = min(len(bus), i0 + len(x))
    if i1 > max(i0, 0):
        bus[max(i0, 0):i1] += x[max(0, -i0):i1 - i0]


def audio():
    import pedalboard as pb
    import pyloudnorm as pyln
    sys.path.insert(0, ROOT + '/film')
    sys.path.insert(0, ROOT + '/voice')
    import voices as VO, pages as PG
    D = T1 - T0 + 0.8
    n = int(D * SR)
    fx = np.zeros(n, np.float32); amb = np.zeros(n, np.float32); mus = np.zeros(n, np.float32); vo = np.zeros(n, np.float32)
    S = ROOT + '/sfx/'
    # rain beyond a small window in a stone wall: muffled, with a closer drip
    rain_all = load(S + 'rain_concrete.wav')
    rainL = pb.Pedalboard([pb.LowpassFilter(2600), pb.HighpassFilter(120)])(rain_all[int(10 * SR):], SR)
    rainR = pb.Pedalboard([pb.LowpassFilter(2400), pb.HighpassFilter(120)])(rain_all[int(40 * SR):], SR)
    ambR = np.zeros(n, np.float32)
    place(amb, rainL, 0.0, -22, fade_in=1.4, length=D)
    place(ambR, rainR, 0.0, -22, fade_in=1.4, length=D)
    puddle = pb.Pedalboard([pb.LowpassFilter(5000)])(load(S + 'rain_puddle.wav')[int(5 * SR):], SR)
    place(amb, puddle, 0.0, -33, fade_in=2.0, length=D)
    th = pb.Pedalboard([pb.LowpassFilter(900)])(load(S + 'thunder_4.wav'), SR)
    place(amb, th, 0.15, -16, fade_out=3.0, length=11.0)
    room = pb.Pedalboard([pb.LowpassFilter(900)])(load(S + 'wind_inside_1.wav')[int(20 * SR):], SR)
    place(amb, room, 0.0, -30, fade_in=2.0, length=D)
    # the candle, close
    cand = pb.Pedalboard([pb.HighpassFilter(250)])(load(S + 'candle_sparkle_1.wav')[int(3 * SR):], SR)
    place(fx, cand, 0.4, -27, fade_in=1.5, length=D)
    # the quill on paper, following the pen: scratch only while the nib is down
    page = PG.pages_for_film()['p1']
    scr = np.concatenate([load(S + 'pencil_3.wav'), load(S + 'pencil_2.wav'), load(S + 'pencil_4.wav')])
    scr = pb.Pedalboard([pb.HighpassFilter(1400), pb.PeakFilter(4200, 4, 1.0), pb.LowpassFilter(11000)])(scr, SR)
    env = np.zeros(n, np.float32)
    hop = SR // 200
    prev = None
    for i in range(0, n, hop):
        t = T0 + i / SR
        p, down, _ = PG.pen_at(page, t)
        sp = 0.0 if prev is None else float(np.linalg.norm(p - prev)) * 200
        prev = p
        env[i:i + hop] = (1.0 if down else 0.0) * np.clip(sp / 260.0, 0.25, 1.4)
    env = np.convolve(env, np.ones(SR // 60) / (SR // 60), mode='same')
    reps = int(np.ceil(n / len(scr))) + 1
    q = np.tile(scr, reps)[:n] * env * db(-12)
    fx += q
    # the ink drop at the blot
    drip = load(S + 'drops_1.wav')
    on = np.argmax(np.abs(drip) > 0.1)
    place(fx, drip[max(on - 400, 0):], 13.3 - T0 - 0.02, -24, length=0.5, fade_out=0.2)
    # a small stone room around the foley
    fx = pb.Pedalboard([pb.Reverb(room_size=0.28, damping=0.55, wet_level=0.16, dry_level=0.92, width=0.6)])(fx, SR)
    # score: a low cello section, a contrabass under it (VSCO-2-CE, real recordings)
    cello = load(ROOT + '/vsco/Strings/Cello Section/susvib/susvib_D2_v1_1.wav')
    cello2 = load(ROOT + '/vsco/Strings/Cello Section/susvib/susvib_A2_v1_1.wav')
    cb = load(ROOT + '/samples/Strings/Solo Contrabass/SusNV/BKCtbss_SusNV_D1_v1_rr1.wav')

    def held(x, dur, xf=0.6):
        """Stretch a sustained note by crossfading loops of its middle section."""
        a, b = int(0.6 * SR), len(x) - int(0.8 * SR)
        mid = x[a:b]
        out = x[:a].copy()
        L = int(xf * SR)
        while len(out) < dur * SR:
            seg = mid.copy()
            fo = np.linspace(1, 0, L) ** 0.5; fi = np.linspace(0, 1, L) ** 0.5
            out[-L:] = out[-L:] * fo + seg[:L] * fi
            out = np.concatenate([out, seg[L:]])
        return out[:int(dur * SR)]
    place(mus, held(cello, 12.0), 14.4 - T0, -13, fade_in=3.5, fade_out=2.5)
    place(mus, held(cello2, 7.0), 19.6 - T0, -17, fade_in=3.0, fade_out=2.0)
    place(mus, held(cb, 7.5), 19.4 - T0, -12, fade_in=3.0, fade_out=2.5)
    mus = pb.Pedalboard([pb.Reverb(room_size=0.85, damping=0.4, wet_level=0.32, dry_level=0.75, width=1.0), pb.LowpassFilter(9000)])(mus, SR)
    # narration (the series narrator), voice chain from the reels
    for lid, st in (('h4', 10.8), ('q1', 14.8), ('q2', 19.9)):
        x = load(f'{ROOT}/film/vo/{lid}.wav')
        x = VO.design('narrator', x)
        place(vo, x, st - T0, 0.0)
    meter = pyln.Meter(SR)
    lv = meter.integrated_loudness(vo.astype(np.float64)[:, None])
    vo *= db(-16.5 - lv)
    # duck the bed a little under the voice
    venv = np.convolve(np.abs(vo), np.ones(SR // 10) / (SR // 10), mode='same')
    duck = 1 - 0.35 * np.clip(venv / (venv.max() + 1e-9) * 3, 0, 1)
    ambR += amb - np.concatenate([np.zeros(0, np.float32), amb])[:n] * 0     # thunder, puddle, room: shared
    # put the shared ambience on both sides, the two rain takes left and right
    rain_only = np.zeros(n, np.float32)
    place(rain_only, rainL, 0.0, -22, fade_in=1.4, length=D)
    shared = amb - rain_only
    L_ = vo + (fx + rain_only + shared) * duck * db(2)
    R_ = vo + (fx + (ambR - rain_only - shared) + shared) * duck * db(2)
    musst = pb.Pedalboard([pb.Reverb(room_size=0.5, damping=0.5, wet_level=0.0, dry_level=1.0, width=1.0)])(np.stack([mus, np.roll(mus, 311)]), SR)
    L_ = L_ + musst[0] * duck; R_ = R_ + musst[1] * duck
    st = np.stack([L_, R_], 1).astype(np.float64)
    lm = meter.integrated_loudness(st)
    st *= db(-14.0 - lm)
    lim = pb.Pedalboard([pb.Limiter(threshold_db=-2.0, release_ms=150)])(st.T.astype(np.float32), SR).T
    pk = np.abs(lim).max()
    lim = lim * (db(-1.2) / pk if pk > db(-1.2) else 1.0)
    fade = np.ones(n, np.float32); fade[-int(0.6 * SR):] = np.linspace(1, 0, int(0.6 * SR)) ** 2
    st = lim * fade[:, None]
    lf = meter.integrated_loudness(st.astype(np.float64))
    if lf > -14.0:
        st = st * db(-14.0 - lf)
    mix = st[:, 0]
    import soundfile as sf
    sf.write(f'{OUT}/clip_audio.wav', st, SR, subtype='PCM_24')
    print('loudness', round(meter.integrated_loudness(st.astype(np.float64)), 2), 'peak dB', round(20 * np.log10(np.abs(mix).max()), 2))


GB_PER_WORKER = 2.5


def frame_chunks():
    """The frames as contiguous chunks in film order, one per worker. CLIP_FRAMES=N renders only the first N."""
    N = int((T1 - T0) * FPS)
    if os.environ.get('CLIP_FRAMES'):
        N = max(1, min(N, int(os.environ['CLIP_FRAMES'])))
    n = min(os.cpu_count() or 2, 8)
    try:    # a worker holds about GB_PER_WORKER GB: never start more than this computer's memory can take
        ram = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / 2 ** 30
        n = min(n, max(1, int((ram - 2) / GB_PER_WORKER)))
    except (ValueError, OSError, AttributeError):
        pass
    if os.environ.get('CLIP_WORKERS'):
        n = max(1, int(os.environ['CLIP_WORKERS']))
    n = min(n, N)
    return [(i, list(range(N * i // n, N * (i + 1) // n))) for i in range(n)]


def prebuild():
    """Paint and cache the plates and pages once, before the workers load them. It runs in a process of its
    own, so its memory is handed back before the workers start."""
    setup(); captions()


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else ''
    if what == 'video':
        import multiprocessing as mp
        ctx = mp.get_context('spawn')
        chunks = frame_chunks()
        print(f'{sum(len(c) for _, c in chunks)} frames, {len(chunks)} workers', flush=True)
        pre = ctx.Process(target=prebuild)
        pre.start(); pre.join()
        if pre.exitcode != 0:
            sys.exit('painting the plates failed')
        with ctx.Pool(len(chunks)) as pl:
            parts = pl.map(worker, chunks)
        with open(f'{OUT}/parts.txt', 'w') as f:
            for p in parts:
                f.write(f"file '{os.path.basename(p)}'\n")
        subprocess.run([ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/parts.txt', '-c', 'copy', f'{OUT}/clip_video.mp4'], check=True)
        print('video done')
    elif what == 'audio':
        audio()
    elif what == 'mux':
        final = f'{OUT}/bamberg_test_clip.mp4'
        subprocess.run([ffmpeg_exe(), '-y', '-loglevel', 'error', '-i', f'{OUT}/clip_video.mp4', '-i', f'{OUT}/clip_audio.wav', '-c:v', 'copy',
                        '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', final], check=True)
        print('mux done')
        copy = os.path.join(os.path.dirname(ROOT), 'Bamberg test clip (Mac render).mp4')
        try:
            shutil.copyfile(final, copy)
            print('copied to', copy)
        except OSError as e:
            print('could not copy the video next to the darkengine folder:', e)
            print('it is here:', final)
    else:
        print('usage: python clip_test.py audio|video|mux')
        sys.exit(1)
