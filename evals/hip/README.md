# HIP (base-model) pass vs Clever AI Detector (2026-11-25)

Tests the deepest lever in `write-human`: regenerate the draft through a
non-instruction-tuned base model and check whether that, finally, moves a
detector.

## Method

- Model: `Qwen3-8B-Base` (Q4_K_M), served by Ollama, imported raw (no chat
  template).
- `scripts/hip.py`, 2 passes, ~200-word chunks, temperature 0.9, top_p 0.95.
- Input: the same return-to-office AI draft used in `evals/voices/` (its raw
  score: 99% AI).
- The base model preserved the draft's facts (rule zero held) and produced a
  visibly different, uneven, casual register.

## Result

| text | AI score | verdict |
| --- | --- | --- |
| human control (published columnist) | 3 | human |
| input AI draft | 99 | ai |
| **HIP base-model output (2 passes)** | **97** | ai |

## Finding

The base-model pass did **not** beat the detector. Its output scored 97% AI,
statistically identical to every instruction-tuned rewrite (97-99%). Clever's
signals shifted — "artificially balanced arguments" and "excessive transition
words" replaced the polish signals — but the score did not move.

The "base models read as human" result in the research (arXiv 2605.19516) was
measured against **GPTZero and Pangram**, not Clever, and did not reproduce
here. Two honest takeaways:

1. **Clever flags LLM output broadly** — instruction-tuned *and* base-model.
   Neither a style edit nor a base-model regeneration reliably clears it. The
   only thing that passed is genuinely human-written prose.
2. **HIP is still shipped**, because it may move *other* detectors (the paper's
   GPTZero/Pangram) and it changes the character of the text — but it is not a
   detector-beater, and it must not be sold as one.

Bottom line, unchanged from `evals/voices/` and the skill's own honesty section:
a style or regeneration pass makes text read human; it does not guarantee what a
classifier says.
