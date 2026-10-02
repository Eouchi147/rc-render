#!/usr/bin/env python3
"""Residual Continuum reel renderer, version 2.

One command turns an episode from episodes/episodes2.json into a finished 9:16 reel (1080x1920, 30 fps):

  * VOICE     Kokoro-82M (Apache-2.0), full-precision model with per-phoneme timings, so every caption word,
              sound effect and on-screen stamp lands on the exact syllable. Sentences are voiced one by one with
              natural pauses, a slightly slower delivery and a warm, produced vocal chain (a touch deeper, EQ,
              gentle compression, a small room). ElevenLabs, with a clone of your own voice, can replace it (--engine elevenlabs, see README).
  * PICTURES  the site's own animated scroll stories, filmed frame by frame on a virtual clock, with per-shot
              framing (push-ins, reframes, whip cuts), film grain and vignette.
  * GRAPHICS  word-by-word captions in the site's fonts, chapter kickers, evidence stamps, counters, a hook title,
              a progress bar and the verdict end card, all timed from the voice.
  * SOUND     sound effects and a score synthesised here from scratch (nothing to license): whooshes on cuts,
              booms on reveals, a stamp thud on a stamp, ticks under a counter, risers into the twist, a pad score
              that changes chord with each beat and ducks under the voice, loudness-normalised for social.

Script markup (inside a line's "say"):
  {648|six hundred and forty-eight}   show "648", say the words
  [sfx:boom]  [sfx:whoosh@-0.3]       a sound effect on the next word (optional offset in seconds)
  [stamp:RETRACTED · AUG 2026|red]    a stamp slams in on the next word (red, gold, green, blue)
  [count:648|m]                        a big counter runs up to 648 on the next word
  [k:THE CLAIM]                        a chapter kicker appears on the next word
  //                                   a longer, deliberate pause

Usage: python3 reel.py <episode-id> [--voice bm_george] [--speed 0.95] [--draft] [--only SECONDS]
       python3 reel.py --voices            (writes voice samples to choose from)
"""
import argparse, asyncio, hashlib, json, math, os, re, shutil, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NARRATOR = os.environ.get("RC_NARRATOR", "signal")   # a character from voices.CAST (see narrator-casting.html)
sys.path.insert(0, HERE)
import voices as VO


def _first(*paths):
    for x in paths:
        if x and os.path.exists(x):
            return x
    return paths[-1]


TTS_DIR = os.environ.get("RC_TTS_DIR") or _first(os.path.join(HERE, "models"), "/home/claude/tts")
MODEL = os.path.join(TTS_DIR, "kokoro-v1.0-r11.onnx")
VOICES = os.path.join(TTS_DIR, "voices-v1.0.bin")
SITE = os.path.abspath(os.environ.get("RC_SITE") or _first(os.path.join(ROOT, "..", "index.html"), "/home/claude/rc2/out/full.html", "/home/claude/rc2/out/index.html"))   # the full single page: the web shell loads its bodies over http
CHROME = _first(os.environ.get("RC_CHROME", ""), "/opt/pw-browsers/chromium", "")
SR = 48000
W, H, DPR = 540, 960, 2
VERD = {"debunked": "Ruled out", "unsupported": "Awaiting discovery", "contested": "Open question", "mixed": "Mixed record",
        "plausible": "Plausible", "strong": "Strong evidence", "solid": "Established"}
VCOL = {"debunked": "#e98a8a", "unsupported": "#c9c1ee", "contested": "#f0b06a", "mixed": "#d8c7a8",
        "plausible": "#e8c86a", "strong": "#7fd1d4", "solid": "#8fd9b0"}
STAMPC = {"red": "#ff7a6b", "gold": "#f2c76e", "green": "#8fe0b0", "blue": "#9fc6ef"}
rng = np.random.default_rng(11)


# ================================================================== script
TOK = re.compile(r"\[(\w+):([^\]]*)\]|\{([^|{}]*)\|([^{}]*)\}([^\s\[{]*)|(//)|(\S+)")


def parse(text):
    words, pend = [], []
    for m in TOK.finditer(text):
        if m.group(1):
            pend.append((m.group(1), m.group(2)))
        elif m.group(3) is not None:
            tail = m.group(5) or ""
            words.append({"disp": m.group(3) + tail, "say": m.group(4) + tail, "ev": pend, "brk": 0}); pend = []
        elif m.group(6):
            if words:
                words[-1]["brk"] = 0.6
        else:
            words.append({"disp": m.group(7), "say": m.group(7), "ev": pend, "brk": 0}); pend = []
        if words and words[-1]["disp"].startswith("^"):          # ^word: the focus of the sentence (voice only, no glow)
            words[-1]["disp"] = words[-1]["disp"][1:]; words[-1]["focus"] = True
        if words and "*" in words[-1]["disp"]:                  # *word*: the narrator leans on it, the caption glows
            words[-1]["disp"] = words[-1]["disp"].replace("*", ""); words[-1]["em"] = True
    if pend and words:
        words[-1].setdefault("ev_end", []).extend(pend)
    import heteronyms as HN
    for w in words:                                          # live@adj: the sense is for the voice and the audit, never shown
        w["disp"] = HN.display(w["disp"])
    return words


def chunks(words):
    """Each sentence is voiced on its own breath: the silences between sentences are then placed exactly where
    they belong (never inside a word), timed by the pause plan. A new direction or pace mid-line also starts one."""
    out, cur = [], []
    for w in words:
        if cur and any(k in ("p", "d") for k, _ in w["ev"]):
            out.append(cur); cur = []
        cur.append(w)
        if w["brk"] or re.search(r"[.?!…]['\"’”)*]*$", w["say"]):
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def sentences(words):
    out, cur = [], []
    for w in words:
        cur.append(w)
        if w["brk"] or re.search(r"[.?!]['\"’”)]*$", w["say"]):
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


# ================================================================== voice
class Voice:
    def __init__(self, spec, speed, cache):
        from kokoro_onnx import Kokoro
        self.k = Kokoro(MODEL, VOICES)
        self.spec, self.speed, self.cache = spec, speed, cache
        self.lang = "en-gb" if spec.split(":")[0].startswith("b") else "en-us"
        if "+" in spec:                                      # blend, e.g. bm_george:0.7+bm_fable:0.3
            parts = [p.split(":") for p in spec.split("+")]
            self.style = sum(self.k.get_voice_style(n) * float(w) for n, w in parts)
        else:
            self.style = spec
        os.makedirs(cache, exist_ok=True)

    def nwords(self, s):
        s = re.sub(r"[^\w'’\- ]", " ", s).strip()
        if not s:
            return 0
        return len(self.k.tokenizer.phonemize(s, self.lang).split())

    def say(self, sent, speed):
        text = " ".join(w["say"] for w in sent)
        key = hashlib.sha1(f"{self.spec}|{speed:.3f}|{text}".encode()).hexdigest()[:16]
        p = os.path.join(self.cache, key + ".npz")
        if os.path.exists(p):
            z = np.load(p, allow_pickle=True)
            return z["a"], list(z["t"])
        a, sr, tm = self.k.create_timed(text, voice=self.style, speed=speed, lang=self.lang)
        t = [(x.phoneme, float(x.start), float(x.end)) for x in tm]
        np.savez(p, a=np.asarray(a, np.float32), t=np.array(t, dtype=object))
        return np.asarray(a, np.float32), t

    def align(self, sent, audio, tm):
        """Word start/end times (s, relative to the sentence audio) from the model's phoneme durations."""
        pw, cur = [], []
        for ph, s, e in tm:
            if ph == " ":
                if cur:
                    pw.append((cur[0][1], cur[-1][2])); cur = []
            elif re.search(r"\w|[ˈˌəɪʊæɑɔɛʌθðŋʃʒɹɾʔː]", ph):
                cur.append((ph, s, e))
        if cur:
            pw.append((cur[0][1], cur[-1][2]))
        need = [max(1, self.nwords(w["say"])) for w in sent]
        dur = len(audio) / 24000
        if sum(need) == len(pw) and pw:
            out, i = [], 0
            for n in need:
                out.append((pw[i][0], pw[i + n - 1][1])); i += n
            return out
        # fallback: spread the words over the voiced span, weighted by length
        a0 = pw[0][0] if pw else 0.05
        a1 = pw[-1][1] if pw else dur - 0.05
        wts = [max(1, len(re.sub(r"\W", "", w["say"]))) for w in sent]
        tot, acc, out = sum(wts), 0, []
        for x in wts:
            s = a0 + (a1 - a0) * acc / tot; acc += x
            out.append((s, a0 + (a1 - a0) * acc / tot))
        return out


class ElevenVoice:
    """ElevenLabs, for your own cloned voice: set ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID, run with --engine elevenlabs.
    Uses the with-timestamps endpoint, so captions and effects stay locked to the words exactly as with Kokoro."""
    def __init__(self, speed, cache):
        self.key = os.environ["ELEVENLABS_API_KEY"]; self.vid = os.environ["ELEVENLABS_VOICE_ID"]
        self.model = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")
        self.speed, self.cache, self.spec = speed, cache, "elevenlabs:" + self.vid
        os.makedirs(cache, exist_ok=True)

    def say(self, sent, speed):
        import base64, urllib.request
        text = " ".join(w["say"] for w in sent)
        key = hashlib.sha1(f"{self.spec}|{speed:.3f}|{text}".encode()).hexdigest()[:16]
        p = os.path.join(self.cache, "el-" + key + ".npz")
        if os.path.exists(p):
            z = np.load(p, allow_pickle=True); return z["a"], list(z["t"])
        body = json.dumps({"text": text, "model_id": self.model, "voice_settings": {"stability": 0.42, "similarity_boost": 0.82,
                           "style": 0.3, "use_speaker_boost": True, "speed": max(0.7, min(1.2, speed))}}).encode()
        req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{self.vid}/with-timestamps?output_format=pcm_24000",
                                     data=body, headers={"xi-api-key": self.key, "Content-Type": "application/json"})
        r = json.loads(urllib.request.urlopen(req, timeout=120).read())
        a = np.frombuffer(base64.b64decode(r["audio_base64"]), dtype="<i2").astype(np.float32) / 32768
        al = r.get("alignment") or r.get("normalized_alignment") or {}
        t = list(zip(al.get("characters", []), al.get("character_start_times_seconds", []), al.get("character_end_times_seconds", [])))
        np.savez(p, a=a, t=np.array(t, dtype=object))
        return a, t

    def align(self, sent, audio, tm):
        spans, cur = [], None
        for ch, s, e in tm:
            if ch.isspace():
                if cur: spans.append(cur); cur = None
            else:
                cur = [s, e] if cur is None else [cur[0], e]
        if cur: spans.append(cur)
        need = [max(1, len(w["say"].split())) for w in sent]
        out, i = [], 0
        for n in need:
            if i + n - 1 < len(spans):
                out.append((spans[i][0], spans[i + n - 1][1]))
            else:
                out.append(out[-1] if out else (0, len(audio) / 24000))
            i += n
        return out


def pace(sent, base):
    """A little human variation: short lines land slower, asides and questions move a touch quicker."""
    n = len(sent)
    ev = [e[0] for w in sent for e in w["ev"]]
    s = base
    if n <= 3:
        s *= 0.96
    elif n >= 14:
        s *= 1.03
    if sent[-1]["say"].endswith("?"):
        s *= 1.02
    if "stamp" in ev or "boom" in [e.split("@")[0] for w in sent for k, e in w["ev"] if k == "sfx"]:
        s *= 0.96
    return s


def gap_after(sent, last_in_line, last_in_beat):
    w = sent[-1]
    g = 0.27
    if w["say"].endswith("?"):
        g = 0.38
    elif w["say"].endswith("!"):
        g = 0.28
    elif not re.search(r"[.?!]$", w["say"]):
        g = 0.2
    g = max(g, w["brk"])
    if last_in_line:
        g += 0.04
    if last_in_beat:
        g += 0.12
    return g


