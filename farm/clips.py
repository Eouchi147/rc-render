#!/usr/bin/env python3
"""clips.py <long film id> [clip ids...]: the chapter clips of one long film, on a GitHub runner (workflow clips.yml).

The long film comes from the release once; then reels/free/clip.py cuts each clip listed for it in yt/clips.json
(each chapter, start to start, in a vertical frame with its question above). Output: build/clips/<clip id>.mp4 and
build/clips/<film>.clips.json (the exact cuts and the checks). Exits 1 if any clip fails a check:
both cuts found in the sound, length within 2.5 s of the listed chapter, loudness -16 to -12 LUFS, true peak under -0.5 dB.
"""
import json, os, subprocess, sys

TOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.environ.get("GH_REPO") or "Eouchi147/rc-render"
REL = f"https://github.com/{REPO}/releases/download/films/"


def main():
    fid, only = sys.argv[1], set(sys.argv[2:])
    L = [c for c in json.load(open(os.path.join(TOP, "yt", "clips.json"), encoding="utf-8"))["clips"]
         if c["film"] == fid and (not only or c["id"] in only)]
    if not L:
        sys.exit(f"no clips listed for {fid}")
    out_dir = os.path.join(TOP, "build", "clips"); os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(TOP, "build", fid + ".mp4")
    if not os.path.exists(src):
        subprocess.run(["curl", "-fsSL", "--retry", "8", "--retry-all-errors", "--retry-delay", "3", "-o", src, REL + fid + ".mp4"], check=True)
    rows, bad = [], 0
    for c in sorted(L, key=lambda c: c["k"]):
        out = os.path.join(out_dir, c["id"] + ".mp4")
        r = subprocess.run([sys.executable, os.path.join(TOP, "reels", "free", "clip.py"), "--src", src, "--at", str(c["at"]), "--to", str(c["to"]),
                            "--title", c["title"], "--kicker", c["kicker"], "--foot", c["foot"], "--out", out], capture_output=True, text=True)
        if r.returncode != 0:
            if os.path.exists(out):
                os.remove(out)
            print(f"FAILED {c['id']}:\n{r.stderr[-2000:]}", flush=True); bad += 1
            rows.append({"id": c["id"], "ok": False, "error": r.stderr[-400:]}); continue
        q = json.loads(r.stdout.strip().splitlines()[-1])
        want = c["to"] - c["at"]
        why = [w for w, ok in [("cut not found in the sound", all(q["found"])),
                               (f"length {q['dur']} s for a {want} s chapter", abs(q["dur"] - want) <= 2.5),
                               (f"loudness {q['lufs']} LUFS", q["lufs"] is not None and -16 <= q["lufs"] <= -12),
                               (f"peak {q['peak']} dB", q["peak"] is not None and q["peak"] <= -0.5)] if not ok]
        q.update({"id": c["id"], "ok": not why, "why": why})
        rows.append(q); bad += bool(why)
        print(("OK  " if not why else "BAD ") + json.dumps(q), flush=True)
    json.dump({"film": fid, "clips": rows}, open(os.path.join(out_dir, fid + ".clips.json"), "w"), indent=1)
    os.remove(src)
    print(f"{fid}: {len(rows) - bad} of {len(rows)} clips ok", flush=True)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
