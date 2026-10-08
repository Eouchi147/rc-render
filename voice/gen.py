"""Speak a list of narration takes with Chatterbox (Resemble AI, MIT licence) on CPU.
jobs.json: {"release": tag, "takes": [{"out": name, "text": ..., "ref": wav or null, "ex": emotion 0.25..1.0,
            "cfg": pace/adherence 0.2..0.7, "temp": 0.8, "seed": 1}]}"""
import sys, os, json, time
import torch, torchaudio as ta
from chatterbox.tts import ChatterboxTTS

jobs = json.load(open(sys.argv[1]))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
torch.set_num_threads(os.cpu_count() or 4)
model = ChatterboxTTS.from_pretrained(device='cpu')
base = os.path.dirname(os.path.abspath(sys.argv[1]))
log = []
for j in jobs['takes']:
    t = time.time()
    torch.manual_seed(int(j.get('seed', 1)))
    ref = j.get('ref')
    kw = dict(exaggeration=float(j.get('ex', 0.5)), cfg_weight=float(j.get('cfg', 0.5)), temperature=float(j.get('temp', 0.8)))
    if ref:
        kw['audio_prompt_path'] = os.path.join(base, ref)
    wav = model.generate(j['text'], **kw)
    ta.save(os.path.join(out, j['out'] + '.wav'), wav, model.sr)
    log.append({'out': j['out'], 'secs': round(time.time() - t, 1), 'dur': round(wav.shape[-1] / model.sr, 2)})
    print(log[-1], flush=True)
json.dump(log, open(os.path.join(out, 'takes_log.json'), 'w'), indent=1)