# ================================================================== timeline
def build(ep, voice, base_speed):
    t = 0.45
    beats, words, clips = [], [], []
    per_sentence = not getattr(voice, "phrases", False)
    breaths, nbreath, prev_gap = [], 0, 0.0
    build.breaths = breaths
    for bi, b in enumerate(ep["beats"]):
        b0 = t if bi else 0.0
        for li, line in enumerate(b["lines"]):
            ws = parse(line)
            ss = sentences(ws) if per_sentence else chunks(ws)
            line_say = [VO._plain(w["say"]) for w in ws]
            ldir, llp, wi = VO.ROLE_DIRECTION.get(b["role"], "calm"), 1.0, 0
            line_takes = None
            if getattr(voice, "directed", False) and hasattr(voice, "say_line") and not per_sentence:
                plan, d_, p_ = [], ldir, llp                  # the whole line in one breath, each sentence to its own note
                for sent in ss:
                    p_ = next((float(v) for k, v in sent[0]["ev"] if k == "p"), p_)
                    d_ = next((v for k, v in sent[0]["ev"] if k == "d"), d_)
                    act = {"tune": next((v for w in sent for k, v in w["ev"] if k == "tune"), None),
                           "note": next((v for w in sent for k, v in w["ev"] if k == "act"), None),
                           "gap": next((float(v) for k, v in sent[0]["ev"] if k == "gap"), None),
                           "beats": {str(j): float(v) for j, w in enumerate(sent) for k, v in w["ev"] if k == "beat"}}
                    plan.append(([w["say"] for w in sent], base_speed * p_, d_, {k: v for k, v in act.items() if v}))
                # house rule, from Sam's choice for "Case closed? Not even close.": a short rhetorical question is taken a
                # touch slower, with a beat before it and a longer one before its answer (unless the script says otherwise)
                for i_, (ws_, sp_, d2_, a_) in enumerate(plan):
                    last = VO._plain(ws_[-1]).rstrip("\"'’”)")
                    if last.endswith("?") and len(ws_) <= 5 and i_ + 1 < len(plan) and len(plan[i_ + 1][0]) <= 6:
                        if abs(sp_ - base_speed) < 1e-6:
                            plan[i_] = (ws_, base_speed * 0.92, d2_, a_)
                            if abs(plan[i_ + 1][1] - base_speed) < 1e-6:
                                plan[i_ + 1] = (plan[i_ + 1][0], base_speed * 0.92, plan[i_ + 1][2], plan[i_ + 1][3])
                        if i_ > 0 and "gap" not in a_:
                            a_["gap"] = 0.45
                        if "gap" not in plan[i_ + 1][3]:
                            plan[i_ + 1][3]["gap"] = 0.7
                voice.speed_line = base_speed                 # one tempo for the whole film: the rhythm is the voice's own
                line_takes = voice.say_line(plan)
            for si, sent in enumerate(ss):
                llp = next((float(v) for k, v in sent[0]["ev"] if k == "p"), llp)      # [p:0.95] pace, kept for the line
                ldir = next((v for k, v in sent[0]["ev"] if k == "d"), ldir)          # [d:reveal] direction, kept for the line
                lp, dirn = llp, ldir
                wi += len(sent)
                sp = (pace(sent, base_speed) if per_sentence else base_speed * VO.DIRECTION[dirn]["tempo"]) * lp
                if not per_sentence and not getattr(voice, "directed", False) and t > 1.0 and len(sent) >= 6 and prev_gap >= 0.45 and (nbreath % 2 == 0 or len(sent) >= 12):
                    breaths.append(t - 0.06)                 # an inhale in the silence before a long phrase
                if not per_sentence and len(sent) >= 6 and prev_gap >= 0.45:
                    nbreath += 1
                if line_takes is not None:
                    a, al, nat_gap = line_takes[si]
                elif getattr(voice, "directed", False):       # the stage note for this sentence (see voices.perform2)
                    act = {"tune": next((v for w in sent for k, v in w["ev"] if k == "tune"), None),
                           "note": next((v for w in sent for k, v in w["ev"] if k == "act"), None),
                           "beats": {str(j): float(v) for j, w in enumerate(sent) for k, v in w["ev"] if k == "beat"}}
                    act = {k: v for k, v in act.items() if v}
                    a, al = voice.say([w["say"] for w in sent], sp, dirn, act=act)
                else:
                    a, al = voice.say([w["say"] for w in sent], sp, dirn)
                clips.append((t, a, [w["say"] for w in sent]))
                for w, (s, e) in zip(sent, al):
                    words.append({"t0": round(t + s, 3), "t1": round(t + e, 3), "disp": w["disp"], "ev": w["ev"],
                                  "beat": bi, "end": sent[-1] is w or bool(re.search(r"[.?!…]$", w["disp"])), "em": w.get("em", False)})
                    if w.get("ev_end"):
                        words[-1]["ev_end"] = w["ev_end"]
                last_line = li == len(b["lines"]) - 1 and si == len(ss) - 1
                g = gap_after(sent, si == len(ss) - 1, last_line)
                if not per_sentence:
                    if si < len(ss) - 1:                     # between sentences of one line: the planned pause
                        pp = VO.pause_plan(line_say, wi - 1)
                        g = pp if pp else 0.2
                        if line_takes is not None:              # the slices are the line itself: her pauses are already in them
                            g = nat_gap
                        else:
                            g = next((float(v) for k, v in ss[si + 1][0]["ev"] if k == "gap"), g)   # [gap:0.8] from the script
                    else:
                        g = line_gap(sent, last_line, bi, ep)
                t += len(a) / SR + g; prev_gap = g
        beats.append({"t0": round(b0, 3), "t1": round(t, 3), "role": b["role"], "visual": b.get("visual", {}),
                      "frame": b.get("frame", {}), "kick": b.get("kick", "")})
    end = t + 0.15
    return beats, words, clips, end, end + 3.6


def line_gap(sent, last_in_beat, bi, ep):
    """Silence between breath groups: longer where the story turns."""
    w = VO._plain(sent[-1]["say"])
    g = 0.5
    if w.endswith("?"):
        g = 0.62
    elif w.endswith("...") or w.endswith("…"):
        g = 0.75
    elif not re.search(r"[.?!]$", w):
        g = 0.28                                            # the line runs on into the next
    g = max(g, sent[-1]["brk"])
    if last_in_beat:
        g += 0.2
        nxt = ep["beats"][bi + 1]["role"] if bi + 1 < len(ep["beats"]) else ""
        if nxt in ("reversal", "tag"):
            g += 0.12                                       # a held breath before the twist and the verdict
    return g


def captions(words):
    groups, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        txt = " ".join(x["disp"] for x in cur)
        nxt = words[i + 1] if i + 1 < len(words) else None
        brk = (re.search(r"[,.;:?!]$", w["disp"]) or len(cur) >= 4 or len(txt) >= 22 or w["end"]
               or (nxt and nxt["beat"] != w["beat"]))
        if brk:
            groups.append(cur); cur = []
    if cur:
        groups.append(cur)
    out = []
    for gi, g in enumerate(groups):
        t0 = g[0]["t0"] - 0.06
        t1 = groups[gi + 1][0]["t0"] - 0.06 if gi + 1 < len(groups) else g[-1]["t1"] + 0.5
        t1 = min(t1, g[-1]["t1"] + 0.9)
        out.append({"t0": round(t0, 3), "t1": round(t1, 3), "w": [[x["disp"], x["t0"], x["t1"], 1 if x.get("em") else 0] for x in g]})
    return out


def events(ep, beats, words, end):
    sfx, stamps, counts, kicks, gos = [], [], [], [], []
    cams = []
    for w in words:
        for kind, val in w["ev"] + [("__end__" + k, v) for k, v in w.get("ev_end", [])]:
            at = w["t0"]
            if kind.startswith("__end__"):
                kind, at = kind[7:], w["t1"]
            if kind == "sfx":
                name, _, off = val.partition("@")
                if name != "none":
                    sfx.append((round(at + (float(off) if off else 0), 3), name))
            elif kind == "stamp":
                txt, _, col = val.partition("|")
                stamps.append({"t": round(at, 3), "text": txt, "c": STAMPC.get(col or "red", col or "#ff7a6b")})
                sfx.append((round(at, 3), "stamp"))
            elif kind == "count":
                v, _, unit = val.partition("|")
                counts.append({"t": round(at, 3), "to": float(v.replace(",", "")), "unit": unit, "dec": len(v.split(".")[1]) if "." in v else 0})
                sfx.append((round(at, 3), "ticks"))
            elif kind == "k":
                kicks.append({"t": round(at - 0.12, 3), "text": val})
            elif kind == "cam":                                 # [cam:s|x|y] reframe the shot on this word
                v = [float(x) for x in val.split("|")]
                cams.append({"t": round(at - 0.2, 3), "b": w["beat"], "s": v[0], "x": v[1] if len(v) > 1 else 0, "y": v[2] if len(v) > 2 else 0})
            elif kind == "go":
                ch, _, d = val.partition("|")
                gos.append((round(at - 0.3, 3), float(ch), float(d) if d else 1.3, w["beat"]))
    for b in beats[1:]:                                    # a soft air swish on hard cuts only; glides stay silent
        if b["visual"].get("cut"):
            sfx.append((round(b["t0"], 3), "air"))
    sfx.append((round(end, 3), "chime"))
    rev = next((b for b in beats if b["role"] == "reversal"), None)
    if rev:
        sfx.append((round(rev["t0"], 3), "riser_to"))
    events.cams = sorted(cams, key=lambda c: c["t"])
    return thin(sorted(sfx)), stamps, counts, kicks, sorted(gos)


PRIORITY = {"chime": 0, "stamp": 1, "boom": 1, "ticks": 2, "air": 9, "riser_to": 3}


def thin(sfx, gap=1.6):
    """Subtle, not busy: never two cues within `gap` seconds. The one tied to the story wins (a stamp or a
    scripted effect beats an automatic air swish)."""
    keep = []
    for c in sorted(sfx, key=lambda c: PRIORITY.get(c[1], 4)):
        if all(abs(c[0] - k[0]) >= gap for k in keep):
            keep.append(c)
    return sorted(keep)


def moves(beats, gos):
    """Camera path through the story: (start time, chapter, glide seconds). Beats set where a shot starts;
    [go:N] markers move it on the exact word."""
    mv = []
    for bi, b in enumerate(beats):
        v = b["visual"]
        if "from" not in v:
            continue
        mv.append((b["t0"], v["from"], 0.0 if (bi == 0 or v.get("cut")) else 1.1))
        mine = [g for g in gos if g[3] == bi]
        if mine:
            mv += [(max(g[0], b["t0"] + 0.01), g[1], g[2]) for g in mine]
        elif v.get("to", v["from"]) != v["from"]:
            d0 = b["t0"] + v.get("delay", 0)
            mv.append((d0, v["to"], max(0.8, (b["t1"] - d0) * v.get("glide", 0.8))))
    return sorted(mv, key=lambda m: m[0])


# ================================================================== sound
def env_exp(n, rate):
    return np.exp(-np.arange(n) / SR * rate).astype(np.float32)


def noise(n):
    return rng.standard_normal(n).astype(np.float32)


def lowpass(x, fc):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(2, fc / (SR / 2), "low", output="sos"), x).astype(np.float32)


def highpass(x, fc):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(2, fc / (SR / 2), "high", output="sos"), x).astype(np.float32)


def bandpass(x, lo, hi):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(2, [lo / (SR / 2), hi / (SR / 2)], "band", output="sos"), x).astype(np.float32)


def sweep(f0, f1, dur, curve=1.0):
    n = int(dur * SR); tt = np.linspace(0, 1, n) ** curve
    f = f0 + (f1 - f0) * tt
    return np.sin(2 * np.pi * np.cumsum(f) / SR).astype(np.float32)


