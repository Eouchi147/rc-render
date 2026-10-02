#!/usr/bin/env python3
"""Long films (16:9, 1920 x 1080, 30 fps, 8 to 12 minutes) rendered in independent chunks, for the render farm.

A long film is voiced and timed once (prep), its pictures are filmed in N chunks that can run on N machines at the same time
(chunk), and the pieces are joined losslessly under the sound (assemble). Every frame is a pure function of the film clock:
a chunk replays the film from its first frame in a fast pre-roll (state only, nothing drawn), then films its own frames, so
chunk K's first frame is exactly the frame a single pass would have drawn there (no jump, no fade at the joins; `seam`
checks it byte for byte).

  python3 longjob.py prep <id> --bundle DIR [--eps files.json] [--page page.html] [--fps 30]
      voice (Kokoro, voices.py, with the TTS cache), timeline, captions and the mix. Writes the bundle:
      DIR/job.json (timing, captions, camera path, HUD data, ~100 KB), DIR/page.html (the film's page), DIR/mix.wav.
      A chunk machine needs only job.json and page.html (plus this repo for fonts); assemble needs mix.wav.
  python3 longjob.py chunk K N --bundle DIR [--keep-edges 1]
      films frames [(K-1)*n/N, K*n/N) (K = 1..N, n = all frames) straight into ffmpeg (no frames on disk) with the film look,
      and writes DIR/seg_K_of_N.mp4 (silent H.264) and DIR/seg_K_of_N.json (frame range, timing).
  python3 longjob.py assemble --bundle DIR [--out OUT.mp4]
      checks every segment is there and contiguous, concatenates them (stream copy), muxes mix.wav (AAC 192k), checks
      frames, duration and loudness, and writes OUT (default DIR/<id>.mp4), <id>.chapters.txt, <id>.description.txt, qa.json.
  python3 longjob.py seam K N --bundle DIR           (needs chunks K-1 and K run with --keep-edges 1)
      re-films the two frames either side of the join before chunk K in one pass and compares them with the chunks' own.
  python3 longjob.py all <id> --bundle DIR --chunks N [--out OUT.mp4] [--eps ...] [--page ...]
      prep, every chunk in turn, assemble (one machine).

Where the episode and page come from: --eps (default $RC_FILMS_EPS, else episodes/files.json) and --page (default
$RC_FILMS_OUT/<id>.html when it exists, else the episode's "site"). `python3 reel.py <id>` on a 16:9 episode runs `all` with
RC_LONG_CHUNKS chunks (default 1). See films/long/LONG_ENGINE.md.
"""
import argparse, asyncio, glob, hashlib, json, os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import reel as R

FONTS = os.path.join(HERE, "fonts")
CHROME_ARGS = ["--no-sandbox", "--disable-dev-shm-usage", "--run-all-compositor-stages-before-draw", "--disable-checker-imaging", "--disable-partial-raster",
               "--disable-new-content-rendering-timeout", "--deterministic-mode", "--force-gpu-mem-available-mb=4096", "--max-tiles-for-interest-area=4096",
               "--default-tile-width=2048", "--default-tile-height=2048"]


# ================================================================== prep
def load_ep(id_, eps=None):
    eps = eps or os.environ.get("RC_FILMS_EPS") or os.path.join(ROOT, "episodes", "files.json")
    E = {e["id"]: e for e in json.load(open(eps, encoding="utf-8"))}
    return E[id_]


def page_of(ep, page=None):
    if page:
        return os.path.abspath(page)
    sb = os.environ.get("RC_FILMS_OUT")
    if sb and os.path.exists(os.path.join(sb, ep["id"] + ".html")):
        return os.path.join(sb, ep["id"] + ".html")
    return os.path.join(ROOT, ep["site"])


def make_voice(ep, cache, who=None, speed=None, engine="kokoro"):
    """Exactly reel.py's choice of voice (voices.py is the authority on how the narrator sounds)."""
    VO = R.VO
    who = who or ep.get("voice", R.NARRATOR)
    if engine == "elevenlabs":
        voice = R.ElevenVoice(speed or 1.0, cache); who = "archivist"
    elif who in VO.CAST:
        voice = VO.engine(VO.CAST[who], cache); voice.speed = speed or VO.CAST[who]["speed"]
    else:
        voice = VO.Kokoro(who, cache); voice.speed = speed or 0.98; who = "archivist"
    R.mix.character = who
    return voice


