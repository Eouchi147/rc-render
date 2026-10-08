"""Assemble the keeper's narration from the Chatterbox takes.
For each recording unit: the best of five takes (words right first, then the ending directed: landing or suspended,
then a natural length). A unit that joins several phrases is cut back at its silences, and every pause is set to the
direction (direct_bamberg.py). Optional TEMPO (< 1 = quicker, pitch kept, Rubber Band) to fit the film.
    python voice2_build.py TAKES_DIR VOICE OUT_DIR [TEMPO]
Writes OUT_DIR/<line>.wav (48 kHz mono) and OUT_DIR/timing.json (line duration, word spans, quote flag)."""
import sys, os, json, re
import numpy as np, soundfile as sf
from scipy.signal import resample_poly
import parselmouth
from perf_bamberg import plan, SEEDS

SR = 48000
src, V, out = sys.argv[1], sys.argv[2], sys.argv[3]
TEMPO = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
os.makedirs(out, exist_ok=True)
log = {d['out']: d for d in json.load(open(os.path.join(src, 'takes_log.json')))}
NUM = {'1628': 'sixteen twenty eight', '1781': 'seventeen eighty one', '100,000': 'a hundred thousand', '100000': 'a hundred thousand',
       '55': 'fifty five', '8': 'eight', '1 ': 'one ', '1014': 'ten fourteen', ' 10 14 ': ' ten fourteen '}


def norm(s):
    s = ' ' + s.lower().replace('-', ' ') + ' '
    for a, b in NUM.items():
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9' ]", ' ', s).split()


def wer(ref, hyp):
    r, h = norm(ref), norm(hyp)
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        p, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (r[i - 1] != h[j - 1]))
    return d[len(h)] / max(len(r), 1)


def landing(x, sr):
    """How much the voice falls over the last stretch (semitones; positive = it lands)."""
    try:
        f0 = parselmouth.Sound(x.astype(np.float64), sr).to_pitch(time_step=0.01, pitch_floor=60, pitch_ceiling=300).selected_array['frequency']
        v = f0[f0 > 0]
        if len(v) < 12:
            return 0.0
        n = max(4, len(v) // 4)
        return float(12 * np.log2(np.median(v[-2 * n:-n]) / np.median(v[-n:])))
    except Exception:
        return 0.0


def env(x, sr):
    return np.convolve(np.abs(x), np.ones(sr // 100) / (sr // 100), mode='same')


def trim(x, sr):
    e = env(x, sr)
    idx = np.where(e > max(e.max() * 0.02, 1e-4))[0]
    if len(idx) == 0:
        return x
    a, b = max(idx[0] - int(0.04 * sr), 0), min(idx[-1] + int(0.08 * sr), len(x))
    y = x[a:b].copy()
    n = int(0.01 * sr); y[:n] *= np.linspace(0, 1, n); y[-n:] *= np.linspace(1, 0, n)
    return y


def gaps(x, sr, min_len=0.07):
    """Silent stretches inside the take: [(start, end)] in seconds."""
    e = env(x, sr)
    quiet = e < max(e.max() * 0.03, 1e-4)
    out, i, n = [], 0, len(x)
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if (j - i) / sr >= min_len and i > 0 and j < n:
                out.append((i / sr, j / sr))
            i = j
        else:
            i += 1
    return out


def split(x, phrases):
    """Cut a unit into its phrases at the silences nearest where each phrase should end (by letters)."""
    if len(phrases) == 1:
        return [x]
    L = np.array([len(p['text']) for p in phrases], float)
    cum = np.cumsum(L)[:-1] / L.sum()
    d = len(x) / SR
    G = gaps(x, SR)
    cuts, used = [], set()
    for c in cum:
        if not G:
            cuts.append(c * d); continue
        k = min((k for k in range(len(G)) if k not in used), key=lambda k: abs((G[k][0] + G[k][1]) / 2 - c * d), default=None)
        if k is None:
            cuts.append(c * d); continue
        used.add(k)
        cuts.append(G[k])
    segs, t0 = [], 0.0
    for c in cuts:
        a, b = (c, c) if not isinstance(c, tuple) else c
        segs.append(x[int(t0 * SR):int((a + 0.03) * SR)])
        t0 = max(b - 0.03, a)
    segs.append(x[int(t0 * SR):])
    return segs


P = plan()
lines, report = {}, []
for p in P:
    cands = []
    for sd in SEEDS:
        k = f"{V}_{p['line']}_{p['k']}_{sd}"
        if k in log and os.path.exists(os.path.join(src, k + '.wav')):
            c = dict(log[k]); c['wer'] = wer(p['check'], c['hyp']) + (0.5 if '//' in c['hyp'] else 0.0)   # '//' = noise the recogniser heard
            x, sr = sf.read(os.path.join(src, k + '.wav'), dtype='float32')
            x = x.mean(1) if x.ndim > 1 else x
            c['x'], c['sr'] = x, sr
            c['fall'] = landing(trim(x, sr), sr)
            cands.append(c)
    if not cands:
        continue
    med = float(np.median([c['dur'] for c in cands]))
    want = p['lands']

    def score(c):
        prosody = -c['fall'] if want else max(c['fall'] - 1.0, 0)
        need = len(p['phrases']) - 1                  # a joined unit needs a real breath at each cut
        miss = max(0, need - len(gaps(trim(c['x'], c['sr']), c['sr'], 0.09))) if need else 0
        return (round(c['wer'], 2), miss, prosody * 0.25 + abs(c['dur'] - med) / max(med, 0.5))
    best = min(cands, key=score)
    x = resample_poly(trim(best['x'], best['sr']), SR, best['sr']).astype(np.float32)
    if TEMPO != 1.0:
        import pedalboard as pb
        x = pb.time_stretch(x[None, :], SR, stretch_factor=1.0 / TEMPO)[0].astype(np.float32)
    report.append((best['out'], round(best['wer'], 2), best['hyp'], round(best['fall'], 1)))
    for ph, seg in zip(p['phrases'], split(x, p['phrases'])):
        lines.setdefault(p['line'], []).append((ph, seg))
quote = {p['line']: p['quote'] for p in P}
timing = {}
for lid, parts in lines.items():
    buf, spans, t = [], [], 0.0
    for i, (ph, x) in enumerate(parts):
        words = ph['text'].split()
        d = len(x) / SR
        a0, a1 = t + 0.03, t + d - 0.05
        w = np.array([len(re.sub(r'[^A-Za-z0-9]', '', wd)) + 2.5 for wd in words], float)
        c = np.concatenate([[0], np.cumsum(w)]) / w.sum()
        for j, wd in enumerate(words):
            spans.append([wd, round(a0 + (a1 - a0) * c[j], 3), round(a0 + (a1 - a0) * c[j + 1], 3)])
        buf.append(x); t += d
        if i < len(parts) - 1:
            h = max(ph['hold'], 0.12)
            buf.append(np.zeros(int(h * SR), np.float32)); t += h
    y = np.concatenate(buf)
    sf.write(os.path.join(out, lid + '.wav'), y, SR)
    timing[lid] = {'dur': round(len(y) / SR, 3), 'words': spans, 'q': quote[lid]}
json.dump(timing, open(os.path.join(out, 'timing.json'), 'w'), indent=1)
bad = [r for r in report if r[1] > 0.15]
print(V, 'lines', round(sum(v['dur'] for v in timing.values()), 1), 's;', len(bad), 'units above 15% recognition error')
for r in bad:
    print('  ', r)
