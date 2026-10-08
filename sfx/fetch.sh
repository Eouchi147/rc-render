#!/usr/bin/env bash
# Fetch the sounds listed in $1 ("name source" per line) and publish them to the "sfx" release.
# source forms:
#   bsb:<id>     BigSoundBank (CC0): the WAV from the site's own download form (else its BWF, else MP3), checked to be audio
#   git:<repo>|<pattern>|...   sparse clone (no-cone patterns, %20 = space), packed as <name>.tgz
#   tree:<repo>  the repository's file list (no file contents), as <name>.txt
#   http(s)://   direct file (name used as given)
set -u
LIST=$1
TAG=sfx
OUT=$(pwd)/out
mkdir -p "$OUT"
gh release view "$TAG" >/dev/null 2>&1 || gh release create "$TAG" --title "sfx" --notes "Sound sources for the films. Sources and licences: sources.csv."
gh release download "$TAG" -p sources.csv -D /tmp 2>/dev/null || echo "name,source,file_url,licence" > /tmp/sources.csv
: > /tmp/new.csv
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
is_audio() { [ -s "$1" ] && file -b "$1" | grep -qiE 'audio|wave|riff|mpeg|aiff|iff data'; }
J=/tmp/jar.txt
nok=0; nfail=0
while read -r name src; do
  [ -z "${name:-}" ] && continue
  case "$name" in \#*) continue;; esac
  case "$src" in
    bsb:*)
      id=${src#bsb:}
      rm -f "$J" "$OUT/$name.wav" "$OUT/$name.mp3"
      page=$(curl -sSL --retry 3 -c "$J" -A "$UA" -o /tmp/page.html -w '%{url_effective}' "https://bigsoundbank.com/UPLOAD/wav/$id.wav")
      sleep 1
      curl -sSL --retry 3 -b "$J" -c "$J" -A "$UA" -e "$page" -o "$OUT/$name.wav" \
           --data "format=wav&id=$id&button=Download" "https://bigsoundbank.com/download.php"
      url="https://bigsoundbank.com/download.php (wav, id $id)"; ext=wav
      if ! is_audio "$OUT/$name.wav"; then
        curl -sSL --retry 3 -b "$J" -A "$UA" -e "$page" -o "$OUT/$name.wav" "https://bigsoundbank.com/UPLOAD/bwf-en/$id.wav"
        url="https://bigsoundbank.com/UPLOAD/bwf-en/$id.wav"
      fi
      if ! is_audio "$OUT/$name.wav"; then
        rm -f "$OUT/$name.wav"; ext=mp3
        curl -sSL --retry 3 -b "$J" -A "$UA" -e "$page" -o "$OUT/$name.mp3" "https://bigsoundbank.com/UPLOAD/mp3/$id.mp3"
        url="https://bigsoundbank.com/UPLOAD/mp3/$id.mp3"
        if ! is_audio "$OUT/$name.mp3"; then echo "FAIL $name ($id): $(file -b "$OUT/$name.mp3" | cut -c1-60)"; rm -f "$OUT/$name.mp3"; nfail=$((nfail+1)); continue; fi
        gh release delete-asset "$TAG" "$name.wav" -y >/dev/null 2>&1 || true
      fi
      echo "ok $name.$ext $(file -b "$OUT/$name.$ext" | cut -c1-70)"; nok=$((nok+1))
      echo "$name.$ext,bigsoundbank.com sound $id ($page),$url,CC0 (BigSoundBank / Joseph Sardin)" >> /tmp/new.csv
      sleep 1 ;;
    git:*)
      spec=${src#git:}
      IFS='|' read -ra parts <<< "$spec"
      repo=${parts[0]}
      rm -rf /tmp/g
      git clone -q --depth 1 --filter=blob:none --no-checkout "$repo" /tmp/g || { echo "FAIL clone $name"; continue; }
      pats=()
      for p in "${parts[@]:1}"; do pats+=("${p//%20/ }"); done
      ( cd /tmp/g && git sparse-checkout set --no-cone "${pats[@]}" && git checkout -q ) || { echo "FAIL sparse $name"; continue; }
      ( cd /tmp/g && find . -type f ! -path './.git/*' | sed 's|^\./||' > /tmp/files.txt && wc -l < /tmp/files.txt && tar czf "$OUT/$name.tgz" -T /tmp/files.txt ) || { echo "FAIL tar $name"; continue; }
      echo "$name.tgz,$repo,${parts[*]:1},see repository licence" >> /tmp/new.csv ;;
    tree:*)
      repo=${src#tree:}
      rm -rf /tmp/t
      git clone -q --depth 1 --filter=blob:none --no-checkout "$repo" /tmp/t && git -C /tmp/t ls-tree -r --name-only HEAD > "$OUT/$name.txt" \
        && echo "tree $name $(wc -l < "$OUT/$name.txt")" || { echo "FAIL tree $name"; continue; }
      echo "$name.txt,$repo,file list,see repository licence" >> /tmp/new.csv ;;
    http*)
      curl -fsSL --retry 3 -A "$UA" -o "$OUT/$name" "$src" || { echo "FAIL $name"; rm -f "$OUT/$name"; continue; }
      echo "$name,$src,$src,see source" >> /tmp/new.csv ;;
  esac
done < "$LIST"
echo "bsb ok $nok, failed $nfail"
# sources.csv: this run's entries, then the earlier ones not fetched again
cut -d, -f1 /tmp/new.csv | sed 's/\.[a-z0-9]*$//' | sort -u > /tmp/newnames.txt
{ echo "name,source,file_url,licence"; cat /tmp/new.csv
  tail -n +2 /tmp/sources.csv | while IFS= read -r l; do b=$(printf '%s' "${l%%,*}" | sed 's/\.[a-z0-9]*$//'); grep -qxF "$b" /tmp/newnames.txt || printf '%s\n' "$l"; done; } > "$OUT/sources.csv"
ls -la "$OUT" | head -200
cd "$OUT" && gh release upload "$TAG" * --clobber