def prep_ep(ep, bundle, page=None, fps=R.FPS16, cache=None, who=None, speed=None, engine="kokoro"):
    assert ep.get("aspect") == "16:9", (ep["id"], "not a 16:9 film")
    os.makedirs(bundle, exist_ok=True)
    src = page_of(ep, page)
    shutil.copyfile(src, os.path.join(bundle, "page.html"))
    voice = make_voice(ep, cache or os.path.join(ROOT, "out", "work", "tts-cache"), who, speed, engine)
    print("voice…", flush=True)
    beats, words, clips, end, _ = R.build(ep, voice, voice.speed)
    total = end + R.LONG_TAIL
    caps = R.captions16(words)
    sfx, stamps, counts, kicks, gos = R.events(ep, beats, words, end)
    sfx.sort()
    print(f"  {total:.1f} s, {len(words)} words, {len(caps)} captions, {len(sfx)} sound cues", flush=True)
    work = os.path.join(bundle, "_mix"); os.makedirs(work, exist_ok=True)
    audio = R.mix(ep, clips, beats, sfx, end, total, work)
    os.replace(audio, os.path.join(bundle, "mix.wav")); shutil.rmtree(work, ignore_errors=True)
    mv = R.moves(beats, gos)
    D = R.long_data(ep, beats, caps, stamps, counts, kicks, end, getattr(R.events, "cams", []), fps)
    job = {"id": ep["id"], "fps": fps, "total": round(total, 4), "end": end, "n": int(total * fps), "mv": mv, "D": D,
           "page_md5": hashlib.md5(open(src, "rb").read()).hexdigest(),
           "youtube": {"title": ep.get("yt_title") or ep.get("title", ""), "description": ep.get("description", ""),
                       "chapters": R.youtube_chapters(D["chapters"], total)}}
    tmp = os.path.join(bundle, "job.json.tmp"); json.dump(job, open(tmp, "w"), ensure_ascii=False); os.replace(tmp, os.path.join(bundle, "job.json"))
    print(f"prep done: {job['n']} frames at {fps} fps, {len(D['chapters'])} chapters -> {bundle}", flush=True)
    return job


# ================================================================== chunk
def frame_range(n, k, N):
    assert 1 <= k <= N, (k, N)
    return (k - 1) * n // N, k * n // N


def story_y(mv, t):
    """The story position at film time t (exactly reel.film's camera path: smootherstep glides between [go:] targets)."""
    y = float(mv[0][1])
    for (m0, ch, dur) in mv:
        if t < m0:
            break
        if dur <= 0 or t >= m0 + dur:
            y = float(ch)
        else:
            u = (t - m0) / dur; u = u * u * u * (u * (u * 6 - 15) + 10)
            y = y + (ch - y) * u
    return y


