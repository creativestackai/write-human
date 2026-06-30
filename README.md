# write-human

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![SKILL.md](https://img.shields.io/badge/format-SKILL.md-blue)](https://agentskills.io)
[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](CHANGELOG.md)

A Claude skill that rewrites a draft so it reads like a person wrote it, not a model. It strips the statistical and stylistic tells that AI detectors flag, puts the rhythm and voice back, and makes the writing better in the process.

Most "humanizers" hand you a list of banned words and call it done. That barely works. Swap "delve" for "explore" and you still have flat, evenly paced, opinion-free text, which still flags as AI and now reads worse too. This skill is built on a different premise.

## The idea

AI detectors do not really measure "a machine wrote this." Research on base versus instruction-tuned models found detectors flag the *polish*: the politeness, the balance, the even rhythm, the hedging, the tidy parallel structure that models pick up from being trained to be helpful assistants. They score two things above all:

- **Perplexity**, how predictable each word is. Models take the safe path every time.
- **Burstiness**, how much sentence length varies. Models cluster around an average; humans swing wildly.

So the fix is not deleting forbidden words. It is rewriting so the text reads like a specific person continuing a thought: uneven rhythm, real opinions, concrete detail. That move raises both numbers the detectors care about, and it happens to be the same thing that makes writing engaging. Undetectable and good are the same target.

## What's inside

```
write-human/
├── SKILL.md                          the workflow and the core idea
├── reference/
│   ├── why-detectors-flag-text.md    how detection works, and why the fixes work
│   ├── ai-tells.md                   the full pattern catalog with before/after fixes
│   └── craft-levers.md               how to make the rewrite genuinely engaging
└── examples/
    └── before-after.md               full worked rewrites in three registers
```

The skill runs a five-step loop: diagnose the tells, rewrite in three layers (lexicon, structure, rhythm), re-voice it with a real point of view, run an adversarial self-audit ("what still reads as AI? now fix that"), and read it aloud.

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

This skill changes surface style, the things a statistical detector measures. It does **not** remove a hard cryptographic watermark like Google's SynthID, which is baked into generation itself and cannot be reliably edited out without wrecking the text. No tool can honestly promise a "0% AI" score, because detectors are probabilistic and every one scores the same text differently.

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

Built from three sources: a deep research survey of the AI-detection and humanization literature (perplexity, burstiness, the base-model finding, watermarking, the false-positive studies), the pattern catalog in [Wikipedia's "Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) maintained by WikiProject AI Cleanup, and a set of classic copywriting craft principles for the engagement layer.

## License

MIT. See [LICENSE](LICENSE). Use it, fork it, change the copyright line to your own name.