def fx(name):
    """Sound effects, synthesised. Each returns (samples, lead) where lead = seconds before the anchor it starts."""
    if name == "whoosh":
        d = 0.75; n = int(d * SR); x = noise(n)
        out = np.zeros(n, np.float32); seg = 1024
        for i in range(0, n, seg):
            u = i / n; c = 300 + 3200 * math.sin(math.pi * u) ** 1.5
            out[i:i + seg] = bandpass(x[i:i + seg], max(60, c * .5), min(6000, c * 1.3))
        e = np.sin(np.pi * np.linspace(0, 1, n)) ** 2.5
        return lowpass(out, 3000) * e * 0.8, 0.35
    if name == "air":                                    # a breath of air, felt more than heard
        x, lead = fx("whoosh")
        return lowpass(x, 1400) * 0.9, lead
    if name in ("boom", "hit"):                          # a low swell, no crack
        d = 3.2 if name == "boom" else 1.6; n = int(d * SR); tt = np.arange(n) / SR
        body = sweep(58, 34, d, 0.4) * np.minimum(1, tt / (0.09 if name == "boom" else 0.04)) * env_exp(n, 1.5 if name == "boom" else 3.2)
        air = lowpass(noise(n), 220) * np.minimum(1, tt / 0.15) * env_exp(n, 3) * 0.35
        return lowpass(body + air, 260), 0.0
    if name == "stamp":                                  # a felt thud on paper, not a slap
        n = int(0.5 * SR); tt = np.arange(n) / SR
        thump = np.sin(2 * np.pi * 88 * tt).astype(np.float32) * np.minimum(1, tt / 0.006) * env_exp(n, 22)
        paper = bandpass(noise(n), 1200, 4200) * env_exp(n, 30) * 0.22
        return thump + paper, 0.0
    if name == "ticks":                                  # a quiet mechanical counter
        n = int(1.4 * SR); out = np.zeros(n, np.float32)
        for k in range(8):
            i = int(SR * 1.25 * (1 - (1 - k / 8) ** 1.6)); m = int(0.02 * SR)
            out[i:i + m] += lowpass(np.sin(2 * np.pi * 1500 * np.arange(m) / SR).astype(np.float32) * env_exp(m, 180), 2500) * 0.45
        return out, 0.0
    if name == "shimmer":
        d = 2.4; n = int(d * SR); tt = np.arange(n) / SR; out = np.zeros(n, np.float32)
        for f in (1760, 2217, 2637, 3322, 3951, 4699):
            out += np.sin(2 * np.pi * f * tt + rng.random() * 6).astype(np.float32) * (0.5 + 0.5 * np.sin(2 * np.pi * (3 + rng.random() * 3) * tt))
        e = np.minimum(1, tt / 0.35) * np.exp(-tt * 1.2)
        return out * e * 0.12, 0.1
    if name == "rumble":
        d = 3.0; n = int(d * SR); x = np.cumsum(noise(n)); x = highpass(x / (np.abs(x).max() + 1e-6), 25)
        x = lowpass(x, 140); tt = np.arange(n) / SR
        return x / (np.abs(x).max() + 1e-6) * np.sin(np.pi * tt / d) ** 1.5 * 0.9, 0.3
    if name == "drill":
        d = 1.4; n = int(d * SR); tt = np.arange(n) / SR
        saw = (2 * ((tt * (190 + 12 * np.sin(2 * np.pi * 7 * tt))) % 1) - 1).astype(np.float32)
        x = bandpass(saw, 300, 3500) * 0.35 + bandpass(noise(n), 2000, 6000) * 0.15
        return x * np.minimum(1, tt / 0.08) * np.minimum(1, (d - tt) / 0.15), 0.0
    if name in ("chisel", "clink"):
        n = int(1.0 * SR); out = np.zeros(n, np.float32)
        for k, at in enumerate((0, .26, .52) if name == "chisel" else (0,)):
            i = int(at * SR); m = int(.3 * SR); tt = np.arange(m) / SR
            b = sum(np.sin(2 * np.pi * f * tt) * a for f, a in ((2900, 1), (4350, .6), (6100, .35))) * np.exp(-tt * 28)
            out[i:i + m] += b.astype(np.float32) * 0.35 + highpass(noise(m), 3000) * np.exp(-tt * 90).astype(np.float32) * 0.3
        return out, 0.0
    if name == "dig":
        n = int(1.2 * SR); out = np.zeros(n, np.float32)
        for at in (0, .38, .76):
            i = int(at * SR); m = int(.3 * SR)
            out[i:i + m] += bandpass(noise(m), 300, 2500) * env_exp(m, 12) * 0.6
        return out, 0.0
    if name == "paper":
        n = int(.6 * SR); x = bandpass(noise(n), 2200, 8000)
        e = np.abs(np.sin(np.linspace(0, 9, n))) * env_exp(n, 4)
        return x * e * 0.5, 0.05
    if name == "heartbeat":
        n = int(1.0 * SR); out = np.zeros(n, np.float32)
        for at, a in ((0, 1), (.22, .7)):
            i = int(at * SR); m = int(.25 * SR)
            out[i:i + m] += sweep(60, 40, .25) * env_exp(m, 18) * a
        return out, 0.0
    if name == "typewriter":
        n = int(1.2 * SR); out = np.zeros(n, np.float32)
        for k in range(9):
            i = int((k * .12 + rng.random() * .04) * SR); m = int(.03 * SR)
            out[i:i + m] += highpass(noise(m), 1500) * env_exp(m, 120) * 0.6
        return out, 0.0
    if name == "chime":
        d = 3.5; n = int(d * SR); tt = np.arange(n) / SR
        b = sum(np.sin(2 * np.pi * 523.25 * r * tt) * a * np.exp(-tt * (1.2 + r * .6)) for r, a in ((1, 1), (2.0, .5), (2.76, .35), (5.4, .15)))
        return b.astype(np.float32) * 0.45, 0.0
    if name == "riser_to":
        d = 2.2; n = int(d * SR); tt = np.arange(n) / SR
        x = bandpass(noise(n), 400, 5000) * 0.25 + sweep(180, 720, d, 1.6) * 0.18
        return x * (tt / d) ** 2.2, d
    if name == "wind":
        d = 5.0; n = int(d * SR); x = noise(n); out = np.zeros(n, np.float32); seg = 2048
        for i in range(0, n, seg):
            c = 380 + 220 * math.sin(i / n * 7)
            out[i:i + seg] = bandpass(x[i:i + seg], c * .7, c * 1.4)
        return lowpass(out, 900) * np.sin(np.pi * tt_(n) / d) * 0.5, 0.0
    return np.zeros(1, np.float32), 0.0


# Mix targets in LU relative to the narrator (momentary loudness, 400 ms). Negative = quieter than the voice.
MUSIC_UNDER_VOICE = -14      # the score while she speaks, measured after its middle is carved out for her (it rises in the pauses)
AMBIENCE = -24               # wind and room tone: felt, barely heard
FXLEVEL = {"boom": -7, "hit": -9, "stamp": -8, "ticks": -14, "whoosh": -13, "air": -16, "shimmer": -12, "rumble": -11,
           "drill": -12, "chisel": -11, "clink": -11, "dig": -11, "paper": -12, "heartbeat": -11, "typewriter": -12,
           "chime": -6, "riser_to": -12}


def kweight(x):
    """ITU-R BS.1770 K-weighting at 48 kHz."""
    from scipy.signal import lfilter
    x = lfilter([1.53512485958697, -2.69169618940638, 1.19839281085285], [1, -1.69065929318241, 0.73248077421585], x)
    return lfilter([1.0, -2.0, 1.0], [1, -1.99004745483398, 0.99007225036621], x)


def lufs(x, mask):
    y = kweight(np.asarray(x, np.float64)) ** 2
    m = mask[: len(y)] if hasattr(mask, "__len__") else np.ones(len(y), bool)
    return 10 * np.log10(np.mean(y[m]) + 1e-12) - 0.691


def peak_lufs(x):
    y = kweight(np.asarray(x, np.float64)) ** 2; w = int(0.4 * SR)
    if len(y) < w:
        y = np.pad(y, (0, w - len(y)))
    return 10 * np.log10(np.convolve(y, np.ones(w) / w, mode="valid").max() + 1e-12) - 0.691


def tt_(n):
    return np.arange(n) / SR


CHORDS = {
    "mystery": {"hook": [38, 50, 53, 57, 64], "world": [34, 46, 50, 53, 57], "collision": [43, 50, 55, 58, 62], "cost": [41, 48, 53, 57, 60],
                "reversal": [45, 52, 57, 61, 64], "tag": [38, 50, 57, 62, 65], "end": [38, 50, 54, 57, 62]},
    "awe": {"hook": [45, 57, 60, 64, 71], "world": [41, 53, 57, 60, 64], "collision": [40, 52, 55, 60, 67], "cost": [43, 55, 59, 62, 67],
            "reversal": [38, 50, 57, 60, 65], "tag": [41, 53, 60, 64, 69], "end": [36, 48, 55, 60, 64]},
    "space": {"hook": [40, 52, 56, 59, 66], "world": [40, 52, 57, 61, 64], "collision": [37, 49, 56, 61, 64], "cost": [35, 47, 54, 59, 63],
              "reversal": [33, 45, 56, 61, 64], "tag": [40, 52, 59, 64, 68], "end": [28, 40, 52, 59, 64, 68]},
    "cold": {"hook": [33, 45, 52, 57, 60], "world": [41, 48, 53, 57], "collision": [40, 47, 52, 56, 62], "cost": [38, 45, 50, 53, 57],
             "reversal": [36, 45, 52, 57, 60], "tag": [36, 48, 52, 55, 60], "end": [33, 45, 52, 57, 59, 64]},
}


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def score(mood, beats, end, total):
    n = int(total * SR); out = np.zeros(n, np.float32); tt = np.arange(n) / SR
    C = CHORDS.get(mood, CHORDS["mystery"])
    segs = [(b["t0"], b["t1"], C.get(b["role"], C["hook"])) for b in beats] + [(end, total, C["end"])]
    for s0, s1, notes in segs:
        a, z = int(max(0, s0 - 0.6) * SR), int(min(total, s1 + 1.2) * SR)
        if z <= a:
            continue
        t = tt[a:z] - tt[a]
        seg = np.zeros(z - a, np.float32)
        for j, m in enumerate(notes):
            f = hz(m); amp = (0.55 if j == 0 else 0.3) / len(notes) ** .3
            for det in (-0.004, 0, 0.004):
                for h in range(1, 7):
                    if f * h > 5000:
                        break
                    seg += (amp / h ** 1.35 * np.sin(2 * np.pi * f * (1 + det) * h * t + rng.random() * 6)).astype(np.float32)
        seg += 0.35 * np.sin(2 * np.pi * hz(notes[0] - 12) * t).astype(np.float32)
        d = (z - a) / SR
        e = np.minimum(1, t / 1.4) * np.minimum(1, np.maximum(0, (d - t) / 1.4))
        seg *= e * (0.8 + 0.2 * np.sin(2 * np.pi * t / 6.5))
        out[a:z] += seg
    for b in beats:                                        # a soft pulse under the tense beats
        if b["role"] in ("collision", "cost"):
            k = b["t0"] + 0.3
            while k < b["t1"] - 0.2:
                i = int(k * SR); m = int(.3 * SR)
                if i + m < n:
                    out[i:i + m] += lowpass(sweep(52, 40, .3) * np.minimum(1, np.arange(m) / SR / .02) * env_exp(m, 12), 150) * 0.16
                k += 60 / 68
    # air above the voice: a breath of high, slowly moving shimmer, so the score has a top as well as a floor
    tt2 = np.arange(n) / SR
    air = bandpass(noise(n), 6500, 11000) * (0.55 + 0.45 * np.sin(2 * np.pi * tt2 / 9.0)) * np.clip(tt2 / 2.0, 0, 1)
    out += air * (0.06 * np.sqrt(np.mean(out ** 2)) / (np.sqrt(np.mean(air ** 2)) + 1e-9))
    return out / (np.abs(out).max() + 1e-6)


def reverb(x, secs=2.2, wet=0.28):
    from scipy.signal import fftconvolve
    m = int(secs * SR); ir = noise(m) * env_exp(m, 3.2 / secs * 2.3); ir = lowpass(ir, 6000); ir /= np.abs(ir).sum() ** .5 * 8
    y = fftconvolve(x, ir)[: len(x)].astype(np.float32)
    return x * (1 - wet) + y * wet * 3


def _has_rubberband():
    try:
        return "rubberband" in subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True).stdout
    except Exception:
        return False


RUBBER = "rubberband=pitch=0.966:formant=preserved" if _has_rubberband() else ""


def ffmpeg_af(src, dst, af):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", af, "-ar", str(SR), "-ac", "1", dst], check=True)


def write_wav(p, x, sr=SR, ch=1):
    x = np.clip(x, -1, 1)
    with wave.open(p, "wb") as w:
        w.setnchannels(ch); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def read_wav(p):
    import soundfile as sf
    a, sr = sf.read(p, dtype="float32")
    return (a.mean(axis=1) if a.ndim > 1 else a), sr


def _sos(kind, f, order=4):
    from scipy.signal import butter
    return butter(order, (np.array(f) if isinstance(f, (list, tuple)) else f) / (SR / 2), kind, output="sos")


def hipass(x, f):
    from scipy.signal import sosfiltfilt
    return sosfiltfilt(_sos("high", f), x).astype(np.float32)


def bandpass(x, a, b):
    from scipy.signal import sosfiltfilt
    return sosfiltfilt(_sos("band", [a, b], 2), x).astype(np.float32)


def carve(x, talk, mid_db, edge_db, lo=220, hi=6000):
    """Split into lows / the voice's middle / highs (zero-phase, so the three sum back exactly) and duck each band by its
    own amount while the narrator speaks."""
    from scipy.signal import sosfiltfilt
    x = np.asarray(x, np.float32)
    l = sosfiltfilt(_sos("low", lo), x); h = sosfiltfilt(_sos("high", hi), x); m = x - l - h
    gm = 10 ** (mid_db * talk / 20); ge = 10 ** (edge_db * talk / 20)
    return (l * ge + m * gm + h * ge).astype(np.float32)