async def film(bundle, a, b, put, log=True, pick=None):
    """Film frames a..b-1 of the bundle's film; frames before a are replayed as state only. put(i, jpeg_bytes) per frame.
    pick: a set of frames to film (QA stills); every other frame is replayed as state only."""
    from playwright.async_api import async_playwright
    job = json.load(open(os.path.join(bundle, "job.json"), encoding="utf-8"))
    fps, story, mv = job["fps"], job["id"], job["mv"]
    async with async_playwright() as pw:
        extra = {"args": CHROME_ARGS}
        if os.environ.get("RC_CHROME_LIB"):
            extra["env"] = {**os.environ, "LD_LIBRARY_PATH": os.environ["RC_CHROME_LIB"]}
        br = await (pw.chromium.launch(executable_path=R.CHROME, **extra) if R.CHROME else pw.chromium.launch(**extra))
        ctx = await br.new_context(viewport={"width": R.W16, "height": R.H16}, device_scale_factor=R.DPR16, color_scheme="dark")
        await ctx.route(re.compile(r"^https?://"), lambda r: r.abort())
        await ctx.add_init_script(R.VT)
        pg = await ctx.new_page(); errs = []
        pg.on("pageerror", lambda e_: errs.append(str(e_)))
        await pg.goto("file://" + os.path.abspath(os.path.join(bundle, "page.html")) + "#films")
        for _ in range(20):
            await pg.evaluate("__step(50)")
        await pg.add_style_tag(content=R.css16(FONTS))
        await pg.evaluate("window.dispatchEvent(new Event('resize'))")
        for _ in range(6):
            await pg.evaluate("__step(50)")
        await pg.evaluate(R.OVERLAY16, job["D"])
        await pg.evaluate("document.fonts && document.fonts.ready")
        keys = await pg.evaluate(f"SY.keys('{story}')")
        snap, setp = f"SY.snap&&SY.snap('{story}')", f"SY.film('{story}',P)"
        await pg.evaluate(f"window.scrollTo(0,{keys[0] + 4});window.dispatchEvent(new Event('scroll'));" + setp.replace("P", str(float(mv[0][1]))) + ";" + snap)
        for _ in range(110):
            await pg.evaluate("__step(33.3)")
        await pg.evaluate("window.__kitRewind && __kitRewind()")     # frame 0 is the start of every build-in
        dt, last_y, batch, settled = 1000 / fps, None, [], False
        for i in range(b):
            t = i / fps
            js = ""
            y = story_y(mv, t)
            if y != last_y:
                jump = last_y is not None and abs(y - last_y) > .5 and y == round(y)
                js += setp.replace("P", f"{y:.5f}") + ";" + (snap + ";" if jump else ""); last_y = y
            js += f"__step({dt});__frame({t:.4f},{(i * 7919) % 2147483647})"
            if i < a or (pick is not None and i not in pick):     # pre-roll: state only, in batches inside the page
                batch.append(js)
                if len(batch) >= 240:
                    await pg.evaluate("()=>{window.__pre=1;try{" + ";".join(batch) + "}finally{window.__pre=0}}"); batch.clear()
                continue
            if batch:
                await pg.evaluate("()=>{window.__pre=1;try{" + ";".join(batch) + "}finally{window.__pre=0}}"); batch.clear()
            if not settled:
                await asyncio.sleep(.3); settled = True
            await pg.evaluate("()=>{" + js + "}")
            put(i, await pg.screenshot(type="jpeg", quality=93))
            if log and (i - a) % (fps * 10) == 0:
                print(f"  frame {i} ({i - a + 1}/{b - a})", flush=True)
        await br.close()
        if errs:
            print("page errors:", errs[:3], flush=True)
        return errs


def stills(bundle, times):
    """QA stills at film times (seconds): DIR/stills/<t>.jpg, each frame exactly as the film draws it."""
    job = json.load(open(os.path.join(bundle, "job.json"), encoding="utf-8"))
    fr = sorted({min(job["n"] - 1, int(round(t * job["fps"]))) for t in times})
    d = os.path.join(bundle, "stills"); os.makedirs(d, exist_ok=True); out = []
    def put(i, jpg):
        p = os.path.join(d, f"{i / job['fps']:07.2f}.jpg"); open(p, "wb").write(jpg); out.append(p)
    asyncio.run(film(bundle, 0, fr[-1] + 1, put, log=False, pick=set(fr)))
    print("\n".join(out)); return out


def chunk(bundle, k, N, keep_edges=0):
    job = json.load(open(os.path.join(bundle, "job.json"), encoding="utf-8"))
    fps, n = job["fps"], job["n"]
    a, b = frame_range(n, k, N)
    seg = os.path.join(bundle, f"seg_{k}_of_{N}.mp4")
    print(f"chunk {k} of {N}: frames {a}..{b - 1} ({(b - a) / fps:.1f} s of film)", flush=True)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
                           "-filter_complex", R._vf16(fps), "-map", "[v]", "-r", str(fps), *R.X264, seg + ".part.mp4"], stdin=subprocess.PIPE)
    edges = os.path.join(bundle, "edges"); os.makedirs(edges, exist_ok=True) if keep_edges else None
    got = []

    def put(i, jpg):
        ff.stdin.write(jpg); got.append(i)
        if keep_edges and (i < a + keep_edges or i >= b - keep_edges):
            open(os.path.join(edges, f"{i:06d}.jpg"), "wb").write(jpg)
    t0 = time.time()
    errs = asyncio.run(film(bundle, a, b, put))
    ff.stdin.close(); rc = ff.wait()
    secs = time.time() - t0
    assert rc == 0 and got == list(range(a, b)), ("chunk failed", rc, len(got), b - a)
    os.replace(seg + ".part.mp4", seg)
    nf = probe_frames(seg)
    assert nf == b - a, ("segment frame count", nf, b - a)
    info = {"k": k, "N": N, "a": a, "b": b, "frames": nf, "seconds": round(secs, 1), "film_seconds": round((b - a) / fps, 3),
            "s_per_s": round(secs / ((b - a) / fps), 2), "page_errors": errs, "page_md5": job.get("page_md5")}
    json.dump(info, open(os.path.join(bundle, f"seg_{k}_of_{N}.json"), "w"), indent=1)
    print(f"chunk {k} of {N} done: {nf} frames in {secs:.0f} s ({info['s_per_s']} s per second of film) -> {seg}", flush=True)
    return info


