#!/bin/bash
cd "$(dirname "$0")"
o=$1; pid=$2; j=$3; mkdir -p judgeS/out; out=judgeS/out/${o}_${pid}.${j}.txt
[ -s "$out" ] && python3 -I -c "import json;t=open('$out').read();json.loads(t[t.find('{'):t.rfind('}')+1])" 2>/dev/null && exit 0
if [ "$j" = codex ]; then
  timeout 500 codex exec -s read-only --skip-git-repo-check --ephemeral -o "$out" "$(cat judgeS/in/$o/$pid.txt)" </dev/null >/dev/null 2>&1
else
  timeout 500 agy --model gemini-3.8-flash-high -p "$(cat judgeS/in/$o/$pid.txt)" </dev/null > "$out" 2>/dev/null
fi