def mix(ep, clips, beats, sfx, end, total, work):
    from scipy.signal import resample_poly
    n = int(total * SR) + SR
    narr = np.zeros(n, np.float32)
    for t0, a, *_ in clips:
        a = np.asarray(a, np.float32)
        if len(a) > 2000:                                    # every take sits on true zero and eases in and out: no clicks at the joins
            a = a - np.float32(np.median(np.concatenate([a[:480], a[-480:]])))
            fz = int(0.006 * SR); a = a.copy(); a[:fz] *= np.linspace(0, 1, fz, dtype=np.float32); a[-fz:] *= np.linspace(1, 0, fz, dtype=np.float32)
        i = int(t0 * SR); narr[i:i + len(a)] += a[: max(0, n - i)]
    rms = float(np.sqrt(np.mean(narr[np.abs(narr) > 0.02 * np.abs(narr).max()] ** 2)))
    for k, te in enumerate(getattr(build, "breaths", [])):
        b_ = VO.breath(rms, 0.3 + 0.08 * ((k * 7) % 3) / 2, seed=k)
        i = int(te * SR) - len(b_)
        if i > 0:
            narr[i:i + len(b_)] += b_
    narr /= np.abs(narr).max() + 1e-6
    write_wav(os.path.join(work, "narr_raw.wav"), narr * 0.9)
    voice = VO.design(mix.character, narr)                 # the character's sound design (voices.py)
    write_wav(os.path.join(work, "narr.wav"), voice)
    # ---- levels are set by loudness, relative to the narrator, so nothing ever jumps out of the mix
    talk = np.zeros(n, np.float32)                          # 1 while the narrator speaks, eased in and out
    for t0, a, *_ in clips:
        talk[int(t0 * SR): int(t0 * SR) + len(a)] = 1
    ramp = int(0.35 * SR); talk = np.convolve(talk, np.ones(ramp) / ramp, mode="same").astype(np.float32)
    duck = lambda depth: 1 - depth * talk
    Lv = lufs(voice, talk > 0.5)
    fxbus = np.zeros(n, np.float32)
    for at, name in sfx:
        x, lead = fx(name); x = np.asarray(x, np.float32).copy()
        k = min(len(x), int(0.004 * SR)); x[:k] *= np.linspace(0, 1, k)   # no clicks
        x *= 10 ** ((Lv + FXLEVEL.get(name, -12) - peak_lufs(x)) / 20)
        i = int((at - lead) * SR)
        if i < 0:
            x = x[-i:]; i = 0
        fxbus[i:i + len(x)] += x[: max(0, n - i)]
    # ---- the sandwich: the voice owns the middle of the spectrum; score, effects and air live below and above it.
    # While she speaks, the middle band of everything else dips (a multiband duck), the lows and highs barely move.
    fxbus = carve(fxbus, talk, -6, -1.5)
    music = score(ep.get("mood", "mystery"), beats, end, total + 1)[:n]
    music = carve(music, talk, -9, -2)
    music *= 10 ** ((Lv + MUSIC_UNDER_VOICE - lufs(music, talk > 0.5)) / 20)
    amb = ep.get("ambience")
    if amb:
        x, _ = fx(amb); rep = np.tile(x, int(n / len(x)) + 1)[:n]
        rep = carve(rep, talk, -8, -2)
        amb_bus = rep * 10 ** ((Lv + AMBIENCE - lufs(rep, talk > 0.5)) / 20)
    else:
        amb_bus = np.zeros(n, np.float32)
    tt = np.arange(n) / SR
    fade = np.clip(tt / 1.2, 0, 1) * np.clip((total - tt) / 1.8, 0, 1)
    dry = music + fxbus + amb_bus
    bed = reverb(dry, wet=0.3)
    bed *= 10 ** ((lufs(dry, np.ones(n, bool)) - lufs(bed, np.ones(n, bool))) / 20)   # the room adds space, not level
    bed = (bed * fade).astype(np.float32)
    # the voice keeps its own space: a gentle scoop of the bed around her presence band, always on
    bed = bed - 0.25 * bandpass(bed, 900, 3500)
    if os.environ.get("RC_STEMS"):
        write_wav(os.path.join(work, "stem_voice.wav"), voice * 0.5); write_wav(os.path.join(work, "stem_bed.wav"), bed * 0.5)
    print(f"  mix: score {lufs(bed, talk > 0.5) - Lv:+.1f} LU under the voice, loudest moment {peak_lufs(bed) - Lv:+.1f} LU", flush=True)
    # stereo: the voice dead centre; the bed opened out to the sides above 300 Hz (lows stay centred and solid)
    d = int(0.011 * SR); hi_ = hipass(bed, 300); side = np.zeros(n, np.float32); side[d:] = hi_[:-d]; side = 0.42 * (side - hi_ * 0.5)
    L = voice + bed + side; R = voice + bed - side
    st = np.stack([L, R], 1); st /= np.abs(st).max() + 1e-6
    pre = os.path.join(work, "mix_pre.wav"); fin = os.path.join(work, "mix.wav")
    import soundfile as sf
    sf.write(pre, (st * 0.9).astype(np.float32), SR, subtype="PCM_24")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", pre, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "2", fin], check=True)
    return fin


# ================================================================== pictures
VT = """(()=>{const _ael=EventTarget.prototype.addEventListener;
/* filming: only the scroll stories listen to scroll; the page chrome (top bar, reading bars, contents) would force a full
   layout of this very long page on every frame */
EventTarget.prototype.addEventListener=function(ty,fn,o){ if(this===window&&ty==='scroll'&&fn&&!/needT/.test(String(fn))) return; return _ael.call(this,ty,fn,o); };
let now=0;const q=[];window.__rnow=performance.now.bind(performance);performance.now=()=>now;const D=Date.now.bind(Date),d0=D();Date.now=()=>d0+now;
window.requestAnimationFrame=cb=>{q.push(cb);return q.length};window.cancelAnimationFrame=()=>{};
window.__step=ms=>{now+=ms;const c=q.splice(0);c.forEach(f=>{try{f(now)}catch(e){console.error(e)}})};
try{localStorage.setItem('rc-theme','dark')}catch(e){}window.RC_HQ=1;window.RC_LBL={top:.1,bottom:.7,pad:.06};})();"""


def css(fonts, capb):
    ff = "".join(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{wt};src:url('file://{fonts}/{fn}') format('woff2')}}"
                 for fam, st, wt, fn in [("Newsreader", "normal", 400, "newsreader-latin-400-normal.woff2"), ("Newsreader", "italic", 400, "newsreader-latin-400-italic.woff2"),
                                         ("Newsreader", "normal", 500, "newsreader-latin-500-normal.woff2"), ("Newsreader", "italic", 500, "newsreader-latin-500-italic.woff2"),
                                         ("Inter", "normal", 400, "inter-latin-400-normal.woff2"), ("Inter", "normal", 600, "inter-latin-600-normal.woff2"),
                                         ("Inter", "normal", 700, "inter-latin-700-normal.woff2")])
    return ff + f"""
html,body{{scrollbar-width:none}}::-webkit-scrollbar{{display:none}}
*,*::before,*::after{{animation-play-state:paused!important;transition-duration:0s!important;transition-delay:0s!important}}
html,body,#main,.page,.story,.story-in,.sy,.sy-in{{overflow-x:clip!important}}   /* a zoomed camera must never widen the mobile layout viewport */
.topbar,#ask-launch{{display:none!important}}
.bottom-nav,.sy-intro,.gz-card,.gz-rail,.gz-lg,.sy-cnt,.sy-bar,.gz-hud,.story .gz-cue,.sy-steps .gz-card{{visibility:hidden!important}}
.sy-stage,#pyr{{position:sticky!important;top:0!important;height:100vh!important;max-height:none!important;min-height:0!important;z-index:50!important;margin:0!important;border-radius:0!important;overflow:hidden!important}}
.sy-hud{{display:none!important}}   /* the kicker carries the date in a film; the room's own counter would collide with scene titles */
#rv{{position:fixed;inset:0;z-index:9999;pointer-events:none;font-family:Inter,system-ui,sans-serif;color:#fff6e8;overflow:hidden}}
#rv [hidden]{{display:none!important}}
#rv .vig{{position:absolute;inset:0;background:radial-gradient(120% 90% at 50% 45%,rgba(0,0,0,0) 55%,rgba(0,0,0,.55) 100%),linear-gradient(rgba(0,0,0,.45),rgba(0,0,0,0) 16%,rgba(0,0,0,0) 62%,rgba(0,0,0,.55))}}
#rv canvas.grain{{display:none}}
#rv .bar{{position:absolute;left:0;top:0;height:3px;background:#e0b27a;box-shadow:0 0 8px rgba(224,178,122,.7)}}
#rv .brand{{position:absolute;top:18px;left:22px;right:22px;display:flex;justify-content:space-between;font:700 10.5px Inter;letter-spacing:.16em;text-transform:uppercase;text-shadow:0 1px 8px rgba(0,0,0,.7)}}
#rv .brand span{{opacity:.92;display:inline-flex;align-items:center;gap:8px}}#rv .brand .mk{{width:20px;height:20px;display:block}}#rv .brand i{{font-style:normal;color:#e8b87a}}
#rv .hook{{position:absolute;left:24px;right:70px;top:120px;font:500 46px/1.04 Newsreader,serif;letter-spacing:-.015em;text-shadow:0 2px 26px rgba(0,0,0,.85)}}
#rv .hook em{{font-style:italic;color:#f2c98e}}
#rv .kick{{position:absolute;left:24px;right:70px;bottom:{capb + 92}px;text-align:center;font:700 13px Inter;letter-spacing:.22em;text-transform:uppercase;color:#f2c98e;text-shadow:0 1px 10px rgba(0,0,0,.9)}}
#rv .kick:before,#rv .kick:after{{content:"";display:inline-block;width:26px;height:1px;background:currentColor;vertical-align:middle;margin:0 10px;opacity:.8}}
#rv .cap{{position:absolute;left:22px;right:70px;bottom:{capb}px;text-align:center;font:700 28px/1.18 Inter;letter-spacing:-.01em}}
#rv .cap .pill{{display:inline;background:rgba(12,9,6,.5);padding:5px 10px 7px;border-radius:12px;-webkit-box-decoration-break:clone;box-decoration-break:clone;backdrop-filter:blur(2px)}}
#rv .cap span{{display:inline-block;margin:0 .12em;color:rgba(255,246,232,.62);text-shadow:0 2px 4px rgba(0,0,0,.95),0 0 18px rgba(0,0,0,.8);transition:none}}
#rv .cap span.done{{color:#fff6e8}}#rv .cap span.on{{color:#ffcf8a}}#rv .cap span.em.done,#rv .cap span.em.on{{color:#ffcf8a}}
#rv .stamp{{position:absolute;left:50%;top:40%;font:800 25px Inter;letter-spacing:.14em;text-transform:uppercase;padding:10px 18px;border:3.5px solid currentColor;border-radius:10px;white-space:nowrap;background:rgba(10,8,6,.45);text-shadow:0 0 14px rgba(0,0,0,.6)}}
#rv .count{{position:absolute;left:0;right:0;top:15%;text-align:center;font:500 88px/1 Newsreader,serif;text-shadow:0 2px 30px rgba(0,0,0,.9)}}
#rv .count small{{font:700 22px Inter;letter-spacing:.06em;margin-left:6px;color:#f2c98e}}
#rv .note{{position:absolute;left:0;right:0;bottom:{max(40, capb - 150)}px;text-align:center;font:600 9px Inter;letter-spacing:.14em;text-transform:uppercase;opacity:.45}}
#rv .end{{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:15px;text-align:center;padding:0 34px;background:radial-gradient(110% 70% at 50% 42%,#1d160f,#070605)}}
#rv .end .k{{font:700 11px Inter;letter-spacing:.2em;text-transform:uppercase;color:#e8b87a}}
#rv .end .q{{font:italic 400 25px/1.2 Newsreader,serif;opacity:.92;max-width:430px}}
#rv .end .v{{font:800 15px Inter;letter-spacing:.12em;text-transform:uppercase;padding:10px 18px;border-radius:999px;border:3px solid var(--vc);color:var(--vc)}}
#rv .end .emk .mk{{width:54px;height:54px;display:block;margin:6px auto 0}}#rv .end .t{{font:500 44px/1.04 Newsreader,serif;margin-top:6px}}#rv .end .t em{{color:#e8b87a}}
#rv .end .u{{font:600 14px Inter;opacity:.85}}#rv .end .src{{font:500 11.5px/1.45 Inter;opacity:.62;max-width:400px;margin-top:4px}}#rv .end .src b{{font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:10px;margin-right:6px;opacity:.9}}#rv .end .m{{font:italic 400 15px Newsreader,serif;opacity:.65;margin-top:10px}}
#rv .end .f{{position:absolute;bottom:120px;font:700 11px Inter;letter-spacing:.2em;text-transform:uppercase;opacity:.6}}
"""


