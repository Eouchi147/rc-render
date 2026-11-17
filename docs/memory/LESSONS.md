# LESSONS · rc-render

Every mistake and the rule it earned. Append only, dated (UTC).

Seeded on 17 Nov 2026 from the commit history.

L1 · 23 Oct 2026 · A film's second insert never showed, because inserts were laid by frame count. Rule: lay inserts by time. Source: commit 54c1bb4.

L2 · 22 Oct 2026 · The stills lane loaded the runner queue every project shares. Rule: several frames per runner (per_job, default 4). Source: commit 4169b30 ("to cut queue load").

L3 · 22 Oct 2026 · Playwright 1.56 could not install its dependencies on ubuntu-latest (26.04). Rule: pin the runner image (ubuntu-24.04). Source: commit 4ee664e.
