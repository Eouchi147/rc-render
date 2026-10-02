# The long-form engine (16:9): what a scene author needs

Long films are 16:9 (1920 x 1080, 30 fps, 8 to 12 minutes), one continuous take across a **wall** of panels, like the
Shorts' murals, with chapter rooms and a landscape HUD. The Shorts (9:16) are untouched: every 9:16 page, board and frame
is byte for byte what it was (the 16:9 code lives in `//<16:9 ... //16:9>` blocks of `kit.js`, which `films.py` strips from
9:16 pages, in `mural.wall()`, and in new names in `free/reel.py`).

Working example: `films/long/demo.py` (95 s: 87 s of narration and the 8 s end card; intro title, 2 chapters, a sky, a map, a timeline, a section, an iso model, a
chart that builds, a reused 9:16 map from the Short "capsian" through a window, a night sea). Read it next to this page.

## 1. The frame and its safe areas

The frame is **1778 x 1000 units** (1 unit = 1.08 px of the video). A panel of the wall is exactly one frame.

```
 y 0   +--------------------------------------------------------------------------------------+
       | (o) RESIDUAL CONTINUUM - LF.00 . SERIES                          01  CHAPTER TITLE     |  HUD: y < 110
 110   |  Hook title (first ~3 s only, x < 1000, y < 280)                                      |
       |                                                                                      |
       |                    drawings: x 80..1700, y 120..800                                  |
       |                    important text: y 130..780                                        |
 800   |                                                                                      |
 815   |              [ captions: 2 lines max, x 280..1500, centred ]                          |  captions: y > 815
 1000  +================ progress bar along the bottom edge ===============  note (tiny) ----+
```

- **Brand** top left (x < 760, y < 110), **current chapter** top right (x > 1250, y < 110; it appears 2.4 s after the
  chapter starts, once its card has had the screen), **captions** bottom centre (y > 815, about 1320 px wide, two lines at
  most), **progress bar** on the bottom edge (ticks at chapter starts), a tiny note bottom right.
- The **hook title** sits top left for the first ~3 s: labels of the opening panel that would land above y 300 wait until
  it clears (films.py does it).
- The **intro title card** (`intro_title`) covers the whole frame during the title beat, the wall dimmed under it; the
  **end card** covers everything after the last word (8 s: the verdict chip, "Weigh it yourself.", `end_line`, sources).
- Every beat pushes in slowly (up to 3%) on top of a 2.5% overscan: keep text 20 units clear of the safe-area lines.

## 2. Cameras

- A scene's `"cam": [z, x, y]` puts the point (x, y) of its panel **at the centre of the picture** (panel units; not the
  Shorts' pivot at (500, 860)). Default `[1, 889, 500]`: the whole panel.
- At z = 1 the only centre that keeps the picture inside its panel is (889, 500), so the wall **clamps** any cam with
  z >= 1 to stay inside the panel (z = 1.3: x 684..1094, y 385..615). To show more than a panel, use a tall panel (below).