OVERLAY = r"""(D)=>{
 const rv=document.createElement('div');rv.id='rv';document.body.appendChild(rv);
 rv.innerHTML='<div class="vig"></div><canvas class="grain" width="180" height="320"></canvas><div class="bar"></div>'+
  '<div class="brand"><span><svg class=\'mk\' viewBox=\'0 0 100 100\'><defs><clipPath id=\'rvu\'><rect width=\'100\' height=\'58\'/></clipPath></defs><circle cx=\'50\' cy=\'50\' r=\'38\' fill=\'none\' stroke=\'#f5f1eb\' stroke-opacity=\'.9\' stroke-width=\'5\'/><circle cx=\'50\' cy=\'58\' r=\'13\' fill=\'#e8b87a\' clip-path=\'url(#rvu)\'/><line x1=\'12.5\' y1=\'58\' x2=\'87.5\' y2=\'58\' stroke=\'#f5f1eb\' stroke-width=\'5\'/><line x1=\'24\' y1=\'66\' x2=\'76\' y2=\'66\' stroke=\'#f5f1eb\' stroke-opacity=\'.45\' stroke-width=\'3.5\'/></svg>Residual Continuum</span><i></i></div><div class="hook"></div><div class="kick"></div><div class="cap"></div>'+
  '<div class="stamp" hidden></div><div class="count" hidden></div><div class="note"></div><div class="end" hidden></div>';
 const $=s=>rv.querySelector(s);
 $('.brand i').textContent=D.series||''; $('.note').textContent=D.note;
 $('.hook').innerHTML=D.hook.replace(/\*([^*]+)\*/g,'<em>$1</em>');
 const e=$('.end');
 e.innerHTML='<span class="k">'+(D.vlabel?'The verdict':'Where do you stand?')+'</span>'+(D.claim?'<span class="q">'+D.claim+'</span>':'')+
  (D.vlabel?'<span class="v" style="--vc:'+D.vcol+'">'+D.vlabel+'</span>':'')+'<span class="emk"><svg class=\'mk\' viewBox=\'0 0 100 100\'><defs><clipPath id=\'rvu\'><rect width=\'100\' height=\'58\'/></clipPath></defs><circle cx=\'50\' cy=\'50\' r=\'38\' fill=\'none\' stroke=\'#f5f1eb\' stroke-opacity=\'.9\' stroke-width=\'5\'/><circle cx=\'50\' cy=\'58\' r=\'13\' fill=\'#e8b87a\' clip-path=\'url(#rvu)\'/><line x1=\'12.5\' y1=\'58\' x2=\'87.5\' y2=\'58\' stroke=\'#f5f1eb\' stroke-width=\'5\'/><line x1=\'24\' y1=\'66\' x2=\'76\' y2=\'66\' stroke=\'#f5f1eb\' stroke-opacity=\'.45\' stroke-width=\'3.5\'/></svg></span><span class="t">Weigh it <em>yourself.</em></span>'+
  (D.src?'<span class="src"><b>Sources</b> '+D.src+'</span>':'')+(D.handle?'<span class="u">'+D.handle+'</span>':'')+'<span class="m">Coherence is the measure, not final demonstration.</span><span class="f">Follow for the next case</span>';
 const gc=$('.grain').getContext('2d'), gi=gc.createImageData(180,320);
 const ease=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2, clamp=(v,a,b)=>v<a?a:v>b?b:v;
 const stage=D.stageSel?document.querySelector(D.stageSel):null;
 if(stage){ stage.style.transformOrigin='50% 50%'; stage.style.willChange='auto'; stage.style.contain='none'; }
 let capKey='', lastT=null; const cam={init:false,beat:-1,s:1,x:0,y:0,vs:0,vx:0,vy:0};
 function frameOf(i){ const f=(D.beats[i]&&D.beats[i].frame)||{}; return {s:f.s||1,x:f.x||0,y:f.y||0,nl:f.nl||0}; }
 const lbls=document.getElementById('pyr-labels');
 window.__frame=(t,seed)=>{
  const tc=t; if(D.fps>=50) t=Math.floor((t*60+1.0001)/2)/30;   /* graphics hold for each pair of 60 fps frames, so the shutter blend never ghosts text */
  $('.bar').style.width=(100*Math.min(1,t/D.end)).toFixed(2)+'%';
  const hk=$('.hook'); const hkE=Math.max(1.2,Math.min(2.9,...D.counts.map(q=>q.t-.5),...D.stamps.map(q=>q.t-.5)));   /* the title card clears before any big number lands */
  const ho=t<hkE?Math.min(1,t/.25):Math.max(0,1-(t-hkE)/.35); hk.style.opacity=ho; hk.style.transform='translateY('+((1-Math.min(1,t/.7))*16).toFixed(1)+'px)';
  let bi=0; for(let i=0;i<D.beats.length;i++){ if(t>=D.beats[i].t0) bi=i; }
  if(stage){ /* the camera: a critically damped spring follows each shot's framing, with a slow push-in and drift across the shot,
     a breath of handheld float, and clean hard cuts that land a touch wide and settle. Nothing ever jumps. */
    const b=D.beats[bi]; let z=frameOf(bi); for(const c of D.cams){ if(c.b===bi&&tc>=c.t) z={s:c.s,x:c.x,y:c.y,nl:z.nl}; }
    const du=clamp((tc-b.t0)/Math.max(1,b.t1-b.t0),0,1), dir=bi%2?1:-1;
    const T={s:z.s*(1+.04*ease(du)), x:z.x+dir*.014*du, y:z.y-.008*du};
    const cut=b.visual&&b.visual.cut&&bi>0, h=lastT===null?0:Math.min(.1,Math.max(0,tc-lastT)); lastT=tc;
    if(!cam.init||(cut&&cam.beat!==bi)){ cam.s=T.s*(cut?1.045:1); cam.x=T.x; cam.y=T.y; cam.vs=cam.vx=cam.vy=0; cam.init=true; }
    if(D.stills){ cam.s=T.s; cam.x=T.x; cam.y=T.y; }
    cam.beat=bi; if(lbls){ const v=z.nl?'hidden':''; if(lbls.style.visibility!==v) lbls.style.visibility=v; }   /* close-ups: no callouts */
    const w=2.4, steps=Math.max(1,Math.round(h/.004)), dt_=h/steps;
    for(let i=0;i<steps;i++){ for(const k of ['s','x','y']){ const v='v'+k; cam[v]+=(w*w*(T[k]-cam[k])-2*w*cam[v])*dt_; cam[k]+=cam[v]*dt_; } }
    const t_=t; t=tc; const hx=(Math.sin(t*.53)*.6+Math.sin(t*1.31+1.7)*.3+Math.sin(t*2.9+.4)*.1)*2.6, hy=(Math.sin(t*.47+2.1)*.6+Math.sin(t*1.13+.5)*.3+Math.sin(t*2.3+1.1)*.1)*2.2;
    const rot=(Math.sin(t*.41+.3)*.6+Math.sin(t*1.07)*.4)*.14;
    stage.style.transform='translate('+(cam.x*540+hx).toFixed(2)+'px,'+(cam.y*960+hy).toFixed(2)+'px) rotate('+rot.toFixed(3)+'deg) scale('+(cam.s*1.025).toFixed(4)+')'; stage.style.filter=''; t=t_; }
  let k=null; for(const q of D.kicks){ if(t>=q.t&&t<q.t+2.3) k=q; }
  const kk=$('.kick'); if(k){ if(kk.textContent!==k.text) kk.textContent=k.text; const u=(t-k.t); kk.style.opacity=Math.min(1,u/.25)*Math.min(1,(2.3-u)/.4); kk.style.letterSpacing=(0.32-0.1*Math.min(1,u/.5)).toFixed(3)+'em'; } else kk.style.opacity=0;
  let g=null; for(const q of D.caps){ if(t>=q.t0&&t<q.t1){ g=q; break; } }
  const cap=$('.cap');
  if(g&&t<D.end){ const key=g.t0+''; if(key!==capKey){ capKey=key; cap.innerHTML='<b class="pill">'+g.w.map(w=>'<span'+(w[3]?' class="em"':'')+'>'+w[0].replace(/&/g,'&amp;').replace(/</g,'&lt;')+'</span>').join(' ')+'</b>'; }
    const sp=cap.firstChild.children; g.w.forEach((w,i)=>{ const on=t>=w[1]-.04&&t<w[2]+.02, done=t>=w[2]; sp[i].className=(on?'on':done?'done':'')+(w[3]?' em':''); sp[i].style.transform=on?'translateY(-2px) scale(1.06)':''; });
    const u=t-g.t0; cap.style.opacity=Math.min(1,u/.08); cap.style.transform='translateY('+(Math.max(0,1-u/.12)*8).toFixed(1)+'px)'; }
  else { cap.style.opacity=0; capKey=''; }
  let st=null; for(const q of D.stamps){ if(t>=q.t&&t<q.t+2.2) st=q; }
  const se=$('.stamp'); if(st){ se.hidden=false; if(se.textContent!==st.text) se.textContent=st.text; se.style.color=st.c; const u=t-st.t, sk=Math.min(1,u/.16);
    const sh=u<.3?Math.sin(u*90)*(1-u/.3)*3:0; se.style.transform='translate(-50%,-50%) rotate(-7deg) translate('+sh.toFixed(1)+'px,0) scale('+(1.9-.9*ease(sk)).toFixed(3)+')'; se.style.opacity=Math.min(sk*1.5,1)*Math.min(1,(2.2-u)/.35); } else se.hidden=true;
  let ct=null; for(const q of D.counts){ if(t>=q.t&&t<q.t+3.2) ct=q; }
  const ce=$('.count'); if(ct){ ce.hidden=false; const u=t-ct.t, v=ct.to*ease(Math.min(1,u/1.3)); ce.innerHTML=v.toLocaleString('en-GB',{minimumFractionDigits:ct.dec,maximumFractionDigits:ct.dec})+(ct.unit?'<small>'+ct.unit+'</small>':''); ce.style.opacity=Math.min(1,u/.2)*Math.min(1,(3.2-u)/.4); ce.style.transform='scale('+(1+.04*Math.min(1,u/1.3)).toFixed(3)+')'; } else ce.hidden=true;
  const eo=clamp((t-D.end)/.45,0,1); e.hidden=eo<=0; window.__covered=eo>=1; if(stage){ const v=eo>=1?'hidden':''; if(stage.style.visibility!==v) stage.style.visibility=v; } e.style.opacity=eo; e.style.transform='scale('+(1.03-.03*eo).toFixed(3)+')';
 };
}"""


