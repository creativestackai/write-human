#!/bin/bash
# usage: run_one.sh <tag> <order> <pid> <judge>
cd SCRATCH
tag=$1; o=$2; pid=$3; j=$4; mkdir -p judge4/$tag/out; out=judge4/$tag/out/${o}_${pid}.${j}.txt
[ -s "$out" ] && python3 -I -c "import json,sys;t=open('$out').read();json.loads(t[t.find('{'):t.rfind('}')+1])" 2>/dev/null && exit 0
if [ "$j" = codex ]; then
  timeout 500 codex exec -s read-only --skip-git-repo-check --ephemeral -o "$out" "$(cat judge4/$tag/$o/$pid.txt)" </dev/null >/dev/null 2>&1
else
  timeout 500 agy --model gemini-3.8-flash-high -p "$(cat judge4/$tag/$o/$pid.txt)" </dev/null > "$out" 2>/dev/null
fi
