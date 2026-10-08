#!/bin/bash
# darkengine: render a film.   Usage:  bash render.sh test
# Works with the bash that comes with macOS (3.2) and on Linux. Run setup.sh once first.

cd "$(dirname "$0")" || exit 1
HERE="$(pwd)"

usage() {
  echo "Usage:  bash render.sh test"
  echo "  test   the 16-second Bamberg test clip (picture, narration, sound and score)"
}

case "${1:-}" in
  test) ;;
  *) usage; exit 1 ;;
esac

if [ ! -x "$HERE/.venv/bin/python" ] || [ ! -f "$HERE/.setup-done" ]; then
  echo "Setup has not finished yet. Run this first:"
  echo "  bash \"$HERE/setup.sh\""
  exit 1
fi

. "$HERE/.venv/bin/activate"
export DARK_ROOT="$HERE"
export RC_TTS_DIR="$HERE/models"
PY="$HERE/.venv/bin/python"
cd "$HERE/film" || exit 1

start=$(date +%s)
echo "Rendering the Bamberg test clip."
echo "The first time, the scene is painted before any frame is rendered: allow some extra minutes."
for step in audio video mux; do
  echo "- $step"
  "$PY" clip_test.py "$step" || { echo; echo "The $step step failed; the lines above say why."; exit 1; }
done

mins=$(( ($(date +%s) - start + 59) / 60 ))
out="$HERE/out/bamberg_test_clip.mp4"
copy="$(dirname "$HERE")/Bamberg test clip (Mac render).mp4"
if [ -f "$copy" ] && [ ! "$copy" -ot "$out" ]; then video="$copy"; else video="$out"; fi
echo
echo "Done in about $mins min. Your video is here:"
echo "  $video"
if [ "$(uname)" = Darwin ]; then open -R "$video" 2>/dev/null; fi
exit 0
