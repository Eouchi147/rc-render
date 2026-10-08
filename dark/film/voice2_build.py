"""Assemble one narrator from the Chatterbox takes: for each sentence the best of three takes (fewest recognition
errors, then the most natural length), trimmed to the voice, joined with the performance's pauses.
    python voice2_build.py TAKES_DIR VOICE OUT_DIR
Writes OUT_DIR/<line>.wav (48 kHz mono) and OUT_DIR/timing.json (line duration, word spans, quote flag)."""
import sys, os, json, re
import numpy as np, soundfile as sf
from scipy.signal import resample_poly
from perf_bamberg import plan, SEEDS

SR = 48000
src, V, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
log = {d['out']: d for d in json.load(open(os.path.join(src, 'takes_log.json')))}


def trim(x, sr):
    e = np.convolve(np.abs(x), np.ones(sr // 100) / (sr // 100), mode='same')
    thr = max(e.max() * 0.02, 1e-4)
    idx = np.where(e > thr)[0]
    if len(idx) == 0:
        return x
    a, b = max(idx[0] - int(0.04 * sr), 0), min(idx[-1] + int(0.08 * sr), len(x))
    y = x[a:b].copy()
    n = int(0.01 * sr); y[:n] *= np.linspace(0, 1, n); y[-n:] *= np.linspace(1, 0, n)
    return y


def weights(words):
    return np.array([len(re.sub(r'[^A-Za-z0-9]', '', w)) + 2.5 for w in words], float)


NUM = {'1628': 'sixteen twenty eight', '30th': 'thirtieth', '55': 'fifty five', 'longstreet': 'long street'}


def norm(s):
    s = s.lower().replace('-', ' ')
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


P = plan()
for d in log.values():
    pass
lines, report = {}, []
for p in P:
    cands = []
    for sd in SEEDS:
        k = f"{V}_{p['line']}_{p['k']}_{sd}"
        if k in log and os.path.exists(os.path.join(src, k + '.wav')):
            c = dict(log[k]); c['wer'] = wer(p.get('check', p['text']), c['hyp']); cands.append(c)
    if not cands:
        continue
    durs = np.array([c['dur'] for c in cands])
    med = float(np.median(durs))
    best = min(cands, key=lambda c: (round(c['wer'], 2), abs(c['dur'] - med)))
    x, sr = sf.read(os.path.join(src, best['out'] + '.wav'), dtype='float32')
    if x.ndim > 1:
        x = x.mean(1)
    x = resample_poly(trim(x, sr), SR, sr).astype(np.float32)
    report.append((best['out'], best['wer'], best['hyp']))
    lines.setdefault(p['line'], []).append((p, x))
timing = {}
for lid, parts in lines.items():
    buf, spans, t = [], [], 0.0
    for i, (p, x) in enumerate(parts):
        words = p['text'].split()
        d = len(x) / SR
        a0, a1 = t + 0.04, t + d - 0.08          # the voiced part of the take
        w = weights(words); c = np.concatenate([[0], np.cumsum(w)]) / w.sum()
        for j, wd in enumerate(words):
            spans.append([wd, round(a0 + (a1 - a0) * c[j], 3), round(a0 + (a1 - a0) * c[j + 1], 3)])
        buf.append(x); t += d
        if i < len(parts) - 1:
            buf.append(np.zeros(int(p['hold'] * SR), np.float32)); t += p['hold']
    y = np.concatenate(buf)
    sf.write(os.path.join(out, lid + '.wav'), y, SR)
    timing[lid] = {'dur': round(len(y) / SR, 3), 'words': spans, 'q': parts[0][0]['quote'],
                   'style': [p['style'] for p, _ in parts]}
json.dump(timing, open(os.path.join(out, 'timing.json'), 'w'), indent=1)
bad = [r for r in report if r[1] > 0.15]
print(V, 'speech', round(sum(v['dur'] for v in timing.values()), 1), 's;', len(bad), 'sentences above 15% recognition error')
for r in bad:
    print('  ', r)
