"""Voice the narration line by line with the series narrator (Kokoro af_heart, directed delivery).
Writes vo/<id>.wav (48 kHz mono, dry) and vo/timing.json (per line: duration and word spans)."""
from darkroot import ROOT
import sys, os, re, json
sys.path.insert(0, ROOT + '/voice')
import numpy as np, soundfile as sf
import voices as VO
from script_bamberg import LINES, LEX_ADD
VO.LEX.update(LEX_ADD)
SR = VO.SR
os.makedirs(ROOT + '/film/vo', exist_ok=True)
k = VO.Kokoro('af_heart', ROOT + '/film/vo/cache', intone='directed')
only = set(sys.argv[1:])
out = json.load(open(ROOT + '/film/vo/timing.json')) if os.path.exists(ROOT + '/film/vo/timing.json') else {}
for lid, text, d, sp, q in LINES:
    if only and lid not in only:
        continue
    words = text.split()
    sents, cur = [], []
    for w in words:
        cur.append(w)
        if re.search(r"[.?!:]['\"’”)]*$", w):
            sents.append(cur); cur = []
    if cur:
        sents.append(cur)
    plan = [(s, sp, d, {}) for s in sents]
    takes = k.say_line(plan)
    parts, spans, t = [], [], 0.0
    for (seg, loc, extra), s in zip(takes, sents):
        parts.append(seg)
        for (a, b), w in zip(loc, s):
            spans.append([w, round(t + a, 3), round(t + b, 3)])
        t += len(seg) / SR
        if extra > 0:
            parts.append(np.zeros(int(extra * SR), np.float32)); t += extra
    a = np.concatenate(parts).astype(np.float32)
    sf.write(f'{ROOT}/film/vo/{lid}.wav', a, SR)
    out[lid] = {"dur": round(len(a) / SR, 3), "words": spans, "q": q}
    print(lid, round(len(a) / SR, 2), flush=True)
json.dump(out, open(ROOT + '/film/vo/timing.json', 'w'), indent=1)
print('total speech', round(sum(v['dur'] for v in out.values()), 1))
