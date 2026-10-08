#!/bin/bash
# darkengine setup: puts Python 3.12 and the packages in .venv (inside this folder), then fetches the
# sounds, textures and instrument samples the films use (about 2.5 GB) into sfx/ tex/ vsco/ samples/.
# Safe to run again: anything already done is skipped, so after a break just run it again.
# Works with the bash that comes with macOS (3.2) and on Linux.
#   LOCAL_ASSETS=/some/folder bash setup.sh   copies the assets from that folder instead of downloading.

cd "$(dirname "$0")" || exit 1
HERE="$(pwd)"
URL="https://github.com/Eouchi147/rc-render/releases/download/sfx"
LOCAL_ASSETS="${LOCAL_ASSETS:-}"

say()  { printf '%s\n' "$*"; }
stop() { printf '\nSetup stopped: %s\n' "$*" >&2; exit 1; }
again="Check the internet connection, then run setup again (it carries on where it stopped)."

say "darkengine setup"
say "  folder: $HERE"
rm -f "$HERE/.setup-done"

# The packages are built for macOS 13 (Ventura) or newer.
if [ "$(uname)" = Darwin ]; then
  v="$(sw_vers -productVersion 2>/dev/null)"
  major="${v%%.*}"
  if [ -n "$major" ] && [ "$major" -lt 13 ] 2>/dev/null; then
    stop "this needs macOS 13 (Ventura) or newer, and this Mac has macOS $v."
  fi
fi

# ---------------------------------------------------------------- 1. uv (it installs Python for us)
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
if ! command -v uv >/dev/null 2>&1; then
  say "- Installing uv, a small tool that installs Python..."
  curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null
  [ -f "$HOME/.local/bin/env" ] && . "$HOME/.local/bin/env"
  hash -r 2>/dev/null
  command -v uv >/dev/null 2>&1 || stop "uv could not be installed. $again"
fi

# ---------------------------------------------------------------- 2. Python and packages in .venv
if [ ! -x "$HERE/.venv/bin/python" ]; then
  say "- Setting up Python 3.12 in .venv ..."
  rm -rf "$HERE/.venv"
  uv venv -q --python 3.12 "$HERE/.venv" || stop "Python 3.12 could not be set up. $again"
fi
say "- Installing the Python packages (a few minutes the first time)..."
uv pip install -q --python "$HERE/.venv/bin/python" -r "$HERE/requirements.txt" \
  || stop "the Python packages did not install. $again"
"$HERE/.venv/bin/python" -c "import numpy, scipy, cv2, numba, PIL, skimage, HersheyFonts, soundfile, pedalboard, pyloudnorm, imageio_ffmpeg; imageio_ffmpeg.get_ffmpeg_exe()" \
  || stop "the Python packages are installed but do not load. Delete the .venv folder and run setup again."
say "  Python is ready."

# ---------------------------------------------------------------- 3. sounds, textures, samples
mkdir -p "$HERE/sfx" "$HERE/tex" "$HERE/vsco" "$HERE/samples" "$HERE/models" "$HERE/out"
total=$(cut -d, -f1 "$HERE/assets.csv" | tr -d '\r' | grep -c -E '\.(wav|jpg|tgz)$')
i=0; have=0; got=0; failed=0

if [ -n "$LOCAL_ASSETS" ]; then
  say "- Copying $total assets from $LOCAL_ASSETS ..."
else
  free_kb=$(df -Pk "$HERE" | awk 'NR==2 {print $4}')
  if [ ! -f "$HERE/vsco/.vsco_perc.tgz.unpacked" ] && [ -n "$free_kb" ] && [ "$free_kb" -lt 5000000 ] 2>/dev/null; then
    say "  Note: this disk has only about $((free_kb / 1000000)) GB free; the assets need about 5 GB."
  fi
  say "- Downloading $total assets (about 2.5 GB, the slow part; files you already have are skipped)..."
fi

