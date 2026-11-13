# ZeroGPT benchmark

Real-detector evidence for `write-human`: runs drafts and rewrites through
ZeroGPT (zerogpt.com) and reports the AI percentage each gets. The skill's
own comparison rounds used LLM judges and explicitly never ran a real
detector; this closes part of that gap for one detector.

## What is actually measured

ZeroGPT's free web UI returns, per check:

- `fakePercentage` — 0-100, higher = more AI. The number it shows users.
- `isHuman` — ZeroGPT's internal flag (0 = AI, higher = leaning human).
- `feedback` — the human-readable verdict ("Your Text is AI/GPT Generated"
  / "Your Text is Most Likely Human written...").
- `h` — the sentences it highlights as AI.

## Finding so far (2026-11-12)

| pair | draft % | rewrite % | verdict |
| --- | --- | --- | --- |
| P01 | 100.0 | 100.0 | still AI |
| P04 | 100.0 | 53.9 | "Most Likely Human written" (short-text caveat) |
| P05 | 100.0 | 100.0 | still AI |

The honest read: ZeroGPT is a perplexity-style detector that flags clean,
well-written text as AI. The only rewrite it let through was the shortest and
most stripped (39 words), and even that came with ZeroGPT's "input more text"
warning. This is evidence *for* the skill's honesty section, not a win: no
style rewrite reliably moves a detector this brittle, and short texts are
over-flagged in both directions. The drafts and rewrites are in `corpus.json`.

## Cross-check against the voice recipe (2026-11-12)

Five first-person "confessional voice" variants that Clever scored 1-15% AI
(98-99% human) all returned a flat **100%** on ZeroGPT, as did the AI control.
ZeroGPT's free detector now stamps essentially everything as AI and cannot
distinguish human-voiced prose from machine text. It is overzealous to the
point of uselessness as a benchmark — do not optimize against it. Clever's
probability + sentence-signal output is the meaningful instrument.

## Why a browser, not a script

ZeroGPT has no free API. A direct POST to its detect endpoint returns
`403 "please make a purchase"`. The free web UI works only inside a browser
session (its cookies satisfy the paywall). So collection is browser-driven,
and `scripts/zerogpt_benchmark.py` is the renderer/aggregator for whatever the
browser collects, plus an optional `--api-key` path for paid API users.

## Collect (free, browser)

In an agent that can drive a browser:

1. Open `https://www.zerogpt.com/`.
2. Locate the textarea (`name="textArea"`) and the "Detect Text" button.
3. For each text (draft, then rewrite): set the textarea value, dispatch an
   `input` event, click "Detect Text", wait ~9s.
4. Read the XHR response to `POST https://api.zerogpt.com/api/detect/detectText`
   (body `{"input_text": "..."}`) and record `data.fakePercentage`,
   `data.isHuman`, `data.feedback`, `data.textWords`,
   `data.additional_feedback`, `data.h`.
5. Save as JSON in the schema of `results.json`, then render.

## Render

```bash
python3 scripts/zerogpt_benchmark.py --results evals/zerogpt/results.json [--csv out.csv]
```

## Caveats

- One detector, not a verdict. The skill's position stands: detectors disagree
  with each other and with themselves.
- Short text (under ~50 words) is over-flagged; ZeroGPT says so itself.
- Unauthenticated checks are rate-limited; scores vary run to run.
- The paid API path (`--api-key`) is untested here — confirm the
  Authorization header against ZeroGPT's API docs before relying on it.
