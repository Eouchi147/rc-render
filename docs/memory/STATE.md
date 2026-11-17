# STATE · rc-render

Where the project stands now. Rewrite this file so it is true today; do not append to it.

Last rewrite: 17 Nov 2026, from the repo. Before the install merged on 17 Nov, main was at f5adee7 (24 Oct 2026, 02:30 UTC).

## What it is

A public render farm on free GitHub runners, shared by several projects (AGENTS.md). The render workflow makes Residual Continuum's films: each run voices, renders, encodes and checks the films whose ids it is given, one runner per film, and publishes them to the films release (README.md). The KINOFORGE lanes (films.yml, stills.yml, remux.yml, chain.yml, tools/getstills.sh; releases kino-films, stills, film-logs) follow the kinoforge repo's AGENTS.md; for the other lanes (render.yml, dark*.yml, voice*.yml, long.yml, clips.yml, sfx.yml, style.yml, diorama.yml), AGENTS.md points to README.md.

## Where it stands

- Last changes, 22 to 24 Oct 2026 (UTC): the KINOFORGE films lane in parallel parts (bd83cb2), check stills (0e9910c), sound-only remux (7ab38cf), inserts laid by time (54c1bb4), a poster per film (4e8266e), spend records per run (66e8b70), the CC0 sound effects bank (7101d89), and music search and fetch from Wikimedia Commons with licence records (81976ae, a856d2f, f5adee7).
- chain.yml checks follow-up renders every 15 minutes, on a schedule.
- dark.yml (the Dark Corners render, 18 parallel parts by default) starts by hand or on a push to main that changes dark/film/jobs/*.go.

## Not verified on 17 Nov

- The runner queue and the latest runs.
- Whether the pushtest branch holds work that main lacks.
