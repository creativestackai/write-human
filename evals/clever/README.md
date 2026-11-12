# Clever AI Detector benchmark

Second real-detector benchmark for `write-human`, cross-checking ZeroGPT against
Clever AI Detector (cleverhumanizer.ai/ai-detector). Clever reports a
probability (0-100), a verdict, and per-sentence signals — a better instrument
than ZeroGPT's blanket score.

## How it works (verified 2026-11-12)

Async job API, free and no auth, but **browser-only** (a direct `fetch` from an
injected script is blocked; the page's own calls work):

1. `POST https://cleverhumanizer.ai/ai-detector/jobs`
   body `{"text": "...", "type_generation": "detector"}` → returns `job_id`.
2. `GET https://cleverhumanizer.ai/ai-detector/jobs/{job_id}` → poll until
   `status == "completed"`, then read `result`.

`result` schema: `ai_score` (0-100), `human_probability_percent`, `verdict`
(`ai` / `human` / `mixed`), `word_count`, `sentence_count`,
`explanation.signals[]` (the reasons), and `sentence_details[]` (per-sentence
`ai_score`, `verdict`, `color`, `reasons`).

**80-word minimum.** Checks under 80 words are silently not scored (the button
stays "Check for AI" and no job is created). The write-human rewrites in this
corpus compress below that, which is itself a finding (see below).

## Results (2026-11-12)

| pair | draft | rewrite | read |
| --- | --- | --- | --- |
| P01 | 99 | 95 (human 5%) | marginal drop |
| P04 | 95 | not scored (39 words) | under minimum |
| P05 | 95 | not scored (77 words) | under minimum |

## What it tells us

1. **Clever is more honest than ZeroGPT.** ZeroGPT stamped everything 100%
   except one too-short text. Clever differentiates (99/95/95) and shows its
   work sentence by sentence.
2. **The rewrite fixed the right signals and created new ones.** P01's rewrite
   dropped "Generic phrasing", "Overly polished language", "Lack of specific
   details", and "Template-like introduction" — the exact things `write-human`
   targets — but gained "Repetitive sentence patterns", "Predictable sentence
   endings", and "Unusual punctuation consistency", because it compressed into
   short, even sentences.
3. **Over-compression is a real detector cost.** Two of three rewrites fell
   under Clever's 80-word floor. The skill's own audit warning ("has it shrunk
   into a summary?") maps directly to a detector gate here: a faithful rewrite
   should stay above 80 words and vary sentence length, not just shrink.
4. **Both detectors agree on the bottom line.** Style rewrites alone do not
   reliably move detector scores; the deep, evidence-backed lever remains
   regenerating through a base model (HIP, see `SKILL.md`), not editing polish.

Caveats: one detector; scores vary run to run; short/formal/non-native text is
over-flagged by every detector, Clever included.
