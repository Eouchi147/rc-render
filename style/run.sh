#!/bin/bash
# Renders one style of the style test with FLUX.1-schnell (Apache-2.0) on CPU via stable-diffusion.cpp.
#   bash style/run.sh <style-key>      -> out/<style-key>.png and out/<style-key>.log
set -u
KEY=$1
mkdir -p out m
exec > >(tee out/$KEY.log) 2>&1
J=style/prompts.json
py() { python3 -c "import json;d=json.load(open('$J'));print($1)"; }
W=$(py "d['w']"); H=$(py "d['h']"); STEPS=$(py "d['steps']"); SEED=$(py "d['seed']")
PROMPT="$(py "d['scene']+', '+d['styles']['$KEY']")"
nproc; free -g | head -2
# build stable-diffusion.cpp (CPU)
if [ ! -x sdcpp/build/bin/sd ] && [ ! -x sdcpp/build/bin/sd-cli ]; then
  git clone --depth 1 --recursive https://github.com/leejet/stable-diffusion.cpp sdcpp && \
  cmake -S sdcpp -B sdcpp/build -DCMAKE_BUILD_TYPE=Release -DGGML_NATIVE=ON >/dev/null && \
  cmake --build sdcpp/build --config Release -j $(nproc) 2>&1 | tail -3
fi
SD=$(ls sdcpp/build/bin/sd sdcpp/build/bin/sd-cli 2>/dev/null | head -1); echo "binary: $SD"
get() {  # get <out> <url1> [url2 ...]
  local o=$1; shift
  for u in "$@"; do
    [ -s "m/$o" ] && return 0
    echo "fetch $o <- $u"; curl -fL --retry 3 -s -o "m/$o" "$u" || rm -f "m/$o"
  done
  ls -la "m/$o"
}
HF=https://huggingface.co
get flux.gguf  $HF/city96/FLUX.1-schnell-gguf/resolve/main/flux1-schnell-Q4_K_S.gguf $HF/second-state/FLUX.1-schnell-GGUF/resolve/main/flux1-schnell-Q4_0.gguf
get t5.gguf    $HF/city96/t5-v1_1-xxl-encoder-gguf/resolve/main/t5-v1_1-xxl-encoder-Q4_K_M.gguf $HF/second-state/FLUX.1-schnell-GGUF/resolve/main/t5xxl-Q4_0.gguf
get clip_l.safetensors $HF/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors $HF/second-state/FLUX.1-schnell-GGUF/resolve/main/clip_l.safetensors
get ae.safetensors $HF/second-state/FLUX.1-schnell-GGUF/resolve/main/ae.safetensors $HF/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors
echo "prompt: $PROMPT"
time $SD --diffusion-model m/flux.gguf --vae m/ae.safetensors --clip_l m/clip_l.safetensors --t5xxl m/t5.gguf \
   -p "$PROMPT" --cfg-scale 1.0 --sampling-method euler --steps $STEPS -W $W -H $H -s $SEED -t $(nproc) -o out/$KEY.png
ls -la out
