"""Glitch check for a rendered reel: flags sudden picture jumps that are not planned cuts.
usage: python3 qa.py out/khafre-pillars.mp4 out/work/khafre-pillars-v2/timeline.json"""
import json, subprocess, sys
import numpy as np

mp4, tl = sys.argv[1], json.load(open(sys.argv[2]))
w, h = 90, 160
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)
num, den = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", mp4], capture_output=True, text=True).stdout.strip().split("/")
FPS = float(num) / float(den)
# ignore the caption band and the top brand line, they change on every word by design
core = fr[:, int(h * .06):int(h * .62), :]
d = np.abs(np.diff(core, axis=0)).mean(axis=(1, 2))
cuts = [b["t0"] for b in tl["beats"][1:] if b["visual"].get("cut")] + [tl["end"]] + [s["t"] for s in tl.get("stamps", [])]
med = np.median(d) + 1e-3
bad = []
for i, v in enumerate(d):
    t = (i + 1) / FPS
    if v > max(6 * med, 4.0) and not any(-0.05 < t - c < 0.12 for c in cuts):
        bad.append((round(t, 2), round(float(v), 1)))
# flicker: a frame unlike both neighbours while they agree with each other (missing tiles, popping labels)
m = lambda i, j: float(np.abs(core[i] - core[j]).mean())
flk = [((i + 0) / FPS, round(m(i - 1, i) + m(i, i + 1) - m(i - 1, i + 1), 2)) for i in range(1, len(core) - 1)]
flk = [f for f in flk if f[1] > 1.5 and not any(-0.05 < f[0] - c < 0.12 for c in cuts)]
def windows(ts):
    g = []
    for t in sorted(ts):
        if g and t - g[-1][1] < 0.3:
            g[-1][1] = t
        else:
            g.append([t, t])
    return [(round(a, 2), round(b, 2)) for a, b in g]
print(f"{len(fr)} frames, median change {med:.2f}, planned cuts {len(cuts)}, unplanned jumps: {len(bad)}, flicker frames: {len(flk)}")
print("  jump windows:", windows([b[0] for b in bad]))
print("  flicker windows:", windows([f[0] for f in flk]))
