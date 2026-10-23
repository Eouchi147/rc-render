#!/usr/bin/env bash
# Build the "sfx-bank" release: every BigSoundBank (CC0) row of dark/assets.csv plus sfx/bank_extra.txt, each checked
# CC0 on its own page, converted to 48 kHz stereo 24-bit FLAC, measured (EBU R128 integrated loudness, true peak), and
# published as one archive sfx-bank.tar (folder sfx-bank/<name>.flac) and sfx-bank.csv (name,source,licence,duration,...).
# The Dark Corners rows come from the "sfx" release, which holds those exact BigSoundBank files (fast and stable);
# the extras come from bigsoundbank.com directly (its own download form, else BWF, else MP3).
set -u
TAG=sfx-bank
W=/tmp/bank; RAW=$W/raw; OUT=$W/sfx-bank; mkdir -p "$RAW" "$OUT"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
is_audio() { [ -s "$1" ] && file -b "$1" | grep -qiE 'audio|wave|riff|mpeg|aiff|iff data'; }
echo "name,source,licence,duration_s,lufs_i,true_peak_dbtp,channels_in,rate_in,file" > "$W/sfx-bank.csv"
: > "$W/jobs.txt"
# 1. the Dark Corners bank rows (name.wav,source text with page url,file_url,licence)
grep -i 'bigsoundbank' dark/assets.csv | while IFS=, read -r f src url lic; do
  id=$(printf '%s' "$url" | grep -oE '[0-9]{4}' | tail -1); echo "${f%.wav} $id dark" >> "$W/jobs.txt"; done
# 2. the extras
grep -vE '^\s*(#|$)' sfx/bank_extra.txt | while read -r n s; do echo "$n ${s#bsb:} extra" >> "$W/jobs.txt"; done
echo "jobs: $(wc -l < "$W/jobs.txt")"
gh release download sfx -p '*.wav' -D "$RAW/dark" >/dev/null 2>&1 || mkdir -p "$RAW/dark"
nok=0; nfail=0
while read -r name id kind; do
  page="https://bigsoundbank.com/s$id.html"
  lic="CC0 (BigSoundBank / Joseph Sardin)"
  html=$(curl -sSL --retry 3 -A "$UA" -w '\n%{url_effective}' "$page" 2>/dev/null)
  purl=$(printf '%s' "$html" | tail -1)
  if ! printf '%s' "$html" | grep -q 'CC0'; then
    if [ "$kind" = dark ]; then lic="CC0 (BigSoundBank; page check failed this run, licence as recorded in dark/assets.csv)"
    else echo "SKIP $name ($id): CC0 not found on $purl"; nfail=$((nfail+1)); continue; fi
  fi
  src=""
  if [ "$kind" = dark ] && is_audio "$RAW/dark/$name.wav"; then src="$RAW/dark/$name.wav"
  else
    J=$W/jar; rm -f "$J" "$RAW/$name".*
    eff=$(curl -sSL --retry 3 -c "$J" -A "$UA" -o /dev/null -w '%{url_effective}' "https://bigsoundbank.com/UPLOAD/wav/$id.wav")
    curl -sSL --retry 3 -b "$J" -c "$J" -A "$UA" -e "$eff" -o "$RAW/$name.wav" --data "format=wav&id=$id&button=Download" https://bigsoundbank.com/download.php
    is_audio "$RAW/$name.wav" || curl -sSL --retry 3 -b "$J" -A "$UA" -e "$eff" -o "$RAW/$name.wav" "https://bigsoundbank.com/UPLOAD/bwf-en/$id.wav"
    if is_audio "$RAW/$name.wav"; then src="$RAW/$name.wav"
    else curl -sSL --retry 3 -A "$UA" -o "$RAW/$name.mp3" "https://bigsoundbank.com/UPLOAD/mp3/$id.mp3"; is_audio "$RAW/$name.mp3" && src="$RAW/$name.mp3"; fi
    sleep 1
  fi
  [ -z "$src" ] && { echo "FAIL $name ($id): no audio"; nfail=$((nfail+1)); continue; }
  ch=$(ffprobe -v error -select_streams a:0 -show_entries stream=channels -of csv=p=0 "$src"); sr=$(ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate -of csv=p=0 "$src")
  ffmpeg -nostdin -v error -y -i "$src" -map 0:a:0 -map_metadata -1 -ac 2 -ar 48000 -c:a flac -sample_fmt s32 -bits_per_raw_sample 24 "$OUT/$name.flac" || { echo "FAIL $name convert"; nfail=$((nfail+1)); continue; }
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/$name.flac")
  m=$(ffmpeg -nostdin -hide_banner -i "$OUT/$name.flac" -af ebur128=peak=true -f null - 2>&1 | tail -14)
  lu=$(printf '%s' "$m" | awk '/ I:/{print $2; exit}'); tp=$(printf '%s' "$m" | awk '/Peak:/{print $2; exit}')
  echo "$name,$purl,$lic,$(printf '%.2f' "$dur"),$lu,$tp,$ch,$sr,sfx-bank/$name.flac" >> "$W/sfx-bank.csv"
  echo "ok $name $id $kind ${dur}s ${lu} LUFS"; nok=$((nok+1))
done < "$W/jobs.txt"
echo "bank ok $nok, failed $nfail"
cd "$W" && tar cf sfx-bank.tar sfx-bank && ls -la sfx-bank.tar sfx-bank.csv
gh release view "$TAG" >/dev/null 2>&1 || gh release create "$TAG" --title "sfx-bank" --notes "BigSoundBank CC0 recordings as 48 kHz stereo 24-bit FLAC (Dark Corners bank + Cutaway series extras). Sources, licences, durations, loudness: sfx-bank.csv. Built by .github/workflows/sfx-bank.yml from sfx/bank.sh."
gh release upload "$TAG" sfx-bank.tar sfx-bank.csv --clobber
