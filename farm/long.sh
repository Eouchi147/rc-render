#!/bin/bash
# long.sh: the three steps of a long film (16:9) on GitHub runners (workflow .github/workflows/long.yml).
#   long.sh prep <id> <module>   compile the film, voice it, time it, mix it  -> build/bundle (job.json, page.html, mix.wav)
#   long.sh chunk <K> <N>        film frames of chunk K of N straight into ffmpeg -> build/bundle/seg_K_of_N.mp4 + .json
#   long.sh assemble <id>        join the chunks under the sound, chapters, QA     -> build/<id>.mp4 (+ chapters, description, qa)
set -e
TOP=$PWD; R=$TOP/reels; B=$TOP/build/bundle
mkdir -p $TOP/build $B
export PYTHONUNBUFFERED=1 RC_TTS_DIR=$TOP/models
# the full Chromium, not Playwright's headless shell: the shell honours --deterministic-mode and then waits for begin-frames
[ -n "$RC_CHROME" ] || RC_CHROME=$(ls -d $HOME/.cache/ms-playwright/chromium-*/chrome-linux*/chrome 2>/dev/null | head -1); export RC_CHROME
step=$1; shift
case $step in
  prep)
    id=$1; mod=$2
    echo "== compile $id ($mod) $(date +%T)"
    (cd $R/films && python3 films.py $mod 2>&1 | tail -5)
    [ -s $R/films/out/$id.html ] || { echo "COMPILE FAILED: no films/out/$id.html"; exit 1; }
    echo "== voice and time $(date +%T)"
    cd $R/free
    python3 longjob.py prep $id --bundle $B --eps $R/episodes/files.json --page $R/films/out/$id.html --tts-cache $TOP/build/tts-cache 2>&1 | grep -v -i warn | tail -20
    [ -s $B/job.json ] && [ -s $B/mix.wav ] || { echo "PREP FAILED"; exit 1; }
    ls -la $B
    echo "== prep done $(date +%T)" ;;
  chunk)
    k=$1; n=$2
    echo "chrome: $RC_CHROME"
    echo "== chunk $k of $n $(date +%T)"
    cd $R/free
    python3 longjob.py chunk $k $n --bundle $B 2>&1 | grep -v -i warn | tail -12
    [ -s $B/seg_${k}_of_${n}.mp4 ] || { echo "CHUNK FAILED"; exit 1; }
    echo "== chunk done $(date +%T)" ;;
  assemble)
    id=$1
    ls $B
    cd $R/free
    python3 longjob.py assemble --bundle $B --out $TOP/build/$id.mp4 2>&1 | tail -20
    [ -f $B/qa.json ] && cp $B/qa.json $TOP/build/$id.qa.json || echo '{}' > $TOP/build/$id.qa.json
    touch $TOP/build/$id.chapters.txt $TOP/build/$id.description.txt
    ls -la $TOP/build
    echo "== assembled $(date +%T)" ;;
  *) echo "usage: long.sh prep <id> <module> | chunk <K> <N> | assemble <id>"; exit 2 ;;
esac