local_file() {  # prints where a copy of $1 sits under LOCAL_ASSETS, if anywhere
  local dir
  for dir in "$LOCAL_ASSETS" "$LOCAL_ASSETS/sfx" "$LOCAL_ASSETS/tex" "$LOCAL_ASSETS/sfx_rel"; do
    if [ -f "$dir/$1" ]; then printf '%s\n' "$dir/$1"; return 0; fi
  done
  return 1
}

fetch() {  # fetch NAME TARGET: download (or copy) one asset to TARGET
  local src
  if [ -n "$LOCAL_ASSETS" ]; then
    src="$(local_file "$1")" || return 1
    cp "$src" "$2"
  elif [ -t 1 ] && [ "${1##*.}" = tgz ]; then
    curl -fL --retry 3 --retry-delay 3 --connect-timeout 30 -# -o "$2" "$URL/$1"
  else
    curl -fL --retry 3 --retry-delay 3 --connect-timeout 30 -sS -o "$2" "$URL/$1"
  fi
}

get_file() {  # get_file NAME FOLDER
  local dest
  dest="$HERE/$2/$1"
  if [ -s "$dest" ]; then have=$((have + 1)); return 0; fi
  say "  [$i/$total] $1"
  if fetch "$1" "$dest.part"; then
    mv -f "$dest.part" "$dest"; got=$((got + 1))
  else
    rm -f "$dest.part"; failed=$((failed + 1)); say "    (could not get $1)"
  fi
}

get_archive() {  # get_archive NAME: fetch a sample archive, unpack it, delete it
  local d mark tgz
  case "$1" in vsco_strings.tgz|vsco_perc.tgz) d=vsco ;; *) d=samples ;; esac
  mark="$HERE/$d/.$1.unpacked"
  if [ -f "$mark" ]; then have=$((have + 1)); return 0; fi
  if [ -n "$LOCAL_ASSETS" ] && ! local_file "$1" >/dev/null && [ -d "$LOCAL_ASSETS/$d" ]; then
    # local test copy: this archive is only there already unpacked, so copy that folder (once)
    if [ ! -f "$HERE/$d/.local-copy" ]; then
      say "  [$i/$total] $1: copying the unpacked $d/ folder"
      if cp -R "$LOCAL_ASSETS/$d/." "$HERE/$d/"; then touch "$HERE/$d/.local-copy"
      else failed=$((failed + 1)); say "    (could not copy $LOCAL_ASSETS/$d)"; return 1; fi
    fi
    touch "$mark"; got=$((got + 1)); return 0
  fi
  tgz="$HERE/$d/$1"
  if [ ! -s "$tgz" ]; then
    say "  [$i/$total] $1 (a large sample archive)"
    if ! fetch "$1" "$tgz.part"; then
      rm -f "$tgz.part"; failed=$((failed + 1)); say "    (could not get $1)"; return 1
    fi
    mv -f "$tgz.part" "$tgz"
  fi
  say "    unpacking $1 into $d/"
  if tar -xzf "$tgz" -C "$HERE/$d"; then
    rm -f "$tgz"; touch "$mark"; got=$((got + 1))
  else
    rm -f "$tgz"; failed=$((failed + 1)); say "    ($1 was damaged; it is fetched again next time)"
  fi
}

while IFS=, read -r name rest <&3 || [ -n "$name" ]; do
  name="$(printf '%s' "$name" | tr -d '\r')"
  case "$name" in
    *.tgz)     i=$((i + 1)); get_archive "$name" ;;
    tex_*.jpg) i=$((i + 1)); get_file "$name" tex ;;
    *.wav)     i=$((i + 1)); get_file "$name" sfx ;;
  esac
done 3< "$HERE/assets.csv"

say "  assets: $got fetched now, $have already here, $failed missing."
if [ "$failed" -gt 0 ]; then
  stop "$failed asset(s) could not be fetched. $again"
fi
touch "$HERE/.setup-done"
say ""
say "Setup finished. To render the test clip, run:"
say "  bash \"$HERE/render.sh\" test"
