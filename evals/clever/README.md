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
| P01 | 99 | 95 (88 words, human 5%) | 4-point drop |
| P05 | 95 | 85 (84 words, human 15%) | 10-point drop |
| P04 | 95 | not scored (39 words) | puffery-heavy draft; faithful rewrite is ~55 words, under the floor |

## What it tells us

1. **Clever is more honest than ZeroGPT.** ZeroGPT stamped everything 100%
   except one too-short text. Clever differentiates (99/95/95) and shows its
   work sentence by sentence.
2. **Length and voice move the score.** The fuller P05 rewrite (84 words, first
   person) dropped 95→85 and human 5%→15%; the impersonal P01 only moved 99→95.
   A real voice plus enough length is what Clever rewards.
3. **Rhythm is the remaining tell.** Even the fuller rewrites keep "Repetitive
   sentence patterns", "Predictable sentence endings", and "Similar sentence
   rhythms". Over-compression fixed "generic phrasing"/"overly polished
   language" but created new rhythm tells — sentence-length variance is the
   lever, now with detector evidence (codified in `SKILL.md` 2.1.1).
4. **Puffery-heavy drafts are untestable at short honest length.** P04's draft
   is mostly filler, so its faithful rewrite is ~55 words — under Clever's
   floor. Short honest rewrites of thin drafts can't be scored by Clever.
5. **Both detectors agree on the bottom line.** Style rewrites move scores a
   little, not reliably to "human"; the deep, evidence-backed lever remains
   regenerating through a base model (HIP, see `SKILL.md`), not editing polish.

Caveats: one detector; scores vary run to run; short/formal/non-native text is
over-flagged by every detector, Clever included.
