#!/usr/bin/env bash
# Download check stills from release "stills" by tag prefix (REST only; gh release download needs GraphQL, blocked here).
# usage: bash tools/getstills.sh <tag> <dir>
set -e; T="$1"; D="${2:-.}"; mkdir -p "$D"
gh api repos/Eouchi147/rc-render/releases/tags/stills --jq ".assets[]|select(.name|startswith(\"$T-\"))|\"\(.id) \(.name)\"" |
while read -r id n; do gh api -H 'Accept: application/octet-stream' "repos/Eouchi147/rc-render/releases/assets/$id" > "$D/$n"; echo "$D/$n"; done