def probe_frames(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries", "stream=nb_read_packets",
                        "-of", "csv=p=0", p], capture_output=True, text=True)
    return int(r.stdout.strip().split(",")[0])


def seam(bundle, k, N):
    """The join before chunk k: frames a-1 and a filmed in one continuous pass, compared with the chunks' own (--keep-edges)."""
    job = json.load(open(os.path.join(bundle, "job.json"), encoding="utf-8"))
    a, _ = frame_range(job["n"], k, N)
    assert k > 1
    got = {}
    asyncio.run(film(bundle, a - 1, a + 1, lambda i, j: got.__setitem__(i, j), log=False))
    ok = True
    for i in (a - 1, a):
        p = os.path.join(bundle, "edges", f"{i:06d}.jpg")
        same = os.path.exists(p) and open(p, "rb").read() == got[i]
        ok &= same
        print(f"  frame {i}: {'identical' if same else 'DIFFERENT (or missing)'} to the chunk's own", flush=True)
    print(f"seam before chunk {k} of {N}: {'seamless (byte-identical frames)' if ok else 'NOT identical'}", flush=True)
    return ok


# ================================================================== assemble
def loudness(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-map", "0:a", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    s = r.stderr[r.stderr.rfind("Summary:"):]
    I = re.search(r"I:\s+(-?[\d.]+) LUFS", s); P = re.search(r"Peak:\s+(-?[\d.]+) dBFS", s)
    return float(I.group(1)) if I else None, float(P.group(1)) if P else None


def assemble(bundle, out=None):
    job = json.load(open(os.path.join(bundle, "job.json"), encoding="utf-8"))
    fps, n = job["fps"], job["n"]
    infos = [json.load(open(p)) for p in glob.glob(os.path.join(bundle, "seg_*_of_*.json"))]
    Ns = {i["N"] for i in infos}
    assert len(Ns) == 1, ("segments from different splits", sorted(Ns))
    N = Ns.pop()
    infos.sort(key=lambda i: i["k"])
    assert [i["k"] for i in infos] == list(range(1, N + 1)), ("missing chunks", [i["k"] for i in infos], N)
    pos = 0
    for i in infos:
        assert i["a"] == pos and i["frames"] == i["b"] - i["a"], ("gap or overlap", i)
        assert os.path.exists(os.path.join(bundle, f"seg_{i['k']}_of_{N}.mp4")), i
        pos = i["b"]
    assert pos == n, ("frames", pos, n)
    out = out or os.path.join(bundle, job["id"] + ".mp4")
    lst = os.path.join(bundle, "concat.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(os.path.join(bundle, f'seg_{i}_of_{N}.mp4'))}'\n" for i in range(1, N + 1)))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", os.path.join(bundle, "mix.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    os.remove(lst)
    # ---- QA: every frame there, the length right, the loudness on target
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate,duration:format=duration",
                                    "-of", "json", out], capture_output=True, text=True).stdout)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video"); au = next(s for s in pr["streams"] if s["codec_type"] == "audio")
    frames = probe_frames(out)
    I, peak = loudness(out)
    qa = {"file": out, "frames": frames, "frames_expected": n, "size": [v["width"], v["height"]], "fps": v["r_frame_rate"],
          "video_s": float(v["duration"]), "audio_s": float(au["duration"]), "expected_s": round(n / fps, 3), "loudness_lufs": I, "peak_dbfs": peak,
          "chunks": [{k: i[k] for k in ("k", "a", "b", "seconds", "s_per_s")} for i in infos], "mb": round(os.path.getsize(out) / 1e6, 1)}
    qa["ok"] = (frames == n and abs(qa["video_s"] - n / fps) < .05 and qa["audio_s"] >= qa["video_s"] - .1 and (v["width"], v["height"]) == (1920, 1080)
                and I is not None and abs(I + 14) <= 1.5 and peak is not None and peak <= -0.5)
    base = os.path.splitext(out)[0]
    yt = job.get("youtube", {})
    open(base + ".chapters.txt", "w").write(yt.get("chapters", "") + "\n")
    if yt.get("description"):
        open(base + ".description.txt", "w").write(yt["title"] + "\n\n" + yt["description"].replace("{chapters}", yt.get("chapters", "")) + "\n")
    json.dump(qa, open(os.path.join(bundle, "qa.json"), "w"), indent=1)
    print(json.dumps(qa, indent=1), flush=True)
    print(("assembled: " if qa["ok"] else "assembled WITH QA PROBLEMS: ") + out, flush=True)
    return qa


