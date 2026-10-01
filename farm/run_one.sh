#!/bin/bash
# run_one.sh <id>: one film, start to finish, on a GitHub runner: compile its File, voice it, render the frames in parallel
# chunks, encode 400-frame pieces, join them with the sound, check it. Output: build/<id>.mp4 and build/<id>.pack.tgz (mix + timeline).
set -e
id=$1; TOP=$PWD; R=$TOP/reels; W=$R/out/work/$id-v2; J=${JOBS:-4}
export RC_EPISODES=files.json RC_TTS_DIR=$TOP/models RC_HEAR=${RC_HEAR:-0} PYTHONUNBUFFERED=1
# the full Chromium, not Playwright's headless shell: the shell honours --deterministic-mode and then waits forever for begin-frames
[ -n "$RC_CHROME" ] || RC_CHROME=$(ls -d $HOME/.cache/ms-playwright/chromium-*/chrome-linux*/chrome 2>/dev/null | head -1); export RC_CHROME
echo "chrome: $RC_CHROME"
code=$(python3 -c "import json;print([e['code'] for e in json.load(open('$R/episodes/files.json')) if e['id']=='$id'][0])")
mod=${MOD:-f${code%%.*}}
echo "== $id ($mod) $(date +%T)"
(cd $R/films && python3 films.py $mod | grep " $id:" || true)
[ -s $R/films/out/$id.html ] || { echo "COMPILE FAILED: no films/out/$id.html"; (cd $R/films && python3 films.py $mod 2>&1 | tail -20); exit 1; }
cd $R/free
python3 reel.py $id --audio-only --out $R/out 2>&1 | grep -v -i warn | tail -14
n=$(python3 -c "import json;print(int(json.load(open('$W/timeline.json'))['total']*60))")
echo "== frames $n $(date +%T)"
per=$(( (n + J - 1) / J ))
for ((a=0; a<n; a+=per)); do b=$((a+per)); [ $b -gt $n ] && b=$n; python3 reel.py $id --chunk $a:$b --out $R/out > $TOP/build/c_$a.log 2>&1 & done; wait || true
for try in 1 2 3 4; do have=$(ls $W/frames 2>/dev/null | wc -l); [ "$have" -ge "$n" ] && break; echo "  refill ($have/$n)"; [ "$have" = 0 ] && tail -8 $TOP/build/c_0.log; python3 reel.py $id --chunk 0:$n --out $R/out > $TOP/build/fill_$try.log 2>&1 || true; done
have=$(ls $W/frames | wc -l); [ "$have" -ge "$n" ] || { echo "INCOMPLETE $have/$n"; exit 1; }
echo "== encode $(date +%T)"
P=400; k=0
for ((a=0; a<n; a+=P)); do b=$((a+P)); [ $b -gt $n ] && b=$n; python3 reel.py $id --encode-part $a:$b --out $R/out > /dev/null 2>&1 & k=$((k+1)); [ $((k % J)) = 0 ] && wait; done; wait
python3 reel.py $id --mux --out $R/out | tail -1
python3 qa.py $R/out/$id.mp4 $W/timeline.json | tail -3
cp $R/out/$id.mp4 $TOP/build/$id.mp4
tar czf $TOP/build/$id.pack.tgz -C $R/out/work $id-v2/mix.wav $id-v2/timeline.json
echo "== done $id $(date +%T)"
