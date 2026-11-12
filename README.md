# write-human

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![SKILL.md](https://img.shields.io/badge/format-SKILL.md-blue)](https://agentskills.io)
[![Version](https://img.shields.io/badge/version-2.1.1-blue.svg)](CHANGELOG.md)

A Claude skill that rewrites a draft so it reads like a person wrote it, not a model. It strips the statistical and stylistic tells that AI detectors flag, puts the rhythm and voice back, and makes the writing better in the process.

Most "humanizers" hand you a list of banned words and call it done. That barely works. Swap "delve" for "explore" and you still have flat, evenly paced, opinion-free text, which still flags as AI and now reads worse too. This skill is built on a different premise.

## The idea

AI detectors do not really measure "a machine wrote this." Research on base versus instruction-tuned models found detectors flag the *polish*: the politeness, the balance, the even rhythm, the hedging, the tidy parallel structure that models pick up from being trained to be helpful assistants. They score two things above all:

- **Perplexity**, how predictable each word is. Models take the safe path every time.
- **Burstiness**, how much sentence length varies. Models cluster around an average; humans swing wildly.

So the fix is not deleting forbidden words. It is rewriting so the text reads like a specific person continuing a thought: uneven rhythm, the author's own opinions, the concrete detail the draft already holds. That is also what makes writing engaging. Human-sounding and good are the same target.

One rule sits above all of it: **the rewrite says only what the draft said.** No invented numbers, names, anecdotes, or narrator. Where a real detail would help, the skill asks you for it.

## What's inside

```
write-human/
├── SKILL.md                          the workflow and the core idea
├── reference/
│   ├── why-detectors-flag-text.md    how detection works, including the 2025-26 detectors
│   ├── ai-tells.md                   the full pattern catalog with before/after fixes
│   └── craft-levers.md               how to make the rewrite genuinely engaging
├── examples/
│   └── before-after.md               five worked rewrites, each with its audit
├── scripts/
│   ├── check.py                      counts what can be counted: added facts, rhythm, voice match
│   └── zerogpt_benchmark.py          runs drafts/rewrites through ZeroGPT's detector
├── evals/
│   ├── zerogpt/                      ZeroGPT benchmark (corpus, results, notes)
│   └── clever/                       Clever AI Detector benchmark (corpus, results, notes)
└── tests/
    └── test_check.py                 unit tests for the checker
```

The skill first routes the draft, because a falsely flagged human essay, a buzzword-heavy assistant draft, and a proof-shaped reasoning-model draft need different handling. Then it diagnoses the tells, rewrites in three layers (lexicon, structure, rhythm), re-voices it to match the author, runs an adversarial self-audit ("what still reads as AI?", "what did I add or drop?", "did any claim get stronger or weaker?"), and reads it aloud.

## What's new in 2.1

- **The base-model lever.** The research this skill is built on says detectors flag instruction-tuning, not "machine-ness." 2.1 turns that into a recipe: HIP (Humanization by Iterative Paraphrasing) — regenerate through a non-instruction-tuned base model in short chunks, then the voice pass on top — for when you control how the text gets made.
- **Variants, not a first draft.** Never accept the first rewrite. Generate structurally different versions, pick against the sample, then audit.
- **Real-detector benchmarks.** `scripts/zerogpt_benchmark.py` + `evals/zerogpt/` (ZeroGPT) and `evals/clever/` (Clever AI Detector) run drafts and rewrites through actual detectors. Both are browser-collected (neither offers a free API); Clever returns a probability score plus sentence-level signals and is the more informative instrument. First results are in each folder's `results.json`.

## What's new in 2.0

- **Fidelity is rule zero.** A controlled comparison ([evals/comparison/REPORT.md](evals/comparison/REPORT.md)) found 1.0 added about four unsupported details per rewrite. The fix cut that to about 0.3.
- **Routing.** Five draft types, each with its own treatment and its own reference to load.
- **Reasoning-model tells.** Proof-shaped paragraphs, deliberation markers, forced symmetry: tells that live in the argument's staging, not its words. The fix takes off the staging and keeps the draft's order, hedges, and conditions.
- **Voice matching.** Echo the author's writing sample, or the page the passage sits on.
- **"Do not sand it flat."** The author's fragments and habits stay. Errors are never planted.
- **A checker you can run yourself.** `scripts/check.py` compares a rewrite against the draft, a writing sample, and the page around it:

```bash
python3 scripts/check.py rewrite.txt --source draft.txt --sample sample.txt --context surrounding.txt
```

Every flag is optional. It lists numbers, names, quotes, or a narrator that appear only in the rewrite, hedge words ("may", "suggests", "provided") that went missing or appeared, sentence-length variation, surface tells, and where the rewrite sits apart from the sample or the surrounding paragraphs. Each line is a place to look, not a verdict. Standard-library Python. It is not an AI detector.

Tested, with a mixed result: in a blind comparison on a fresh holdout (Part 5 of the report), 2.0 matched 1.1 on fidelity and was not shown to sound more human. Leading with the conclusion on reasoning-model drafts made two rewrites claim more than their drafts did, so that rule was rewritten to keep the draft's order and hedges. A second comparison (Part 6) shows the strengthened claims gone and fidelity ahead of 1.1; sounding more human than 1.1 is still not shown. See the changelog.

## Install

**Claude Code:** drop the `write-human/` folder into your skills directory (`~/.claude/skills/write-human/`), or package it and install:

```bash
zip -r write-human.skill write-human
```

Then double-click the `.skill` file, or point Claude Code at the folder.

**Claude Desktop / Cowork:** install the packaged `write-human.skill` file from the app.

The skill triggers on its own when you ask to humanize, de-slop, or fix the AI voice in a draft. You can also invoke it by name.

**Other agents:** the skill is a plain `SKILL.md` plus reference files, so it works with any tool that reads the [agentskills.io](https://agentskills.io) format (Cursor, Copilot CLI, OpenHands, and others). Drop the folder into that tool's skills directory.

## How to use it

Give it a draft and ask:

> Humanize this. It sounds like ChatGPT wrote it.

> Rewrite this landing page copy so it doesn't read as AI.

> My essay keeps getting falsely flagged by a detector. Fix the voice without changing my argument.

You will get back a short diagnosis, a rewrite, an honest self-audit of what still reads synthetic, and a final version. Ask for "just the clean text" if you do not want the working.

## What it does not do

Read this part. It matters.

This skill changes style: words, structure, rhythm, voice. It does **not** remove a cryptographic watermark like Google's SynthID, which is baked into generation itself and cannot be reliably edited out without wrecking the text. No tool can honestly promise a "0% AI" score, because detectors are probabilistic and every one scores the same text differently. The newest detectors read a model's internal representation of the text or search the web for its sources, and are built to survive paraphrasing, so the promise is emptier now than it was.

It also will not plant grammar mistakes to look human, try to scramble a watermark, disguise where generated text was pasted into someone else's writing, or blur facts so they are harder to check.

The reason to use this is that AI detection is badly biased and gets real people in trouble. One Stanford study had seven detectors falsely flag 61% of TOEFL essays that humans actually wrote, because non-native English and tightly structured technical writing both look "too clean" to a scanner. Helping a real writer sound like themselves, so they are not falsely accused and so their work actually lands, is the point. Dressing up unread model output to pass it off where that is forbidden is not, and the skill will steer you away from that framing.

## How this differs from a banned-word linter

There are good tools that hand you an exhaustive tiered list of AI words, a
severity score, and a flag-only mode. The `avoid-ai-writing` skill is one. This
is not that, on purpose. A blacklist tells you which words to delete; it cannot
tell you that the real problem is even rhythm, no point of view, and three
sentences in a row at the same length. `write-human` is the method: voice,
burstiness, concrete detail, and an adversarial self-audit, with a short word
list as a convenience rather than the main event. The two pair well. Rewrite
here for voice, then run a linter as a final pass if you want one.

## Feedback

Found a case where the skill fires when it shouldn't, or a rewrite that still
reads synthetic? Open an issue. See [CONTRIBUTING.md](CONTRIBUTING.md) for how
trigger tuning and new patterns get proposed.

## Credits

Built from five sources: a 2026 survey of third-generation detectors (RepreGuard, Exons-Detect, GigaCheck, GECScore, Pangram 4, agentic detection) read for what a style edit can and cannot honestly do, a deep research survey of the AI-detection and humanization literature (perplexity, burstiness, the base-model finding, watermarking, the false-positive studies), the pattern catalog in [Wikipedia's "Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) maintained by WikiProject AI Cleanup, a set of classic copywriting craft principles for the engagement layer, and the fidelity-first editing approach of [blader/humanizer](https://github.com/blader/humanizer) (MIT): keep every supported claim and invent nothing. See [NOTICE](NOTICE) and the comparison in [evals/comparison/REPORT.md](evals/comparison/REPORT.md).

## License

Apache License 2.0. See [LICENSE](LICENSE). Use it, fork it. Attribution and the license notice carry over per the terms.