def run_all(ep, bundle, N, out=None, page=None, fps=R.FPS16, cache=None, keep_edges=0, **vk):
    prep_ep(ep, bundle, page, fps, cache, **vk)
    for k in range(1, N + 1):
        chunk(bundle, k, N, keep_edges)
    return assemble(bundle, out)


def from_reel(ep, a):
    """reel.py <id> on a 16:9 episode: the whole film on this machine (RC_LONG_CHUNKS chunks in turn) into <out>/<id>.mp4."""
    bundle = os.path.join(a.out, "work", ep["id"] + "-16x9")
    return run_all(ep, bundle, int(os.environ.get("RC_LONG_CHUNKS", "1")), os.path.join(a.out, ep["id"] + ".mp4"),
                   fps=int(os.environ.get("RC_LONG_FPS", R.FPS16)), cache=os.path.join(a.out, "work", "tts-cache"),
                   who=a.voice, speed=a.speed, engine=a.engine)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prep"); p.add_argument("id"); p.add_argument("--bundle", required=True); p.add_argument("--eps"); p.add_argument("--page")
    p.add_argument("--fps", type=int, default=R.FPS16); p.add_argument("--tts-cache")
    c = sub.add_parser("chunk"); c.add_argument("k", type=int); c.add_argument("N", type=int); c.add_argument("--bundle", required=True); c.add_argument("--keep-edges", type=int, default=0)
    s = sub.add_parser("seam"); s.add_argument("k", type=int); s.add_argument("N", type=int); s.add_argument("--bundle", required=True)
    q = sub.add_parser("stills"); q.add_argument("--bundle", required=True); q.add_argument("--at", type=float, nargs="+", required=True)
    m = sub.add_parser("assemble"); m.add_argument("--bundle", required=True); m.add_argument("--out")
    w = sub.add_parser("all"); w.add_argument("id"); w.add_argument("--bundle", required=True); w.add_argument("--chunks", type=int, default=1); w.add_argument("--out")
    w.add_argument("--eps"); w.add_argument("--page"); w.add_argument("--fps", type=int, default=R.FPS16); w.add_argument("--tts-cache"); w.add_argument("--keep-edges", type=int, default=0)
    a = ap.parse_args()
    if a.cmd == "prep":
        prep_ep(load_ep(a.id, a.eps), a.bundle, a.page, a.fps, a.tts_cache)
    elif a.cmd == "chunk":
        chunk(a.bundle, a.k, a.N, a.keep_edges)
    elif a.cmd == "stills":
        stills(a.bundle, a.at)
    elif a.cmd == "seam":
        sys.exit(0 if seam(a.bundle, a.k, a.N) else 1)
    elif a.cmd == "assemble":
        sys.exit(0 if assemble(a.bundle, a.out)["ok"] else 1)
    elif a.cmd == "all":
        sys.exit(0 if run_all(load_ep(a.id, a.eps), a.bundle, a.chunks, a.out, a.page, a.fps, a.tts_cache, a.keep_edges)["ok"] else 1)


if __name__ == "__main__":
    main()
