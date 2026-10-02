# Residual Continuum · long-form deep dives (16:9, 8 to 12 minutes)

Sam's ask (1 Oct 2026): "long form 16:9, 8 to 12 minute deep dive videos, same standards we've established so far".
YouTube is the priority (that is where the money is), so these must be the best history videos on their subject:
gripping from the first second, clear to a newcomer, exact enough for a specialist, honest about uncertainty.

Read first: `films/rewrite/CASE_BRIEF.md` (the standard, narration markup, honesty rules) and the project identity below.
Everything there applies. This brief only adds what is different for long form.

## Identity (non-negotiable)
- A curious friend who has read everything and still says "we don't know" like it is the best part. Ask the child's
  question first, then answer like the grown-up who checked. Wonder before verdict. One dry joke per chapter at most,
  never at anyone's expense. Numbers land like punchlines. Every faith and every challenger presented at their strongest.
  End on what would change our minds.
- No proof language ("proves", "undeniable", "definitely"). Use "suggests", "the evidence points to", "we can't rule out".
- No em dashes or en dashes in prose. British spelling. Dates hedged (about, around, BCE/CE).
- Religion: treated with respect, faith never rated, never contradict the Quran. Never mention any "invisible spine" or
  hidden religious frame. Human remains with care and dignity.
- Never reveal anyone's email. No outbound links except DOIs and Wikimedia Commons.

## Shape of a deep dive (about 10 minutes, 1,400 to 1,700 spoken words)
1. **Cold open** (20 to 40 s): the single most astonishing image and the child's question. No logo, no "in this video".
   Hook in the first 3 seconds.
2. **Title beat** (5 s): the film's title said once, the promise of the film in one line.
3. **4 to 6 chapters** (1.5 to 2.5 min each), each a small story with the house arc: where and when (one vivid
   picture), the claim at its strongest, how we know (one everyday analogy per method), the twist, a one-line landing.
   Each chapter has a short title for the on-screen chapter card and the YouTube chapters list.
4. **The weighing** (60 to 90 s): what is established, what is open, what is ruled out, said plainly; the verdict in the
   exact grade words (Established, Strong evidence, Plausible, Mixed record, Open question, Awaiting evidence, Ruled out).
5. **What would change our minds** (20 to 40 s): the test, the dig, the scan, the date that would settle it.
6. **Close** (10 s): a quiet last image and "Weigh it yourself."

Continuous take, no cuts: chapters are rooms of the same wall; the camera glides from one to the next. Every argument is
drawn and animated while it is said (maps, cross-sections, iso models, timelines, charts that build, people for scale).

## Facts and research
- Your facts base: the short films of the same subject (their narration in `films/rewrite/<id>.json` or the spec in
  `films/fNN.py` / `films/lg_*.py`, their on-screen labels, their `sources` strings) and the project's case pages.
- You may and should add facts from the peer-reviewed literature and major excavation reports, found with web search.
  For every fact you add, record the source (author, year, journal, DOI when there is one) in `facts_added`. Prefer
  primary papers. Never invent numbers, quotes or names. If sources disagree, say so in the film.
- New proper names spoken aloud must be listed in `names` (with how they are said, e.g. "Göbekli Tepe: guh-BECK-lee
  TEP-eh") so the pronunciation lexicon can be checked before voicing.

## Narration markup (same as the shorts)
Every sentence starts with `[act:...]`; `[p:0.9]` before a sentence carrying a hard idea or number; `^` before 1 to 3
stressed words (never directly before `{`); numbers read aloud as `{1947|nineteen forty-seven}`; `[d:mood]` at line
starts where the mood shifts; heteronyms with their sense (`record@noun`, `lead@metal`, `read@past`, ...). Plain letters
only in spoken words (no macrons or dotted letters). Lint each line with `free/heteronyms.py` (see CASE_BRIEF).
Do NOT write `[go:]` markers: the scene author adds them.

## What to deliver: `films/long/<id>/script.json`
```
{
  "id": "<id>", "kind": "theme" | "case", "series": "<File name>",
  "title": "<on-screen title>", "yt_title": "<YouTube title, <= 70 chars, curiosity without clickbait lies>",
  "verdict": "<exact grade words>", "hook": "<the cold-open question, <= 8 words>",
  "chapters": [
    {"title": "<chapter title, <= 32 chars>",
     "beats": [
       {"role": "hook|world|collision|cost|reversal|tag|weigh|test|close",
        "lines": ["[d:...][act:...] ...", "..."],
        "shots": [ {"id": "s1", "say": "<which words it covers>",
                    "draw": "<what is drawn and how it animates, true to the numbers said>",
                    "reuse": "<optional: an existing short's scene to adapt, e.g. 'big-void shot 3, muon detector map'>"} ]}
     ]}
  ],
  "description": "<YouTube description: 2 short paragraphs, then 'Chapters' with mm:ss placeholders, then Sources>",
  "sources": ["Author Year, Journal, doi:...", "..."],
  "facts_added": [{"fact": "...", "source": "..."}],
  "names": [{"name": "...", "say": "..."}],
  "words": <spoken word count>
}
```
Shots: about one new picture every 8 to 15 seconds of narration (so 40 to 70 shots in all). Draw for a 16:9 frame
(1778 wide x 1000 tall, caption band at the bottom, keep drawings in x 80..1700, y 120..820). Prefer drawing to text:
labels of 1 to 4 words, no paragraphs on screen.

## Check before you reply
- Word count 1,400 to 1,700 spoken words (strip markup), 4 to 6 chapters, cold open under 40 s.
- Every added fact has a source in `facts_added`; every source in `sources`.
- No em/en dashes in spoken text, no proof language, verdict words exact.
- Reply with: id, word count, chapter titles with their word counts, the 10 most important facts added (with sources),
  names to check, and anything you were unsure of. Do not edit any file outside `films/long/<id>/`.
