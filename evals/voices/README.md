# Voice-catalog demo against Clever AI Detector (2026-11-25)

A direct test of the five-voice catalog (v2.4.0) against Clever. The question:
does writing through a named voice move the detector score, or not?

## Method

One AI-flavoured draft (return-to-office opinion, ~120 words) was rewritten once
per voice (insider columnist, MJ, SD, AA, combined), plus two control texts
submitted as-is:

- **human_journalist_excerpt** — a verbatim paragraph from a published newspaper
  columnist (genuinely human prose, pasted untouched).
- **human_casual_attempt** — a deliberately casual, lower-case "human" note the
  assistant wrote to test whether Clever would score *anything* low.

Two "improved" rewrites (real company names and dates added, keyword repetition
broken, punctuation varied) and one pure first-person narrative were also run,
to rule out the obvious fixes.

## Results

| text | AI score | verdict |
| --- | --- | --- |
| human journalist (control) | **3** | human |
| human casual (assistant-written) | 93 | ai |
| original AI draft | 99 | ai |
| insider columnist | 98 | ai |
| MJ | 99 | ai |
| SD | 99 | ai |
| AA | 99 | ai |
| combined | 99 | ai |
| combined v2 (specifics added) | 97 | ai |
| insider columnist v2 (specifics added) | 99 | ai |
| narrative (first person) | 99 | ai |

## Finding

The voices are **genuinely distinct as style** — that feature works. But none of
the assistant-generated rewrites beat the detector: they all scored 97-99% AI,
statistically identical to the raw draft. The single human-written text scored
3%.

The detector is not broken — it separates human prose (3%) from everything the
assistant produced (93-99%), including the deliberately "casual" control. What
it is reading is not the surface style (voice, rhythm, punctuation, specifics
all failed to move it) but the generator's fingerprints, which survive style
editing.

This revises an earlier impression that the voiced rewrites "score excellently
on Clever": those 2-15% figures were single, unreproduced runs. The reliable,
reproducible result is that **an instruction-tuned model rewriting a draft does
not fool Clever, whatever voice it uses.**

The deeper lever stays the one already documented in `evals/clever/` and
`SKILL.md`: regenerate through a minimally-tuned base model (Humanization by
Iterative Paraphrasing), which lacks the RLHF/instruction-tuning artifacts the
detector tracks. That is an engineering change (run a base model locally), not a
prompt or style change.
