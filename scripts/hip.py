#!/usr/bin/env python3
"""
Humanization by Iterative Paraphrasing (HIP) pass.

Regenerate text through a locally-served BASE model (non-instruction-tuned) to
strip the instruction-tuning / RLHF fingerprints that AI detectors track. Base
models lack those artifacts, so their output reads as human to detectors where
an instruction-tuned rewrite does not.

Requires a base model served by Ollama (setup in reference/hip.md). No Python
dependencies — standard library only.

Usage:
  python3 hip.py input.txt > output.txt
  python3 hip.py input.txt --passes 3 --model qwen3-8b-base
  cat input.txt | python3 hip.py -

Flags:
  --model     Ollama model name        (default: qwen3-8b-base)
  --chunk     words per chunk          (default: 200)
  --passes    paraphrase passes        (default: 2)
  --temp      sampling temperature     (default: 0.9)
  --top-p     nucleus sampling         (default: 0.95)
  --host      Ollama host              (default: http://localhost:11434)

Faithfulness caveat: a base model is a paraphraser, not a faithful editor. It
can drift a fact or drop a detail. Treat this as the FIRST stage of the
write-human pipeline: run hip.py to shed the machine fingerprints, then run the
voice / self-audit pass from SKILL.md (or ask for missing specifics) to restore
any lost detail. This is the documented tradeoff of the HIP lever.
"""

import argparse
import json
import re
import sys
import urllib.request


def sentence_split(text):
    """Split into sentences on terminal punctuation followed by a capital."""
    parts = re.split(r"(?<=[.!?])\s+(?=[\'\"]?[A-Z0-9])", text.strip())
    return [p.strip() for p in parts if p.strip()]


def chunk_text(text, words=200):
    """Pack sentences into ~N-word chunks on sentence boundaries."""
    sentences = sentence_split(text)
    chunks, cur, cur_wc = [], [], 0
    for s in sentences:
        wc = len(s.split())
        if cur and cur_wc + wc > words:
            chunks.append(" ".join(cur))
            cur, cur_wc = [], 0
        cur.append(s)
        cur_wc += wc
    if cur:
        chunks.append(" ".join(cur))
    return chunks


def build_prompt(text):
    return (
        "Rewrite the following text in your own words. Keep every fact, name, "
        "number, and the exact meaning, but phrase it the way a person would in "
        "casual, natural writing.\n\n"
        "Text: {text}\n\n"
        "Rewritten:".format(text=text)
    )


def paraphrase(text, model, temp, top_p, host, timeout=300):
    payload = {
        "model": model,
        "prompt": build_prompt(text),
        "raw": True,          # send the prompt verbatim, no chat template
        "stream": False,
        "options": {
            "temperature": temp,
            "top_p": top_p,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "num_predict": 1024,
        },
    }
    req = urllib.request.Request(
        host.rstrip("/") + "/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data.get("response", "").strip()


def clean(text):
    """Drop the label the base model may echo back, and a trailing fragment."""
    text = re.sub(
        r"^(Rewritten|Paraphrase|Here is|Here's|Output)\s*[:\-]\s*",
        "", text, flags=re.IGNORECASE,
    ).strip()
    return text


def main():
    ap = argparse.ArgumentParser(description="HIP base-model paraphrase pass")
    ap.add_argument("input", help="input file, or '-' for stdin")
    ap.add_argument("--model", default="qwen3-8b-base")
    ap.add_argument("--chunk", type=int, default=200)
    ap.add_argument("--passes", type=int, default=2)
    ap.add_argument("--temp", type=float, default=0.9)
    ap.add_argument("--top-p", type=float, default=0.95)
    ap.add_argument("--host", default="http://localhost:11434")
    args = ap.parse_args()

    if args.input == "-":
        text = sys.stdin.read()
    else:
        with open(args.input, encoding="utf-8") as f:
            text = f.read()

    for p in range(args.passes):
        chunks = chunk_text(text, args.chunk)
        out = []
        for i, c in enumerate(chunks):
            r = paraphrase(c, args.model, args.temp, args.top_p, args.host)
            out.append(clean(r))
            sys.stderr.write(
                "  pass {}/{} chunk {}/{} ({}w -> {}w)\n".format(
                    p + 1, args.passes, i + 1, len(chunks),
                    len(c.split()), len(r.split()),
                )
            )
            sys.stderr.flush()
        text = "\n\n".join(out)

    sys.stdout.write(text + "\n")


if __name__ == "__main__":
    main()
