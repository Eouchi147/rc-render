# rc-render: start here (every agent)

A public render farm on free GitHub runners, shared by several of Sam's projects. Know which project you work for.

- **KINOFORGE lanes** (`films.yml`, `stills.yml`, `remux.yml`, `chain.yml`, `tools/getstills.sh`; releases `kino-films`,
  `stills`, `film-logs`): the rules, the memory and the playbooks live in the KINOFORGE repo. Read
  https://github.com/Eouchi147/kinoforge/blob/main/AGENTS.md first, then its `docs/PLAYBOOKS/render-on-github.md`.
  Log every change to these workflows in KINOFORGE's `docs/LOG.md` and `docs/WORKFLOWS.md`.
- **Other lanes** (`render.yml`, `dark*.yml`, `voice*.yml`, `long.yml`, `clips.yml`, `sfx.yml`, `style.yml`,
  `diorama.yml`): see `README.md`; do not change them for KINOFORGE work.

Rules for everyone here: the repo and its releases are public (no secrets, no client material, nothing personal); never
handle API keys; dispatch through the REST API (`gh api -X POST .../dispatches`) with `ref` as a branch or a FULL commit
hash; one stills run in flight per builder (the runner queue is shared); commit only your own files, pull with rebase
before you push, never force-push.
