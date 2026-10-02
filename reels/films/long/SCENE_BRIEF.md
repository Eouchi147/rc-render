# Scene authoring brief: turning a long-form script into a 16:9 film (Residual Continuum)

You turn one finished deep-dive script (`films/long/<id>/script.json`) into a compiled 16:9 long film: a Python module
`films/long/<mod>.py` whose `EPISODES()` returns `[ep]`, built with `mural.remix()` on the 16:9 wall. Another step voices
and renders it on the render farm, so the module must compile cleanly and every panel must look right.

## Read first
1. `films/long/LONG_ENGINE.md` (the frame, safe areas, cameras, the wall, chapter cards, inset()/tall(), fields, pitfalls).
2. `films/long/demo.py` (a complete working example: copy its patterns: B(), scenes as functions, ep fields, remix).
3. `films/rewrite/CASE_BRIEF.md` Part 2 (the pictures standard: draw the idea while it is said, build-ins in the order
   named, honest schematic drawings true to the numbers) and the best Shorts' scene functions it lists
   (`capsian_m()`, `el_guettar_m()` in f15.py; `nebra_m()`, `great_year_m()` in f08.py; `alexandria_m()` in f12.py).
4. `films/illus.py` helpers and the EL.* vocabulary in `films/kit.js` (label, cap, pin, line, arrow, poly, rect, circle,
   glow, person, dim, map, axis, band, water, stars, iso, group, panel, boat, scale and the LIB monuments).
5. Your script: every chapter, beat, line and shot (`say` = the words it covers, `draw` = what to draw, `reuse` = an
   existing Short scene to adapt).

## What to build
- One scene per script shot, as functions like the demo's (a few shots may share a panel through `line_adds`/`beat_adds`
  when the script's `draw` is a new framing or an addition on the same picture). Draw exactly what `draw` asks, true to the
  numbers said. Where `reuse` names a Short's scene, find it (grep films/*.py; the Shorts' specs are functions returning
  episodes whose `shots` are scenes) and reuse it with `inset()` (portrait scene through a window, s >= .75) or `tall()`,
  or redraw it wide when a 16:9 composition is clearly better. Deep-copy before editing; never edit another file.
- Beats: one ep beat per script beat, `{"role", "visual": {"from": <shot index>}, "lines": [...]}`. Keep every narration
  line EXACTLY as in script.json, only adding `[go:N|t]` markers (N = the ep's shot index, t = glide seconds, e.g. 1.6) at
  the start of the sentence where the picture changes (after the `[d:...]` mood tag if the line starts with one, before
  `[p:...]`/`[act:...]`; follow how the demo places `[go:5]`). If the compile's lint rejects a line, make the smallest fix.
- Chapters: the first beat of each story chapter carries `"chapter": "<script chapter title>"`. The cold-open/opening
  chapter gets NO card. The card holds for the beat's FIRST sentence, so a chapter's first beat needs at least two
  sentences, the first being a good line to hold on a title card. The title beat: role "title", `"intro": True`.
- ep fields (see demo.py): `id`, `code`, `series`, `title`, `case`, `verdict` (use the same verdict key spelling the Shorts
  use for this grade: grep an existing Short with the same grade), `claim`, `mood`, `hook_text` (the script's hook, with one
  *emphasised* word), `beats`, `shots`, `sources` (a " · " separated short list of the key sources with DOIs, like the demo),
  `post`, `hashtags`, `aspect: "16:9"`, `intro_title`, `yt_title`, `description` (the script's description with the mm:ss
  chapter placeholders replaced by `{chapters}`), `end_line` (one quiet line for the end card, from the script's close).
- Frame: 1778 x 1000; drawings in x 80..1700, y 120..800; nothing important under y 800 (captions) or above y 110 (HUD).
  Labels 1 to 4 words, size >= 24 (main ones 30 to 34), never overlapping, never off-frame. No em or en dashes anywhere
  on screen. Prefer drawing to text. A new picture every 8 to 15 s of narration. Build-ins start about 0.5 s and follow
  the narration's order. Make it beautiful: depth (dim back layers), light (glow), people for scale, motion (draw, rise, pop).

## Compile and look (your sandbox only)
```
cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_<id>/boards && cp ../episodes/files.json /tmp/claude-0/sbx_<id>/
RC_FILMS_OUT=/tmp/claude-0/sbx_<id> RC_FILMS_EPS=/tmp/claude-0/sbx_<id>/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_<id>/boards python3 films.py long.<mod>
RC_WAIT=6000 RC_FILMS_OUT=/tmp/claude-0/sbx_<id> python3 preview.py <id>     # stills: /tmp/claude-0/pv_<id>_<n>.png
```
NEVER run films.py without all three RC_FILMS_ variables (it would overwrite the repo's episodes/files.json and out/).
Look at EVERY still (Read the PNG). Fix overlaps, text off-frame or under the captions, empty or confusing panels, wrong
scale, labels too small. Re-run until clean. Do not run `longjob.py prep/chunk/all` or `reel.py` (voicing and rendering
happen on the farm). The machine has 2 CPUs shared with three other authors: run one preview at a time.

## Rules
- Edit ONLY `films/long/<mod>.py` (and scratch files in your sandbox/scratchpad). Do not touch kit.js, mural.py, films.py,
  illus.py, preview.py, reel.py, longjob.py, voices.py, any fNN.py/lg_*.py, episodes/, or the script.json. If the engine
  cannot do something you need, work around it in your module and report it.
- Honesty: drawings schematic but true to the numbers said; no invented details; claims drawn in the "claimed" (dotted)
  style, evidence solid. Religions treated with respect; no scripture brought in. No email addresses anywhere.

## Reply with
The module path, number of panels/scenes, chapters, a one-line list of the authored scenes (grouped by chapter), which
Short scenes you reused, any lines you had to change (old and new), engine limits you hit, and the paths of the 8 stills
that best show the film.
