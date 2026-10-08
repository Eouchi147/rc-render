#!/usr/bin/env bash
# Fetch the sounds listed in $1 ("name source" per line) and publish them to the "sfx" release.
# source forms:
#   bsb:<id>    BigSoundBank (CC0): WAV if available, else MP3
#   fs:<url>    Freesound sound page: HQ preview, licence recorded
#   git:<repo>|<pattern>|...   sparse clone (no-cone patterns, %20 = space), packed as <name>.tgz
#   http(s)://  direct file (name used as given)
set -u
LIST=$1
TAG=sfx
OUT=$(pwd)/out
mkdir -p "$OUT"
gh release view "$TAG" >/dev/null 2>&1 || gh release create "$TAG" --title "sfx" --notes "Sound sources for the films. Sources and licences: sources.csv."
gh release download "$TAG" -p sources.csv -D "$OUT" 2>/dev/null || echo "name,source,file_url,licence" > "$OUT/sources.csv"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
while read -r name src; do
  [ -z "${name:-}" ] && continue
  case "$name" in \#*) continue;; esac
  case "$src" in
    bsb:*)
      id=${src#bsb:}
      url="https://bigsoundbank.com/UPLOAD/wav/$id.wav"; ext=wav
      if ! curl -fsSL --retry 3 -A "$UA" -o "$OUT/$name.$ext" "$url"; then
        rm -f "$OUT/$name.$ext"
        url="https://bigsoundbank.com/UPLOAD/mp3/$id.mp3"; ext=mp3
        curl -fsSL --retry 3 -A "$UA" -o "$OUT/$name.$ext" "$url" || { echo "FAIL $name"; rm -f "$OUT/$name.$ext"; continue; }
      fi
      echo "$name.$ext,bigsoundbank.com sound $id,$url,CC0 (BigSoundBank / Joseph Sardin)" >> "$OUT/sources.csv" ;;
    fs:*)
      page=${src#fs:}
      html=$(curl -fsSL --retry 3 -A "$UA" "$page") || { echo "FAIL page $name"; continue; }
      prev=$(printf '%s' "$html" | grep -o 'https://cdn.freesound.org/previews/[^"]*-hq.mp3' | head -1)
      lic=$(printf '%s' "$html" | grep -o 'creativecommons.org/[a-z/0-9.]*' | head -1)
      [ -z "$prev" ] && { echo "FAIL nopreview $name"; continue; }
      curl -fsSL --retry 3 -A "$UA" -o "$OUT/$name.mp3" "$prev" || { echo "FAIL $name"; continue; }
      echo "$name.mp3,$page,$prev,$lic" >> "$OUT/sources.csv" ;;
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
      echo "$name.tgz,$repo,${parts[*]:1},see repository licence" >> "$OUT/sources.csv" ;;
    http*)
      curl -fsSL --retry 3 -A "$UA" -o "$OUT/$name" "$src" || { echo "FAIL $name"; rm -f "$OUT/$name"; continue; }
      echo "$name,$src,$src,see source" >> "$OUT/sources.csv" ;;
  esac
done < "$LIST"
ls -la "$OUT"
cd "$OUT" && gh release upload "$TAG" * --clobber
