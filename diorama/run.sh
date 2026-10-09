#!/bin/bash
# bash diorama/run.sh SCENE LOOK  -> out/SCENE_LOOK.png (Blender 4.2 LTS, CPU)
set -u; S=$1; L=$2; mkdir -p out
exec > >(tee out/${S}_${L}.log) 2>&1
pip install -q numpy opencv-python-headless
python3 diorama/export.py $S out/
if [ ! -x blender/blender ]; then
  curl -fsSL https://download.blender.org/release/Blender4.2/blender-4.2.3-linux-x64.tar.xz | tar xJ && mv blender-4.2.3-linux-x64 blender
fi
time blender/blender -b -P diorama/blend.py -- out/$S.json out/${S}_sky.png $L $(pwd)/out/${S}_${L}.png 2>&1 | grep -v "^Fra:" | tail -40
ls -la out
