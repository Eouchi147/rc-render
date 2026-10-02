# Long-form round brief: one agent, one film, script to compiled film

You make one complete long-form deep dive (16:9, about 10 minutes) for the history channel Residual Continuum, from
research to a compiled, previewed film module. Ten films are already finished this way (LF.01 to LF.10: Under Giza,
Atlantis, Göbekli Tepe, The Comet and the Cold, The UFO Files, Impossible Stones, Gunung Padang, Derinkuyu, Ancient
Astronauts, Voynich); the owner loved them. The goal of the channel: social buzz and to be the number one reference on
these subjects, without ever trading honesty for clicks.

Lessons from the review of round 2 (apply them):
- The first 3 seconds: the hero image must be fully drawn and instantly recognisable. In LF.09 the famous carved lid of
  the cold open was drawn as a plain slab, the weakest moment of that film. If the object is famous, draw its silhouette
  and the details people know it by, with light and depth, before anything else appears.
- Cross-sections, maps and diagrams must read on a phone: at most about 6 labels on a panel, generous spacing, back layers
  dimmed for depth. LF.08's underground cross-section was too busy. Two clear panels beat one crowded one.
- Each film is reviewed from its contact sheet before it is rendered: a panel that is empty, crowded or wrong is sent back.

Workspace: `/home/claude/rc2/reels` (a clone of the render farm repo). Scratch: `/tmp/claude-0/` and your scratchpad.

## Part A: the script (`films/long/<id>/script.json`)
Follow `films/long/LONG_BRIEF.md` exactly (identity, shape, research, markup, schema, checks) and the narration rules
of `films/rewrite/CASE_BRIEF.md` Part 1. Lessons from round 1:
- 1,450 to 1,650 spoken words (round 1 ran 1,600 to 1,690 words = 10.6 to 10.9 min). 4 to 6 chapters.
- The first 3 seconds decide everything: open on the single most astonishing true image and the child's question.
- `yt_title`: <= 60 characters so it is not cut off, curiosity without lies; `hook` <= 8 words.
- Facts: the Short(s) of the same subject (their spec in `films/fNN.py`, narration in `films/rewrite/<id>.json`) plus
  peer-reviewed papers and excavation reports found with web search; every added fact in `facts_added` with its source;
  never invent numbers, quotes or names; where sources disagree, say so. Any claim about a real living person (a
  retraction, an accusation, a firing) must be checked against a primary source.
- Lint every narration line with `free/heteronyms.py` (`H.lint(line)` returns a list of problems; empty = ok).
- New spoken names go in `names` with how they are said. Do NOT edit `free/voices.py`; the editor adds them.

## Part B: the film (`films/long/<mod>.py`)
Follow `films/long/SCENE_BRIEF.md` exactly (read `films/long/LONG_ENGINE.md` and `films/long/demo.py` first). Then study
the finished round-1 modules for the patterns that work around the engine's limits, and reuse their helpers by copying
them into your module (never import another long module):
- `films/long/lf_gobekli.py`: tagged camera zooms + `_attach()` to add elements mid-line on a revisited panel; a speech
  `Clock` to time build-ins inside a sentence; covers to fake fades and motion.
- `films/long/lf_atlantis.py` and `lf_sky_fell.py`: lines read from script.json at compile time with `[go:]` inserted;
  ledgers that fill row by row; balances; sky covers.
- `films/long/lf_under_giza.py`: a five-row ledger whose grade chips pop as each grade is said.
Rules that matter:
- The verdict key is the Shorts' spelling: Ruled out = `debunked`, Awaiting evidence = `unsupported`, Open question =
  `contested`, Mixed record = `mixed`, Plausible = `plausible`, Strong evidence = `strong`, Established = `solid`.
- The opening chapter (hook + title beat) gets no card; the title beat has role "title" and `"intro": True`.
- `description` = the script's description with the chapter list replaced by `{chapters}`.
- Compile and preview ONLY in your sandbox `/tmp/claude-0/sbx_<id>` with all three RC_FILMS_ variables (see SCENE_BRIEF).
  Look at every still and fix what is wrong. Four other authors share the 2 CPUs: run one preview at a time, and prefer
  previews of the panels you changed (e.g. render stills for chosen steps with your own small playwright script).
- Edit only `films/long/<id>/script.json` and `films/long/<mod>.py`. Never run films.py without the RC_FILMS_ variables.
  Do not run longjob.py or reel.py (the farm voices and renders).

## Reply with
id, module, spoken words, chapters (titles and word counts), verdict, yt_title, hook, the 8 most important facts added
(with sources), the names to add to the pronunciation lexicon (with how they are said), the number of panels, the paths
of the 6 best stills, and anything you were unsure of.
