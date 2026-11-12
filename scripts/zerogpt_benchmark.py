#!/usr/bin/env python3
"""ZeroGPT benchmark harness for write-human rewrites.

Measures draft vs rewrite through ZeroGPT's AI detector (zerogpt.com) so the
skill's effect on a real detector can be seen instead of assumed.

How detection actually works (verified 2026-11-12):
  * ZeroGPT's detect endpoint (POST https://api.zerogpt.com/api/detect/detectText,
    body {"input_text": "..."}) returns 403 "please make a purchase" to any
    direct/API call. There is no free programmatic tier.
  * The free web UI (15,000 chars per check) is the only free path, and it
    requires a real browser session. The response carries `data.fakePercentage`
    (0-100, higher = more AI), `data.isHuman`, `data.feedback` ("Your Text is
    AI/GPT Generated" / "Most Likely Human written..."), and `data.h` (the
    sentences highlighted as AI).

Two ways to use this harness:
  1. Free (browser). Collect results through a browser against the web UI (the
     exact routine is in evals/zerogpt/README.md), save them to a results JSON,
     then render the comparison with `--results`.
  2. Paid API. If you hold a ZeroGPT key, run with `--api-key`; confirm the
     Authorization header against ZeroGPT's API docs before trusting it (the
     free web UI itself sends no API key).

Usage:
  python3 scripts/zerogpt_benchmark.py --corpus evals/zerogpt/corpus.json --results evals/zerogpt/results.json
  python3 scripts/zerogpt_benchmark.py --corpus corpus.json --api-key YOUR_KEY [--csv out.csv]
  python3 scripts/zerogpt_benchmark.py --howto

Standard library only. Not an AI detector itself: it reports what ZeroGPT
reported, nothing more.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

DETECT_URL = "https://api.zerogpt.com/api/detect/detectText"


def load_json(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def detect_api(text: str, api_key: str) -> dict:
    """Paid API path. Confirm the auth header against ZeroGPT's API docs."""
    body = json.dumps({"input_text": text}).encode()
    req = urllib.request.Request(
        DETECT_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read())
    except urllib.error.HTTPError as err:
        return {"error": f"HTTP {err.code}: {err.reason}", "detail": err.read().decode()[:200]}
    d = payload.get("data") or {}
    return {
        "words": d.get("textWords"),
        "fake_pct": d.get("fakePercentage"),
        "isHuman": d.get("isHuman"),
        "feedback": d.get("feedback"),
        "note": d.get("additional_feedback"),
    }


def render(results: dict, csv_path: str | None = None) -> None:
    pairs = results.get("pairs", [])
    print("ZeroGPT benchmark (zerogpt.com) -- AI % by text.")
    print("One probabilistic detector; short text is over-flagged. Not a verdict.\n")
    print(f"{'pair':<6} {'draft%':>8} {'rewrite%':>9} {'delta':>7}  verdict (rewrite)")
    print("-" * 78)
    for p in pairs:
        d = p.get("draft", {})
        r = p.get("rewrite", {})
        dd, rr = d.get("fake_pct"), r.get("fake_pct")
        delta = ""
        if isinstance(dd, (int, float)) and isinstance(rr, (int, float)):
            delta = f"{rr - dd:+.1f}"
        note = f"  [{r.get('note')}]" if r.get("note") else ""
        print(f"{p.get('id', '?'):<6} {dd!s:>8} {rr!s:>9} {delta:>7}  {r.get('feedback', '')}{note}")

    if csv_path:
        with open(csv_path, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["pair", "draft_fake_pct", "rewrite_fake_pct", "rewrite_feedback", "draft_words", "rewrite_words"])
            for p in pairs:
                d, r = p.get("draft", {}), p.get("rewrite", {})
                w.writerow([p.get("id"), d.get("fake_pct"), r.get("fake_pct"),
                            r.get("feedback"), d.get("words"), r.get("words")])
        print(f"\nWrote {csv_path}")


HOWTO = r"""Free-tier collection (browser, no API key).

ZeroGPT has no free API. Collect through a real browser against zerogpt.com.
The routine below is the one this harness's sample results were produced with;
it runs inside an agent that can drive a browser. It posts to the same
endpoint the web UI uses, so the session cookies satisfy ZeroGPT's paywall.

  1. Open https://www.zerogpt.com/ and locate the textarea named "textArea"
     and the "Detect Text" button.
  2. For each text (draft, then rewrite), set the textarea, click Detect Text,
     wait ~9s, and read the XHR response to /api/detect/detectText.
  3. From the response JSON, record data.fakePercentage, data.isHuman,
     data.feedback, data.textWords, data.additional_feedback, data.h.
  4. Save as results JSON in the schema this script renders (see
     evals/zerogpt/results.json), then run --results.

Limits: 15,000 chars per check on the free UI; unauthenticated checks are
rate-limited; results are per-request and may vary run to run.
"""


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="ZeroGPT benchmark for write-human rewrites.")
    parser.add_argument("--corpus", help="JSON corpus: [{id, draft, rewrite}, ...]")
    parser.add_argument("--results", help="JSON of collected results, to render")
    parser.add_argument("--api-key", help="paid ZeroGPT API key (optional)")
    parser.add_argument("--csv", help="write a CSV of the comparison")
    parser.add_argument("--howto", action="store_true", help="print the free browser-collection routine")
    args = parser.parse_args(argv)

    if args.howto:
        print(HOWTO)
        return 0

    if args.results:
        render(load_json(args.results), args.csv)
        return 0

    if args.corpus and args.api_key:
        corpus = load_json(args.corpus)
        pairs = []
        for item in corpus:
            draft = detect_api(item["draft"], args.api_key)
            rewrite = detect_api(item["rewrite"], args.api_key)
            pairs.append({"id": item.get("id"), "draft": draft, "rewrite": rewrite})
            print(json.dumps({"id": item.get("id"), "draft": draft, "rewrite": rewrite}))
        results = {
            "detector": "ZeroGPT",
            "url": "https://www.zerogpt.com/",
            "collected_via": "paid API",
            "pairs": pairs,
        }
        render(results, args.csv)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