async def film(ep, beats, caps, stamps, counts, kicks, end, total, site, work, fps, fonts, stills=None, mv=None, chunk=None):
    from playwright.async_api import async_playwright
    frames = os.path.join(work, "frames")
    if chunk is None:
        shutil.rmtree(frames, ignore_errors=True)
    os.makedirs(frames, exist_ok=True)
    story = ep.get("story")
    stage_sel = "#pyr" if story == "home" else (f"#sy-{story} .sy-stage" if story else None)
    D = {"series": ((ep["code"] + " · ") if ep.get("code") else "") + ep.get("series", ""), "hook": ep["hook_text"], "handle": os.environ.get("RC_HANDLE", ""), "src": ep.get("sources", ""),
         "caps": caps, "beats": beats, "stamps": stamps, "counts": counts,
         "kicks": kicks, "end": end, "note": ep.get("note", "Schematic reconstruction · sources in the case file"), "claim": ep.get("claim", ""),
         "cams": getattr(events, "cams", []), "stills": bool(stills), "fps": 0, "vlabel": VERD.get(ep.get("verdict"), ""), "vcol": VCOL.get(ep.get("verdict"), "#fff"), "stageSel": stage_sel}
    async with async_playwright() as pw:
        extra = {"args": ["--no-sandbox", "--disable-dev-shm-usage", "--run-all-compositor-stages-before-draw", "--disable-checker-imaging", "--disable-partial-raster", "--disable-new-content-rendering-timeout", "--deterministic-mode", "--force-gpu-mem-available-mb=4096", "--max-tiles-for-interest-area=4096", "--default-tile-width=2048", "--default-tile-height=2048"]}
        if os.environ.get("RC_CHROME_LIB"):
            extra["env"] = {**os.environ, "LD_LIBRARY_PATH": os.environ["RC_CHROME_LIB"]}
        b = await (pw.chromium.launch(executable_path=CHROME, **extra) if CHROME else pw.chromium.launch(**extra))
        ctx = await b.new_context(viewport={"width": W, "height": H}, device_scale_factor=DPR, color_scheme="dark", has_touch=True, is_mobile=True)
        await ctx.route(re.compile(r"^https?://"), lambda r: r.abort())
        await ctx.add_init_script(VT)
        pg = await ctx.new_page(); errs = []
        pg.on("pageerror", lambda e_: errs.append(str(e_)))
        if ep.get("site"):                                  # a film with its own stage page (the scene kit)
            site = os.path.join(ROOT, ep["site"])
        await pg.goto("file://" + site + "#" + ep["view"])
        for _ in range(20):
            await pg.evaluate("__step(50)")
        await pg.add_style_tag(content=css(fonts, ep.get("cap_bottom", 232)))
        await pg.evaluate("window.dispatchEvent(new Event('resize'))")
        for _ in range(6):
            await pg.evaluate("__step(50)")
        await pg.evaluate(OVERLAY, D)
        await pg.evaluate("document.fonts && document.fonts.ready")
        keys = []
        if story == "home":
            keys = await pg.evaluate("window.RC_storyKeys ? RC_storyKeys() : []")
        elif story:
            keys = await pg.evaluate(f"SY.keys('{story}')")
        snap = "window.RC_snap&&RC_snap()" if story == "home" else f"SY.snap&&SY.snap('{story}')"
        setp = "RC_film(P)" if story == "home" else f"SY.film('{story}',P)"
        def key(i):
            return keys[max(0, min(int(i), len(keys) - 1))]
        if keys and mv:
            await pg.evaluate(f"window.scrollTo(0,{keys[0] + 4});window.dispatchEvent(new Event('scroll'));" + setp.replace("P", str(float(mv[0][1]))) + ";" + snap)
            for _ in range(110):
                await pg.evaluate("__step(33.3)")
        await pg.evaluate("window.__kitRewind && __kitRewind()")     # the opening shot starts on frame 0: its build-ins and camera move play
        n = int(total * fps); dt = 1000 / fps; last_y = None
        times = stills if stills else [i / fps for i in range(n)]
        batch = []                                         # frames with no picture run in one go inside the page (fast pre-roll)
        async def flush():
            if batch:
                t0_ = __import__("time").time(); nb = len(batch)
                if os.environ.get("RC_PROF"):
                    slow = await pg.evaluate("()=>{const S=[];let t;" + "".join("t=__rnow();" + j + f";if(__rnow()-t>40)S.push([{k},Math.round(__rnow()-t),{json.dumps(j[:90])}]);" for k, j in enumerate(batch)) + "return S}")
                    if slow: print("  slow frames:", slow[:6], flush=True)
                    batch.clear()
                else:
                    await pg.evaluate("()=>{window.__pre=1;try{" + ";".join(batch) + "}finally{window.__pre=0}}"); batch.clear()
                if os.environ.get("RC_PROF"): print(f"  batch {nb} frames {__import__('time').time() - t0_:.2f}s", flush=True)
        settled = False
        for i, t in enumerate(times):
            if chunk is not None and i >= chunk[1]:
                break
            js = ""
            if keys and mv:
                y = float(mv[0][1])                        # the story position: chapter plus fraction, set directly in the page
                for (m0, ch, dur) in mv:
                    if t < m0:
                        break
                    if dur <= 0 or t >= m0 + dur:
                        y = float(ch)
                    else:
                        u = (t - m0) / dur; u = u * u * u * (u * (u * 6 - 15) + 10)     # smootherstep: eases in and out
                        y = y + (ch - y) * u
                if y != last_y:
                    jump = last_y is not None and abs(y - last_y) > .5 and y == round(y)      # a hard cut: the scene snaps, no morph
                    js += setp.replace("P", f"{y:.5f}") + ";" + (snap + ";" if jump else ""); last_y = y
            if stills:
                js += "for(let k=0;k<45;k++)__step(33.3);"
            js += f"__step({dt});__frame({t:.4f},{(i * 7919) % 2147483647})"
            picture = chunk is None or (chunk[0] <= i < chunk[1] and not os.path.exists(os.path.join(frames, f"{i:05d}.jpg")))
            if not picture:
                batch.append(js)
                if len(batch) >= int(os.environ.get("RC_BATCH", 240)):
                    await flush()
                continue
            await flush()                                  # pre-roll frames (state only), then this frame drawn for real
            if chunk is not None and not settled:          # a chunk that starts mid-film: let wall-clock CSS transitions settle
                await asyncio.sleep(1.2); settled = True   # after the fast pre-roll, or its first frames flash (sky, labels)
            await pg.evaluate("()=>{" + js + "}")
            await pg.screenshot(path=os.path.join(frames, f"{i:05d}.jpg"), type="jpeg", quality=93)
            if i % (fps * 5) == 0:
                print(f"  frame {i}/{n}", flush=True)
        await flush()
        await b.close()
        if errs:
            print("page errors:", errs[:3])
    return frames


def _vf(fps):
    """The film look, done in ffmpeg so the browser only draws the scene:
    a warm halation that lets only the highlights glow; a gentle film curve (lifted blacks, rolled-off whites);
    cool shadows and warm highlights; a hair of chromatic fringing; a faint, uneven exposure flicker; and real
    grain: a half-resolution plate of moving noise, softened and laid over the picture, so it reads as film stock
    rather than digital speckle. Present, never loud."""
    return ("[0:v]scale=1080:1920:flags=lanczos,format=gbrp,split[a][b];"
            "[b]scale=270:480:flags=bilinear,curves=all='0/0 0.56/0 1/1',gblur=sigma=7,colorchannelmixer=rr=1.1:gg=.9:bb=.68,scale=1080:1920:flags=bicubic[g];"
            "[a][g]blend=all_mode=screen:all_opacity=0.34,"
            "curves=all='0/0.032 0.25/0.24 0.75/0.765 1/0.962',colorbalance=rs=-.018:bs=.022:rh=.028:bh=-.024,"
            "rgbashift=rh=-1:bh=1,format=yuv420p,split[p1][p2];"
            "[p2]scale=540:960:flags=bilinear,format=gray,geq=lum='128',format=yuv420p,noise=c0s=38:c0f=t,gblur=sigma=0.7,scale=1080:1920:flags=bicubic[n];"
            "[p1][n]blend=all_mode=overlay:all_opacity=0.15,format=yuv420p[v]")


X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "19", "-maxrate", "14M", "-bufsize", "28M", "-profile:v", "high", "-pix_fmt", "yuv420p"]


# ================================================================== 16:9 long form (YouTube): landscape HUD, look and captions
# Used only for a film whose episode has "aspect": "16:9" (see free/longjob.py and films/long/LONG_ENGINE.md). Everything above
# (W, H, DPR, VT, css, OVERLAY, _vf, X264 and the 9:16 code paths) is the Shorts' and stays exactly as it is.
W16, H16, DPR16 = 960, 540, 2                # viewport in CSS px; screenshots at DPR 2 are 1920 x 1080
FPS16 = 30
LONG_TAIL = 8.0                              # seconds of end card after the last word (room for YouTube end-screen elements)
MARK16 = ("<svg class='mk' viewBox='0 0 100 100'><defs><clipPath id='rvu{k}'><rect width='100' height='58'/></clipPath></defs>"
          "<circle cx='50' cy='50' r='38' fill='none' stroke='#f5f1eb' stroke-opacity='.9' stroke-width='5'/><circle cx='50' cy='58' r='13' "
          "fill='#e8b87a' clip-path='url(#rvu{k})'/><line x1='12.5' y1='58' x2='87.5' y2='58' stroke='#f5f1eb' stroke-width='5'/>"
          "<line x1='24' y1='66' x2='76' y2='66' stroke='#f5f1eb' stroke-opacity='.45' stroke-width='3.5'/></svg>")


def css16(fonts):
    """The landscape HUD (960 x 540 CSS px): brand top left, chapter top right, captions bottom centre (2 lines, 660 px = 1320 px
    on the 1920 frame), progress bar along the bottom edge, hook title top left, intro title card, end card."""
    ff = "".join(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{wt};src:url('file://{fonts}/{fn}') format('woff2')}}"
                 for fam, st, wt, fn in [("Newsreader", "normal", 400, "newsreader-latin-400-normal.woff2"), ("Newsreader", "italic", 400, "newsreader-latin-400-italic.woff2"),
                                         ("Newsreader", "normal", 500, "newsreader-latin-500-normal.woff2"), ("Newsreader", "italic", 500, "newsreader-latin-500-italic.woff2"),
                                         ("Inter", "normal", 400, "inter-latin-400-normal.woff2"), ("Inter", "normal", 600, "inter-latin-600-normal.woff2"),
                                         ("Inter", "normal", 700, "inter-latin-700-normal.woff2")])
    return ff + """
html,body{scrollbar-width:none}::-webkit-scrollbar{display:none}
*,*::before,*::after{animation-play-state:paused!important;transition-duration:0s!important;transition-delay:0s!important}
html,body,#main,.page,.story,.story-in,.sy,.sy-in{overflow-x:clip!important}
.sy-stage{position:sticky!important;top:0!important;height:100vh!important;max-height:none!important;min-height:0!important;z-index:50!important;margin:0!important;border-radius:0!important;overflow:hidden!important}
.sy-hud,.sy-intro,.sy-cnt,.sy-bar{display:none!important}
#rv{position:fixed;inset:0;z-index:9999;pointer-events:none;font-family:Inter,system-ui,sans-serif;color:#fff6e8;overflow:hidden}
#rv [hidden]{display:none!important}
#rv .vig{position:absolute;inset:0;background:radial-gradient(125% 115% at 50% 46%,rgba(0,0,0,0) 58%,rgba(0,0,0,.5) 100%),linear-gradient(rgba(0,0,0,.36),rgba(0,0,0,0) 20%,rgba(0,0,0,0) 66%,rgba(0,0,0,.5))}
#rv .track{position:absolute;left:0;right:0;bottom:0;height:3px;background:rgba(255,246,232,.1)}
#rv .track i{position:absolute;top:0;width:2px;height:3px;background:rgba(10,8,6,.95)}
#rv .bar{position:absolute;left:0;bottom:0;height:3px;background:#e0b27a;box-shadow:0 0 8px rgba(224,178,122,.6)}
#rv .brand{position:absolute;top:20px;left:28px;display:flex;align-items:center;gap:9px;font:700 9.5px Inter;letter-spacing:.17em;text-transform:uppercase;text-shadow:0 1px 8px rgba(0,0,0,.7)}
#rv .brand .mk{width:19px;height:19px;display:block}#rv .brand span{opacity:.92}
#rv .brand i{font-style:normal;color:#e8b87a;opacity:.95}
#rv .brand i:not(:empty):before{content:"";display:inline-block;width:14px;height:1px;background:rgba(255,246,232,.5);vertical-align:middle;margin:0 9px 0 1px}
#rv .chap{position:absolute;top:23px;right:28px;font:600 9.5px Inter;letter-spacing:.17em;text-transform:uppercase;color:rgba(255,246,232,.86);text-shadow:0 1px 8px rgba(0,0,0,.75);opacity:0}
#rv .chap b{color:#e8b87a;font-weight:700;margin-right:9px}
#rv .hook{position:absolute;left:28px;top:58px;max-width:500px;font:500 36px/1.06 Newsreader,serif;letter-spacing:-.015em;text-shadow:0 2px 24px rgba(0,0,0,.85)}
#rv .hook em{font-style:italic;color:#f2c98e}
#rv .cap{position:absolute;left:50%;bottom:30px;width:660px;margin-left:-330px;text-align:center;text-wrap:balance;font:600 20px/1.36 Inter;letter-spacing:-.005em}
#rv .cap .pill{display:inline;background:rgba(12,9,6,.52);padding:3px 9px 5px;border-radius:9px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
#rv .cap span{display:inline-block;margin:0 .1em;color:rgba(255,246,232,.66);text-shadow:0 1px 3px rgba(0,0,0,.95),0 0 14px rgba(0,0,0,.75)}
#rv .cap span.done{color:#fff6e8}#rv .cap span.on{color:#ffcf8a}#rv .cap span.em.done,#rv .cap span.em.on{color:#ffcf8a}
#rv .stamp{position:absolute;left:50%;top:38%;font:800 22px Inter;letter-spacing:.14em;text-transform:uppercase;padding:9px 16px;border:3px solid currentColor;border-radius:9px;white-space:nowrap;background:rgba(10,8,6,.45);text-shadow:0 0 14px rgba(0,0,0,.6)}
#rv .count{position:absolute;left:0;right:0;top:16%;text-align:center;font:500 76px/1 Newsreader,serif;text-shadow:0 2px 30px rgba(0,0,0,.9)}
#rv .count small{font:700 19px Inter;letter-spacing:.06em;margin-left:6px;color:#f2c98e}
#rv .note{position:absolute;right:28px;bottom:12px;font:600 7.5px Inter;letter-spacing:.14em;text-transform:uppercase;opacity:.4}
#rv .intro{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:14px;text-align:center;background:radial-gradient(90% 80% at 50% 50%,rgba(13,10,7,.5),rgba(7,6,5,.8))}
#rv .intro .k{font:700 10px Inter;letter-spacing:.24em;text-transform:uppercase;color:#e8b87a}
#rv .intro .t{font:500 54px/1.04 Newsreader,serif;letter-spacing:-.015em;max-width:760px;text-wrap:balance;text-shadow:0 2px 30px rgba(0,0,0,.8)}
#rv .intro .t em{font-style:italic;color:#f2c98e}
#rv .intro .r{width:120px;height:1px;background:#e8b87a;opacity:.85}
#rv .end{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:11px;text-align:center;padding:0 80px;background:radial-gradient(90% 80% at 50% 44%,#1d160f,#070605)}
#rv .end .k{font:700 10px Inter;letter-spacing:.22em;text-transform:uppercase;color:#e8b87a}
#rv .end .q{font:italic 400 21px/1.25 Newsreader,serif;opacity:.92;max-width:640px}
#rv .end .v{font:800 13px Inter;letter-spacing:.12em;text-transform:uppercase;padding:8px 16px;border-radius:999px;border:2.5px solid var(--vc);color:var(--vc)}
#rv .end .emk .mk{width:40px;height:40px;display:block;margin:4px auto 0}
#rv .end .t{font:500 42px/1.04 Newsreader,serif}#rv .end .t em{color:#e8b87a}
#rv .end .l{font:italic 400 17px/1.3 Newsreader,serif;opacity:.84;max-width:600px}
#rv .end .u{font:600 12px Inter;opacity:.8}
#rv .end .src{font:500 9.5px/1.5 Inter;opacity:.55;max-width:700px;margin-top:4px}#rv .end .src b{font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:8.5px;margin-right:6px}
#rv .end .m{position:absolute;bottom:22px;left:0;right:0;font:italic 400 12px Newsreader,serif;opacity:.55}
"""


