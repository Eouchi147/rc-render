# Bringing a film to the new standard (Residual Continuum)

The owner's standard for every film: **one continuous take, no cuts**; every argument **drawn and animated** (not written
on screen); narration in the spirit of the French science show "C'est pas sorcier": a warm, curious guide who makes
people *understand* and be *fascinated*, self-contained (a viewer who never heard of the subject follows everything),
slowing down on hard ideas. Visual storytelling is paramount. The goal: viral, and the #1 reference on these subjects.

(Restored 2 Oct 2026. The `_seed/` folder of the Shorts' original narrations is not in this repo; compare the finished
narrations in `films/rewrite/<id>.json` with the scenes in the fNN.py files instead.)

Study at least two finished films before writing anything:
- narration: `films/rewrite/<id>.json`, e.g. capsian, el-guettar, nebra-disc, piri-reis, shroud, dating-methods.
- pictures: `capsian_m()` and `el_guettar_m()` in `films/f15.py`; `nebra_m()`, `great_year_m()` in `f08.py`;
  `alexandria_m()`, `piri_reis_m()` in `f12.py`; `sea_peoples_m()`, `shroud_m()` in `f11.py`; `grades_m()` in `f00.py`.
- engine: the docstrings of `films/mural.py` (remix), `films/illus.py` (drawing helpers), and the element vocabulary in
  `films/kit.js` (EL.* builders: rect, circle, line, poly, arrow, label, glow, person, iso, group, panel...).

## Part 1: the narration
- Every line so a newcomer understands: *where and what* (with one vivid picture or comparison), the mystery or
  claim (the challenger at their strongest, posed as a question), *how we know* (one everyday analogy for any method:
  carbon dating, DNA, strata, sediment cores...), then the verdict. Short sentences. Put `[p:0.9]` (or 0.93) before a
  sentence that carries a hard idea or a number.
- Keep, at the same place in the same line: `[d:...]` moods (line start), `[sfx:...]`, `[stamp:...]`, `[count:...]`
  and every `[go:N|t]` marker (it moves the camera; it must stay at the start of the sentence where the picture changes).
  Drop every `[k:...]` and `[cam:...]`.
- Every sentence starts with `[act:<short direction>]`; optional `[tune:rise|fall|level]` after it; `^` before 1 to 3
  stressed words. Never `^` directly before `{`. Numbers the narrator reads: `{1947|nineteen forty-seven}` (digits only
  inside braces). Heteronyms need their sense (`record@noun`, `lead@metal`, `read@past`, `live@adj`, `close@adj`,
  `used@verb`, `wind@air`, `minute@time`, `tear@cry`, `desert@noun`, `present@adj`... see `free/heteronyms.py`).
  Check every string: `cd /home/claude/rc2/reels/free && python3 -c "import json,heteronyms as H; ... print(H.lint(line))"`
  (H.lint(line) returns a list of problems; empty means ok).
- The verdict keeps the film's grade, in the same words (*Ruled out*, *Awaiting evidence*, *Open question*, *Mixed record*,
  *Plausible*, *Strong evidence*, *Established*).
- Spoken words must be plain letters: never ʿ, ʾ, macrons (ā ī ū) or dotted letters (ḥ ṣ ṭ) inside the narration, because the
  narrator spells them out letter by letter ("letter 2bf, A macron, d"). Write the name as it is said (Aad, Tayma, Hijr) unless
  `free/voices.py` LEX already has the scholarly form. Scholarly spellings are fine in on-screen labels.
- Rules: no em dashes or en dashes in prose; British spelling; never "proves", "undeniable", "definitely"; dates
  hedged ("about", "around", BCE/CE); challengers fair; religions treated with respect, faith never rated (only stones,
  dates, layers, skies are weighed), never contradict the Quran; human remains with care and dignity.

## Part 2: the pictures
- **Replace every shot that would be mostly text** (stat cards, quotes, titles, bullet lists, "the verdict" cards) with an
  authored scene that *draws the idea while the narrator says it*: the mound growing layer by layer, a box filling
  with 25,000 shells, ancestry as 100 squares of which 6 turn blue, a sea level line rising over a coast, a timeline
  that draws itself with the claim's date struck through, people walking a route, a cross-section, a sky turning.
- Timing: an element's `"in"` is seconds after the camera arrives on the panel. Choreograph: things appear in the order
  the narrator names them, about 0.6 to 1.5 s apart; nothing important appears before it is mentioned; the scene is
  complete by the end of its lines. Use `fx`: `draw` (lines, arrows, outlines and rings trace themselves), `fill` (bars
  and layers grow from the bottom), `pop`, `rise`, default fade; `op` + `keepop` for dim layers. Ambient life: `glow`
  (lamp/fire), `person` figures for scale.
- Labels: few, short (1 to 4 words), never on top of each other, never cut by the frame edge (anchor long labels with
  `a="end"`/`"start"`).
- Honesty: drawings are schematic but true to the numbers said (heights, dates, proportions). No invented details.
