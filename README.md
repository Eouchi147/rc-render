# rc-render

The render farm for **Residual Continuum** films: each run of the `render` workflow voices, renders, encodes and checks
the films whose ids it is given, one runner per film, and publishes each finished film to the `films` release.
The film specs live in `reels/films` (compiled on the runner), the narrator in `reels/free/voices.py`.
Coherence is the measure, not final demonstration.