OVERLAY16 = r"""(D)=>{
 const rv=document.createElement('div');rv.id='rv';document.body.appendChild(rv);
 const em=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/\*([^*]+)\*/g,'<em>$1</em>');
 rv.innerHTML='<div class="vig"></div><div class="track"></div><div class="bar"></div>'+
  '<div class="brand">'+D.mark1+'<span>Residual Continuum</span><i></i></div><div class="chap"><b></b><span></span></div>'+
  '<div class="hook"></div><div class="cap"></div><div class="stamp" hidden></div><div class="count" hidden></div><div class="note"></div>'+
  '<div class="intro" hidden><span class="k"></span><span class="t"></span><span class="r"></span></div><div class="end" hidden></div>';
 const $=s=>rv.querySelector(s);
 $('.brand i').textContent=D.series||''; $('.note').textContent=D.note||'';
 $('.hook').innerHTML=em(D.hook||'');
 const tr=$('.track'); (D.chapters||[]).forEach(c=>{ if(c.t>.5&&c.t<D.end){ const m=document.createElement('i'); m.style.left=(100*c.t/D.end).toFixed(2)+'%'; tr.appendChild(m); } });
 const IN=D.intro; if(IN){ $('.intro .k').textContent=IN.kicker||''; $('.intro .t').innerHTML=em(IN.title); }
 const e=$('.end');
 e.innerHTML='<span class="k">'+(D.vlabel?'The verdict':'Where do you stand?')+'</span>'+(D.claim?'<span class="q">'+em(D.claim)+'</span>':'')+
  (D.vlabel?'<span class="v" style="--vc:'+D.vcol+'">'+D.vlabel+'</span>':'')+'<span class="emk">'+D.mark2+'</span><span class="t">Weigh it <em>yourself.</em></span>'+
  (D.endLine?'<span class="l">'+em(D.endLine)+'</span>':'')+(D.src?'<span class="src"><b>Sources</b> '+em(D.src)+'</span>':'')+(D.handle?'<span class="u">'+D.handle+'</span>':'')+
  '<span class="m">Coherence is the measure, not final demonstration.</span>';
 const ease=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2, clamp=(v,a,b)=>v<a?a:v>b?b:v;
 const stage=D.stageSel?document.querySelector(D.stageSel):null;
 if(stage){ stage.style.transformOrigin='50% 50%'; stage.style.willChange='auto'; stage.style.contain='none'; }
 let capKey='', chKey='', lastT=null; const cam={init:false,beat:-1,s:1,x:0,y:0,vs:0,vx:0,vy:0};
 function frameOf(i){ const f=(D.beats[i]&&D.beats[i].frame)||{}; return {s:f.s||1,x:f.x||0,y:f.y||0}; }
 window.__frame=(t,seed)=>{
  const tc=t; if(D.fps>=50) t=Math.floor((t*60+1.0001)/2)/30;
  $('.bar').style.width=(100*Math.min(1,t/D.end)).toFixed(2)+'%';
  const hk=$('.hook'); const hkE=Math.max(1.2,Math.min(2.9,...D.counts.map(q=>q.t-.5),...D.stamps.map(q=>q.t-.5)));
  const ho=t<hkE?Math.min(1,t/.25):Math.max(0,1-(t-hkE)/.35); hk.style.opacity=ho; hk.style.transform='translateY('+((1-Math.min(1,t/.7))*12).toFixed(1)+'px)';
  let bi=0; for(let i=0;i<D.beats.length;i++){ if(t>=D.beats[i].t0) bi=i; }
  if(stage){ /* the same camera as the Shorts (a critically damped spring, a slow push-in across each beat, a breath of handheld
     float), calmer and in landscape pixels */
    const b=D.beats[bi]; let z=frameOf(bi); for(const c of D.cams){ if(c.b===bi&&tc>=c.t) z={s:c.s,x:c.x,y:c.y}; }
    const du=clamp((tc-b.t0)/Math.max(1,b.t1-b.t0),0,1), dir=bi%2?1:-1;
    const T={s:z.s*(1+.03*ease(du)), x:z.x+dir*.01*du, y:z.y-.006*du};
    const h=lastT===null?0:Math.min(.1,Math.max(0,tc-lastT)); lastT=tc;
    if(!cam.init){ cam.s=T.s; cam.x=T.x; cam.y=T.y; cam.vs=cam.vx=cam.vy=0; cam.init=true; }
    cam.beat=bi;
    const w=2.4, steps=Math.max(1,Math.round(h/.004)), dt_=h/steps;
    for(let i=0;i<steps;i++){ for(const k of ['s','x','y']){ const v='v'+k; cam[v]+=(w*w*(T[k]-cam[k])-2*w*cam[v])*dt_; cam[k]+=cam[v]*dt_; } }
    const hx=(Math.sin(tc*.53)*.6+Math.sin(tc*1.31+1.7)*.3+Math.sin(tc*2.9+.4)*.1)*2.2, hy=(Math.sin(tc*.47+2.1)*.6+Math.sin(tc*1.13+.5)*.3+Math.sin(tc*2.3+1.1)*.1)*1.6;
    const rot=(Math.sin(tc*.41+.3)*.6+Math.sin(tc*1.07)*.4)*.08;
    if(window.__wallCam) __wallCam(cam.s*1.025,cam.x*960+hx,cam.y*540+hy,rot);   /* a wall draws it inside the picture (see kit.js WALL) */
    else stage.style.transform='translate('+(cam.x*960+hx).toFixed(2)+'px,'+(cam.y*540+hy).toFixed(2)+'px) rotate('+rot.toFixed(3)+'deg) scale('+(cam.s*1.025).toFixed(4)+')'; }
  const eo=clamp((t-D.end)/.45,0,1);
  let io=0; if(IN){ io=clamp(Math.min((t-IN.t0)/.45,(IN.t1-t)/.6),0,1); const ie=$('.intro'); ie.hidden=io<=0;
    if(io>0){ const u=clamp((t-IN.t0)/1.1,0,1); ie.style.opacity=io.toFixed(3); ie.querySelector('.t').style.transform='translateY('+((1-ease(u))*14).toFixed(1)+'px)'; ie.querySelector('.r').style.transform='scaleX('+ease(clamp((t-IN.t0-.3)/.9,0,1)).toFixed(3)+')'; } }
  let ch=null; for(const c of (D.chapters||[])){ if(t>=c.t+2.4) ch=c; }
  const cE=$('.chap'), ck=ch?ch.n+'':''; if(ck!==chKey){ chKey=ck; if(ch){ cE.firstChild.textContent=(ch.n<10?'0':'')+ch.n; cE.lastChild.textContent=ch.title; } }
  cE.style.opacity=(ch?Math.min(1,(t-ch.t-2.4)/.6):0)*(1-io)*(1-eo);
  let k=null; for(const q of D.kicks){ if(t>=q.t&&t<q.t+2.3) k=q; }
  let g=null; for(const q of D.caps){ if(t>=q.t0&&t<q.t1){ g=q; break; } }
  const cap=$('.cap');
  if(g&&t<D.end){ const key=g.t0+''; if(key!==capKey){ capKey=key; cap.innerHTML='<b class="pill">'+g.w.map(w=>'<span'+(w[3]?' class="em"':'')+'>'+w[0].replace(/&/g,'&amp;').replace(/</g,'&lt;')+'</span>').join(' ')+'</b>'; }
    const sp=cap.firstChild.children; g.w.forEach((w,i)=>{ const on=t>=w[1]-.04&&t<w[2]+.02, done=t>=w[2]; sp[i].className=(on?'on':done?'done':'')+(w[3]?' em':''); });
    const u=t-g.t0; cap.style.opacity=(Math.min(1,u/.1)*(1-io)).toFixed(3); cap.style.transform='translateY('+(Math.max(0,1-u/.14)*6).toFixed(1)+'px)'; }
  else { cap.style.opacity=0; capKey=''; }
  let st=null; for(const q of D.stamps){ if(t>=q.t&&t<q.t+2.2) st=q; }
  const se=$('.stamp'); if(st){ se.hidden=false; if(se.textContent!==st.text) se.textContent=st.text; se.style.color=st.c; const u=t-st.t, sk=Math.min(1,u/.16);
    const sh=u<.3?Math.sin(u*90)*(1-u/.3)*3:0; se.style.transform='translate(-50%,-50%) rotate(-6deg) translate('+sh.toFixed(1)+'px,0) scale('+(1.9-.9*ease(sk)).toFixed(3)+')'; se.style.opacity=Math.min(sk*1.5,1)*Math.min(1,(2.2-u)/.35); } else se.hidden=true;
  let ct=null; for(const q of D.counts){ if(t>=q.t&&t<q.t+3.2) ct=q; }
  const ce=$('.count'); if(ct){ ce.hidden=false; const u=t-ct.t, v=ct.to*ease(Math.min(1,u/1.3)); ce.innerHTML=v.toLocaleString('en-GB',{minimumFractionDigits:ct.dec,maximumFractionDigits:ct.dec})+(ct.unit?'<small>'+ct.unit+'</small>':''); ce.style.opacity=Math.min(1,u/.2)*Math.min(1,(3.2-u)/.4); } else ce.hidden=true;
  e.hidden=eo<=0; window.__covered=eo>=1; if(stage){ const v=eo>=1?'hidden':''; if(stage.style.visibility!==v) stage.style.visibility=v; } e.style.opacity=eo; e.style.transform='scale('+(1.03-.03*eo).toFixed(3)+')';
 };
}"""


def _vf16(fps):
    """The Shorts' film look (_vf) at 1920 x 1080: the same halation, curve, colour, fringing and grain, its plates scaled to the
    landscape frame (halation at a quarter, grain at half resolution)."""
    return ("[0:v]scale=1920:1080:flags=lanczos,format=gbrp,split[a][b];"
            "[b]scale=480:270:flags=bilinear,curves=all='0/0 0.56/0 1/1',gblur=sigma=7,colorchannelmixer=rr=1.1:gg=.9:bb=.68,scale=1920:1080:flags=bicubic[g];"
            "[a][g]blend=all_mode=screen:all_opacity=0.34,"
            "curves=all='0/0.032 0.25/0.24 0.75/0.765 1/0.962',colorbalance=rs=-.018:bs=.022:rh=.028:bh=-.024,"
            "rgbashift=rh=-1:bh=1,format=yuv420p,split[p1][p2];"
            "[p2]scale=960:540:flags=bilinear,format=gray,geq=lum='128',format=yuv420p,noise=c0s=38:c0f=t,gblur=sigma=0.7,scale=1920:1080:flags=bicubic[n];"
            "[p1][n]blend=all_mode=overlay:all_opacity=0.15,format=yuv420p[v]")


SOFT16 = {"the", "a", "an", "of", "to", "from", "and", "in", "on", "at", "by", "for", "with", "or", "but", "as", "that", "his", "her", "their",
          "its", "into", "than", "more", "some", "this", "these", "those", "is", "was", "were", "are", "be", "who", "which", "not", "no", "very"}


