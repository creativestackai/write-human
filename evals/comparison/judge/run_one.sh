#!/bin/bash
# usage: run_one.sh <set: in|in2> <pid> <judge: codex|gemini>
cd SCRATCH
set_=$1; pid=$2; j=$3; out=judge/out/${set_}_${pid}.${j}.txt
[ -s "$out" ] && exit 0
if [ "$j" = codex ]; then
  timeout 500 codex exec -s read-only --skip-git-repo-check --ephemeral -o "$out" "$(cat judge/$set_/$pid.txt)" </dev/null >/dev/null 2>&1
else
  timeout 500 agy --model gemini-3.8-flash-high -p "$(cat judge/$set_/$pid.txt)" </dev/null > "$out" 2>/dev/null
fi
