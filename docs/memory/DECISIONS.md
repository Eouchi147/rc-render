# DECISIONS · rc-render

Every decision, with its date and reason. Append only: new decisions go at the bottom. To change one, add the new decision and mark the old one "SUPERSEDED on <date> by D<n>".

Seeded on 17 Nov 2026 from AGENTS.md and the commit history.

D1 · standing · The repo and its releases are public: no secrets, no client material, nothing personal; agents never handle API keys. Source: AGENTS.md.

D2 · standing · Dispatch through the REST API with ref as a branch or a full commit hash; one stills run in flight per builder, because the runner queue is shared. Source: AGENTS.md.

D3 · 23 Oct 2026 · AGENTS.md is the entry point for agents, and the KINOFORGE lanes point to the kinoforge repo's rules and playbooks. Source: commit 1ed26ca.

D4 · 23 Oct 2026 · Music comes from Wikimedia Commons with its licence record; sound effects come from the CC0 BigSoundBank, each licence checked on its page. Source: commits 81976ae, 7101d89 and 55558e1.

D5 · 17 Nov 2026 · The owner's standing instruction, in its public version, is installed as CLAUDE.md, and project memory now lives in docs/memory/. Source: the owner's message of 17 Nov 2026.