def _split16(ws, mc, mw):
    """A sentence too long for one caption, cut into the most even pieces that fit, preferring cuts after a comma and never
    leaving a little word (the, of, from...) at the end of a line."""
    L = lambda i, j: len(" ".join(w["disp"] for w in ws[i:j]))
    n = len(ws)
    if L(0, n) <= mc and n <= mw:
        return [ws]
    m = max(-(-L(0, n) // mc), -(-n // mw)); target = L(0, n) / m
    def pen(w):
        d = re.sub(r"[^\w']", "", w["disp"].lower())
        return 4 + (-8 if re.search(r"[,;:]$", w["disp"]) else 0) + (12 if d in SOFT16 else 0)
    dp, prev = [0.0] + [1e18] * n, [0] * (n + 1)
    for j in range(1, n + 1):
        for i in range(j - 1, -1, -1):
            if L(i, j) > mc or j - i > mw:
                break
            c = dp[i] + (L(i, j) - target) ** 2 / 100 + (pen(ws[j - 1]) if j < n else 0)
            if c < dp[j]:
                dp[j], prev[j] = c, i
    cuts, j = [], n
    while j > 0:
        cuts.append((prev[j], j)); j = prev[j]
    return [ws[i:j] for i, j in reversed(cuts)]


def captions16(words, max_chars=62, max_words=12):
    """Long-form captions: sentence by sentence (a long one in even pieces), at most two lines of about 1300 px, never across
    a beat, each word lighting as it is said."""
    sents, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if w["end"] or not nxt or nxt["beat"] != w["beat"]:
            sents.append(cur); cur = []
    if cur:
        sents.append(cur)
    groups = [g for s in sents for g in _split16(s, max_chars, max_words)]
    out = []
    for gi, g in enumerate(groups):
        t0 = g[0]["t0"] - 0.06
        t1 = groups[gi + 1][0]["t0"] - 0.06 if gi + 1 < len(groups) else g[-1]["t1"] + 0.6
        t1 = min(t1, g[-1]["t1"] + 1.1)
        out.append({"t0": round(t0, 3), "t1": round(t1, 3), "w": [[x["disp"], x["t0"], x["t1"], 1 if x.get("em") else 0] for x in g]})
    return out


def chapters16(ep, beats):
    """[{t, n, title}]: where each chapter starts (the start of its first beat, when the camera sets off for its card)."""
    out = []
    for bi, b in enumerate(ep["beats"]):
        if b.get("chapter"):
            out.append({"t": beats[bi]["t0"], "n": len(out) + 1, "title": b["chapter"]})
    return out


def intro16(ep, beats):
    """The intro title card: over the title beat (role "title" or "intro": true), at least 3.4 s; without one, just after the hook."""
    if not ep.get("intro_title"):
        return None
    bi = next((i for i, b in enumerate(ep["beats"]) if b.get("intro") or b.get("role") == "title"), None)
    t0, t1 = (beats[bi]["t0"], beats[bi]["t1"] - 0.15) if bi is not None else (3.3, 7.3)
    return {"t0": round(t0, 3), "t1": round(max(t1, t0 + 3.4), 3), "title": ep["intro_title"], "kicker": ep.get("series", "")}


def youtube_chapters(chapters, total):
    """YouTube's chapter list (first entry at 0:00)."""
    f = lambda t: f"{int(t // 60)}:{int(t % 60):02d}"
    rows = [] if chapters and chapters[0]["t"] < 1 else ["0:00 Introduction"]
    return "\n".join(rows + [f"{f(c['t'])} {c['title']}" for c in chapters])


def long_data(ep, beats, caps, stamps, counts, kicks, end, cams, fps):
    """What OVERLAY16 needs to draw the HUD of a long film."""
    return {"series": ((ep["code"] + " · ") if ep.get("code") else "") + ep.get("series", ""), "hook": ep["hook_text"], "handle": os.environ.get("RC_HANDLE", ""),
            "src": ep.get("sources", ""), "caps": caps, "beats": [{k: b[k] for k in ("t0", "t1", "role", "visual", "frame")} for b in beats],
            "stamps": stamps, "counts": counts, "kicks": kicks, "end": end, "cams": cams, "fps": 0 if fps < 50 else fps,
            "note": ep.get("note", "Schematic reconstruction · sources in the description"), "claim": ep.get("claim", ""),
            "vlabel": VERD.get(ep.get("verdict"), ""), "vcol": VCOL.get(ep.get("verdict"), "#fff"), "endLine": ep.get("end_line", ""),
            "chapters": chapters16(ep, beats), "intro": intro16(ep, beats), "stageSel": f"#sy-{ep['id']} .sy-stage",
            "mark1": MARK16.format(k="a"), "mark2": MARK16.format(k="b")}


def encode(frames, audio, out, fps, part=None):
    """Whole film in one go, or (part=(a, b)) just frames a..b as a silent piece to be joined by mux()."""
    if part:
        a, b = part
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-start_number", str(a), "-i", os.path.join(frames, "%05d.jpg"),
                        "-frames:v", str(b - a), "-filter_complex", _vf(fps), "-map", "[v]", "-r", str(fps), *X264, out], check=True)
        return
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(frames, "%05d.jpg"), "-i", audio,
                    "-filter_complex", _vf(fps), "-map", "[v]", "-map", "1:a", "-r", str(fps), *X264,
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)


def mux(parts, audio, out):
    lst = out + ".txt"
    open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", audio, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    os.remove(lst)


def voices_demo(out):
    line = ("Six hundred and forty-eight metres. Straight down. Under a pyramid. "
            "Which is quite a lot to find, without a shovel.")
    work = os.path.join(out, "work", "voices"); os.makedirs(work, exist_ok=True)
    parts = []
    for spec in ["bm_george", "bm_george:0.6+bm_fable:0.4", "am_michael", "am_fenrir:0.5+am_michael:0.5", "bm_fable"]:
        v = Voice(spec, 0.95, os.path.join(work, "cache"))
        ws = parse(line); clips = []
        for s in sentences(ws):
            a, _ = v.say(s, pace(s, 0.95)); clips.append(a); clips.append(np.zeros(int(0.4 * 24000), np.float32))
        from scipy.signal import resample_poly
        a = resample_poly(np.concatenate(clips), 2, 1).astype(np.float32)
        raw = os.path.join(work, "raw.wav"); write_wav(raw, a / np.abs(a).max() * .9)
        pr = os.path.join(work, spec.replace(":", "").replace("+", "_") + ".wav")
        ffmpeg_af(raw, pr, (RUBBER + "," if RUBBER else "") + "highpass=f=70,equalizer=f=170:t=q:w=1.1:g=2.5,"
                            "equalizer=f=3000:t=q:w=1.3:g=1.8,equalizer=f=7600:t=q:w=2:g=-2.5,acompressor=threshold=-21dB:ratio=2.6:attack=6:release=140:makeup=2,aecho=0.92:0.3:23|41:0.09|0.05,loudnorm=I=-16")
        parts.append((spec, pr))
    print(json.dumps(parts, indent=1))
    return parts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", nargs="?")
    ap.add_argument("--voice", default=None)
    ap.add_argument("--engine", default="kokoro", choices=["kokoro", "elevenlabs"])
    ap.add_argument("--speed", type=float, default=None)
    ap.add_argument("--out", default=os.path.join(ROOT, "out"))
    ap.add_argument("--fps", type=int, default=60)   # 60 fps: fluid motion on every platform
    ap.add_argument("--draft", action="store_true")
    ap.add_argument("--only", type=float, default=0)
    ap.add_argument("--audio-only", action="store_true")
    ap.add_argument("--chunk", default=None, help="a:b  film only frames a to b-1 (resumable, for short sessions)")
    ap.add_argument("--encode-only", action="store_true")
    ap.add_argument("--voices", action="store_true")
    ap.add_argument("--encode-part", default=None, help="a:b  encode frames a..b as a silent piece (long films on slow machines)")
    ap.add_argument("--mux", action="store_true", help="join the encoded pieces and add the sound")
    ap.add_argument("--stills", action="store_true", help="one frame in the middle of each beat, as a contact sheet")
    a = ap.parse_args()
    if a.voices:
        voices_demo(a.out); return
    E = {e["id"]: e for e in json.load(open(os.path.join(ROOT, "episodes", os.environ.get("RC_EPISODES", "episodes3.json")), encoding="utf-8"))}
    ep = E[a.episode]
    if ep.get("aspect") == "16:9":                         # a long film (16:9): voiced, filmed in chunks and assembled by longjob.py
        import longjob
        return longjob.from_reel(ep, a)
    fps = 15 if a.draft else a.fps
    work = os.path.join(a.out, "work", ep["id"] + "-v2"); os.makedirs(work, exist_ok=True)
    who = a.voice or ep.get("voice", NARRATOR)
    if a.engine == "elevenlabs":
        voice = ElevenVoice(a.speed or 1.0, os.path.join(a.out, "work", "tts-cache")); who = "archivist"
    elif who in VO.CAST:
        voice = VO.engine(VO.CAST[who], os.path.join(a.out, "work", "tts-cache")); voice.speed = a.speed or VO.CAST[who]["speed"]
    else:                                                   # a raw Kokoro blend, e.g. am_fenrir:0.5+am_michael:0.5
        voice = VO.Kokoro(who, os.path.join(a.out, "work", "tts-cache")); voice.speed = a.speed or 0.98; who = "archivist"
    mix.character = who
    print("voice…", flush=True)
    beats, words, clips, end, total = build(ep, voice, voice.speed)
    caps = captions(words)
    if a.audio_only:
        open(os.path.join(work, "tts_used.txt"), "w").write("\n".join(getattr(voice, "used", [])))
    sfx, stamps, counts, kicks, gos = events(ep, beats, words, end)
    sfx.sort()
    print(f"  {total:.1f} s, {len(words)} words, {len(sfx)} sound cues", flush=True)
    audio = os.path.join(work, "mix.wav")
    if not ((a.chunk or a.encode_only or a.encode_part or a.mux) and os.path.exists(audio)):
        audio = mix(ep, clips, beats, sfx, end, total, work)
    tl = os.path.join(work, "timeline.json")                 # written atomically: parallel render jobs all pass here
    tmp = tl + f".{os.getpid()}"
    json.dump({"beats": beats, "caps": caps, "sfx": sfx, "stamps": stamps, "counts": counts, "kicks": kicks, "end": end, "total": total},
              open(tmp, "w"), indent=1)
    os.replace(tmp, tl)
    if a.audio_only:
        if os.environ.get("RC_HEAR", "1") == "1":
            for what, line in getattr(voice, "log", []):
                print(f"  performance: {what}: {line}")
            bad = VO.hear_check([([x.replace("*", "") for x in c[2]], c[1]) for c in clips])
            json.dump(bad, open(os.path.join(work, "hear_check.json"), "w"), indent=1, ensure_ascii=False)
            for x in bad:
                print(f"  hear-check {x['match']:.2f}: missed {x['missed']} | heard: {x['heard']}")
        print("audio:", audio); return
    if a.stills:
        ts = []
        for b in beats:
            ts += [b["t0"] + 0.4, (b["t0"] + b["t1"]) / 2, b["t1"] - 0.3]
        for g in gos: ts.append(g[0] + g[2] + 0.2)
        for c in getattr(events, 'cams', []): ts.append(c['t'] + 1.6)
        ts += [end + 1.0]
        for st in stamps: ts.append(st["t"] + 0.5)
        for c in counts: ts.append(c["t"] + 1.5)
        ts = sorted(ts)
        fr = asyncio.run(film(ep, beats, caps, stamps, counts, kicks, end, total, SITE, work, 30, os.path.join(HERE, "fonts"), stills=ts, mv=moves(beats, gos)))
        from PIL import Image
        ims = [Image.open(os.path.join(fr, f"{i:05d}.jpg")).resize((216, 384)) for i in range(len(ts))]
        cols = 8; sheet = Image.new("RGB", (216 * cols, 384 * ((len(ims) + cols - 1) // cols)))
        for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 216, (i // cols) * 384))
        p = os.path.join(a.out, f"{ep['id']}-stills.png"); sheet.save(p); print("stills:", p, [round(x, 1) for x in ts]); return
    out = os.path.join(a.out, f"{ep['id']}.mp4")
    if a.encode_part:
        pa, pb = (int(x) for x in a.encode_part.split(":"))
        pth = os.path.join(work, f"part-{pa:05d}.mp4"); encode(os.path.join(work, "frames"), audio, pth, fps, part=(pa, pb)); print("wrote", pth); return
    if a.mux:
        parts = sorted(os.path.join(work, f) for f in os.listdir(work) if f.startswith("part-") and f.endswith(".mp4"))
        mux(parts, audio, out); print("wrote", out, "from", len(parts), "parts"); return
    if a.encode_only:
        encode(os.path.join(work, "frames"), audio, out, fps); print("wrote", out); return
    ch = tuple(int(x) for x in a.chunk.split(":")) if a.chunk else None
    print("pictures…", flush=True)
    frames = asyncio.run(film(ep, beats, caps, stamps, counts, kicks, end, a.only or total, SITE, work, fps, os.path.join(HERE, "fonts"), mv=moves(beats, gos), chunk=ch))
    if ch:
        print("chunk done", ch, "of", int((a.only or total) * fps)); return
    print("encoding…", flush=True)
    encode(frames, audio, out, fps)
    print("wrote", out)


if __name__ == "__main__":
    main()
