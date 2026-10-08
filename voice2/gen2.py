"""Shard of a Chatterbox job list (Resemble AI, MIT licence), CPU. Each take is checked by speech recognition
(faster-whisper base.en): the transcript and its word error rate are logged so the best take can be chosen.
    python gen2.py jobs.json out SHARD NSHARDS"""
import sys, os, json, time, re
import torch, torchaudio as ta
from chatterbox.tts import ChatterboxTTS
from faster_whisper import WhisperModel

jobs = json.load(open(sys.argv[1]))
out, k, n = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
os.makedirs(out, exist_ok=True)
torch.set_num_threads(os.cpu_count() or 4)
model = ChatterboxTTS.from_pretrained(device='cpu')
asr = WhisperModel('base.en', device='cpu', compute_type='int8')
base = os.path.dirname(os.path.abspath(sys.argv[1]))


def norm(s):
    s = s.lower().replace('-', ' ')
    return re.sub(r"[^a-z0-9' ]", ' ', s).split()


def wer(ref, hyp):
    r, h = norm(ref), norm(hyp)
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        p, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (r[i - 1] != h[j - 1]))
    return d[len(h)] / max(len(r), 1)


log = []
for i, j in enumerate(jobs['takes']):
    if i % n != k:
        continue
    t = time.time()
    torch.manual_seed(int(j.get('seed', 1)))
    kw = dict(exaggeration=float(j.get('ex', 0.5)), cfg_weight=float(j.get('cfg', 0.5)), temperature=float(j.get('temp', 0.75)))
    if j.get('ref'):
        kw['audio_prompt_path'] = os.path.join(base, j['ref'])
    wav = model.generate(j['text'], **kw)
    path = os.path.join(out, j['out'] + '.wav')
    ta.save(path, wav, model.sr)
    segs, _ = asr.transcribe(path, beam_size=3, language='en')
    hyp = ' '.join(s.text for s in segs).strip()
    log.append({'out': j['out'], 'secs': round(time.time() - t, 1), 'dur': round(wav.shape[-1] / model.sr, 2),
                'hyp': hyp, 'wer': round(wer(j.get('check', j['text']), hyp), 3)})
    print(log[-1], flush=True)
json.dump(log, open(os.path.join(out, f'log_{k:02d}.json'), 'w'), indent=1)