- A new framing of the same panel: `cams={shot: cam}`, `beat_adds={beat: (els, cam)}`, `line_adds={(beat, line): (els, cam)}`,
  exactly as in `remix()`. A move to another panel: a `[go:N|t]` marker (N = the ep's shot index; t = the glide, at least).
- Glides are timed by distance (1.4 s close by, 1.2 + d/3000 s otherwise, at most 2.6 s); a long glide lifts the camera
  off the wall (`hop` = .08 + d/7000, at most .5) and comes back in.
- Text keeps its size against the authored zoom (labels do not grow when you frame a detail at z 1.4), but shrinks with
  the wall while the camera lifts off between panels.

## 3. Writing a 16:9 scene

A scene is a dict, as in the Shorts: `{"base": ..., <base params>, "cam": [...], "els": [...]}`, element vocabulary of
`kit.js` (EL.*: label, cap, pin, line, arrow, poly, rect, circle, glow, person, dim, map, axis, band, water, stars, iso,
group, panel, and the LIB monuments) and the helpers of `films/illus.py` (label, arrow, line, glow, person, dot, box...),
all in panel units.

- `"in"`: seconds after the camera sets off for the panel (the start of the glide). Build in the order the narrator names
  things, 0.6 to 1.5 s apart; nothing important before it is said. `fx`: draw, fill, pop, rise, type, fade.
- Bases in 16:9 (defaults follow the panel's width): `sky` (ground y 760, sun at 70% of the width, ridges and stars across),
  `section` (ground y 300, strata below, layer names at x `lx`), `dark` (warm dark, `stars`, `floor`), `map` (sea and grid),
  `plan` (north arrow top right), `paper` (a 1000 x 700 sheet, centred). Pass `"sun": [x, y, r]` / `False`, `"ground"`, etc.
- Elements with landscape defaults: `stars`, `water` (x across the panel), `title` (x centred), `iso` (centre 889, 620).
- Maps: `films.View(lon0, lon1, lat0, lat1, rect=(90, 120, 1600, 680))` fits a lon/lat box in the drawing zone;
  `v.p(lon, lat)`, `v.land()`, `v.km(100)` (see `range_map()` in the demo).
- Labels: 1 to 4 words, size >= 24 (30 to 34 for the main one), never on top of each other, never under the captions.
  No em or en dashes anywhere on screen (films.py refuses them).
- Timelines and charts build: `axis` + `band` (fade), a thick `line` with `fx: draw` is a bar that grows left to right,
  dots that `pop` one per unit count along with it (see `timeline()` and `chart()` in the demo).

## 4. The wall

`mural.remix(ep)` on an ep with `"aspect": "16:9"` calls `mural.wall(ep, ...)` (or call `wall()` yourself to set
`cols`, `gap`, `rooms`, `hold`):

- Panels are hung **in the order the story first visits them**, in rows of up to `cols` (3) that snake (a meander: each row
  starts under the end of the last and runs back). With `rooms=True` every chapter starts a new row: a room of the wall.
- **Chapter cards**: a beat with `"chapter": "Title"` (optional `"chapter_kicker"`, default "Chapter N") gets a drawn card
  (the number large and faint, a kicker, a rule that draws itself, the title rising in) on its own panel at the head of the
  room. The beat opens with a glide to the card; the card holds for the beat's **first sentence** (`hold=1`), then the
  camera glides to the beat's own panel (`visual.from`) at the start of the next sentence. A one-sentence chapter beat moves
  on as its last word ends. If you put a `[go:]` in that first sentence, it wins. Chapter titles: <= 40 characters, plain.
- **Intro title**: `"intro_title"` on the ep, shown over the beat with `"role": "title"` (or `"intro": true`), at least
  3.4 s; say the title aloud in that beat. Without a title beat it shows from 3.3 s to 7.3 s.
- Every element is built **once** (kit.js `WALL`): a step lists only what it adds (a panel's content on its first visit,
  the thread to it, additions). Frames only touch panels near the camera (the rest are `display:none`), so frame time does
  not grow with the number of panels (see section 8).
- `alias={shot: earlier shot}` returns to an earlier panel (with the shot's own cam); `adds={shot: [els]}` adds to a panel
  on its first visit. All as in `remix()`. `[k:]` and `[cam:]` markers are dropped.

## 5. Reusing a scene from a Short

Two ways, both in `films/mural.py`:

- `inset(scene, s=None, crop=None, at=None, els=(), base="dark", cam=None, drop=TEXT, keep=None)`: the 9:16 scene shown
  through a **window** of a 16:9 panel. `crop = [x, y, w, h]` of the portrait frame (default its drawing zone
  `[0, 260, 1000, 1160]`), scaled by `s` (default: a window 740 units tall), its top left corner at `at` in the panel
  (default centred, 40 above the middle). A portrait point (x, y) lands at `at + ((x, y) - crop[:2]) * s` (use it to aim
  arrows from the window to your 16:9 elements). `els`: 16:9 elements drawn around or over the window. The Short's text
  cards (`para`, `num`, `title`, `q`, `cap`) go unless `keep(e)` keeps them; its build-ins play on the panel's clock. Keep
  `s` >= .75 so its labels stay legible (25 units x .75 = 19). Edit the scene first if a label does not belong (the demo
  drops the Pantelleria pin).
- `tall(scene, cam=None)`: the 9:16 scene hung on the wall **as it is**, a 1000 x 1778 panel with extra space either side.
  The default camera `[.66, 500, 880]` frames its whole drawing zone (zoomed out, the wall dark around it); give later
  steps closer cams (`cams=`, `beat_adds`) to tilt down it (sky, ground, strata). Its own Shorts `cam` is ignored.

## 6. The film's fields

Besides the Shorts' fields (`id`, `code`, `series`, `title`, `case`, `verdict`, `claim`, `mood`, `hook_text`, `beats`, `shots`,
`sources`, `post`, `hashtags`):

| field | what it does |
|---|---|
| `aspect: "16:9"` | makes it a long film (16:9 page, wall, landscape HUD, `longjob.py`) |
| `intro_title` | the full-frame title card over the title beat |
| `end_line` | the line under "Weigh it yourself." on the end card |
| `yt_title` | YouTube title (<= 70 characters), written to `<id>.description.txt` |
| `description` | YouTube description; `{chapters}` is replaced by the chapter list with real times |
| beat `chapter`, `chapter_kicker`, `intro` | chapters (cards, HUD, YouTube list) and the title beat |
| `note` | the tiny note bottom right (default "Schematic reconstruction · sources in the description") |

Narration markup is the Shorts' (see `films/rewrite/CASE_BRIEF.md`); the scene author adds the `[go:N|t]` markers at the
start of the sentence where the picture changes.

## 7. Commands

Compile and look (sandbox only; never without the RC_FILMS_ variables):
```
cd /home/claude/rc2/reels/films && mkdir -p /tmp/claude-0/sbx_engine/boards && cp ../episodes/files.json /tmp/claude-0/sbx_engine/
RC_FILMS_OUT=/tmp/claude-0/sbx_engine RC_FILMS_EPS=/tmp/claude-0/sbx_engine/files.json RC_FILMS_BOARDS=/tmp/claude-0/sbx_engine/boards python3 films.py long.demo
RC_WAIT=9000 RC_FILMS_OUT=/tmp/claude-0/sbx_engine python3 preview.py lf-demo     # 960x540 stills of each step: /tmp/claude-0/pv_lf-demo_<n>.png
```
(`preview.py` sees the 16:9 page and uses a landscape viewport; `RC_DPR=2` for full resolution. Its stills have no HUD.)

Voice, film, assemble (`free/longjob.py`; `--eps`/`--page` default to `$RC_FILMS_EPS` / `$RC_FILMS_OUT/<id>.html`):
```
cd /home/claude/rc2/reels/free
export RC_FILMS_OUT=/tmp/claude-0/sbx_engine RC_FILMS_EPS=/tmp/claude-0/sbx_engine/files.json
python3 longjob.py prep lf-demo --bundle /tmp/claude-0/lf_bundle               # voice + timing + mix -> job.json, page.html, mix.wav
python3 longjob.py stills --bundle /tmp/claude-0/lf_bundle --at 1 14.8 26.5 92 # exact frames with the HUD -> <bundle>/stills/
python3 longjob.py chunk 1 3 --bundle /tmp/claude-0/lf_bundle --keep-edges 1   # chunk K of N (K = 1..N), any machine, any order
python3 longjob.py chunk 2 3 --bundle /tmp/claude-0/lf_bundle --keep-edges 1
python3 longjob.py chunk 3 3 --bundle /tmp/claude-0/lf_bundle --keep-edges 1
python3 longjob.py seam 2 3 --bundle /tmp/claude-0/lf_bundle                   # optional: the joins are byte-identical
python3 longjob.py assemble --bundle /tmp/claude-0/lf_bundle --out /tmp/claude-0/lf_demo.mp4
python3 longjob.py all lf-demo --bundle DIR --chunks 3 --out OUT.mp4           # all of it on one machine
RC_EPISODES=<files.json> python3 reel.py lf-demo --out DIR                     # the same through reel.py (RC_LONG_CHUNKS, default 1)
```

**On the farm**: run `prep` once (it needs the TTS models and the cache); ship `job.json` and `page.html` (about 0.5 MB) to
each chunk machine, which needs this repo (fonts, `reel.py`), Playwright's Chromium and ffmpeg, but not the TTS; collect
`seg_K_of_N.mp4` + `seg_K_of_N.json` from every machine into the bundle with `mix.wav`, then `assemble`. Chunks are
independent: each replays the film from frame 0 as state only (about 6 s for the end of a 12 minute film), then films
its own frames straight into ffmpeg (no frames on disk). `assemble` refuses a missing, overlapping or short segment, and
writes OUT (default `<bundle>/<id>.mp4`) with `OUT.chapters.txt` (YouTube chapters, first at 0:00), `OUT.description.txt`
(`yt_title`, then `description` with its `{chapters}` filled in) beside it, and `qa.json` (frames, durations, integrated
loudness about -14 LUFS, peak); it exits non-zero when a check fails.

## 8. Performance

Measured on this 2-CPU machine (October 2026):

- **Built once.** A 77-panel stress wall (72 scenes, 5 chapter cards; a 10 minute film has 40 to 80 panels) is 3.3 MB of page
  data and 12,000 DOM nodes and loads in 0.5 s. Repeating the wall in every step, as the Shorts' murals do, would have
  been about 128 MB.
- **Culled.** Each frame updates only the panels near the camera (1 at rest, 3 to 6 while it lifts off between panels): the
  page's drawing costs 0.4 ms a frame at 77 panels, the same as at 10. Drawing every panel (`window.__wallAll = 1`, a QA
  switch) costs 4 to 7 ms and styles every node.
- **Filming** (1920 x 1080, film look in ffmpeg): 7.7 to 8.8 s of compute per second of film (Chromium's screenshot and
  ffmpeg's film look run side by side, about 0.25 s a frame). The 95 s demo in 3 chunks: 280 s, 276 s, 243 s. A 10 minute
  film is about 85 minutes of compute: in 6 chunks on 6 machines, about 15 minutes. Faster machines speed up ffmpeg most.
- **Pre-roll** (frames before a chunk, state only) costs about 0.3 ms a frame (2,835 frames in 0.8 s): the last chunk of a
  12 minute film replays its 20,000 earlier frames in about 6 s.
- **Seams.** `seam 2 3` and `seam 3 3` on the demo: the frames either side of each join are byte-identical to a single pass.
- **Disk.** No frames on disk (piped to ffmpeg). The demo: 66 MB of video (5.4 Mbit/s at CRF 19 with grain), mix.wav
  18 MB; a 10 minute film is about 400 MB of segments and a 115 MB mix.wav.

## 9. Pitfalls (found while building it)

- A 16:9 cam at z = 1 with any centre other than (889, 500) shows the bare wall and the thread at one edge: the wall now
  clamps it, but author for (889, 500) and zoom in to frame details.
- `"in"` times start when the glide to the panel starts, not when it lands: the first 1.5 to 2 s are mid-flight. Start
  important build-ins at about 0.5 s (they are seen as the camera settles) and the rest after the panel is still.
- Labels of a reused 9:16 scene shrink with `s`; text cards of the Short are dropped. Check every inset in the stills.
- Random scatters (shells, dots) must be clamped inside their shape; a dot below a curved outline shows on the sand.
- The intro card hides the captions while it is up: put only the title (said aloud) in the title beat.
- A beat's `visual.from` is where the beat *goes*, a `[go:N]` where a sentence goes; panels are hung in that order, so
  a scene first visited late is hung late (fine: the camera always travels to a neighbour).
- Don't render without `prep`'s `job.json` matching the page: `prep` copies the page into the bundle; recompile and
  re-run `prep` after any change to the film (the narration timing and the camera path live in `job.json`).
- `preview.py` stills show each step after `RC_WAIT` ms of real time and no HUD; check the HUD, captions and intro/end
  cards with `longjob.py stills`.
- Byte-identical joins need every frame to be a pure function of the clock *and* of nothing Chromium remembers. A CSS
  transform that changes every frame on a composited element (the Shorts' camera float on the sticky stage) makes Chromium
  keep a raster scale that depends on the frames before, so a chunk's first frame differed by a few glyph pixels from a
  single pass. On a wall the float is drawn inside the SVG (`window.__wallCam`, called by OVERLAY16): no such history.
  Keep it that way: no per-frame CSS transforms, filters or will-change on the stage of a long film.
- Captions come from the narration: a long sentence is cut into even pieces of at most 62 characters (two lines), after a
  comma when it can and never after a little word. Write sentences that read well in two halves.
