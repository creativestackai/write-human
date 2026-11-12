# Changelog

All notable changes to this skill are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the skill uses
[semantic versioning](https://semver.org/).

## [2.1.0] - 2026-11-12

Operationalizes the one evidence-backed lever the skill had named but not
turned into a recipe: the base-model finding (detectors track
instruction-tuning, not "machine-ness").

### Added
- "The deepest lever, when it is available" in `SKILL.md`: the HIP recipe
  (Humanization by Iterative Paraphrasing) — regenerate through a
  non-instruction-tuned base model in short chunks, two or three passes, then
  the voice pass on top. Marked as the strongest available move, with the
  standing caveat that no detector score is guaranteed.
- `reference/why-detectors-flag-text.md` section 5 now gives the HIP recipe,
  and section 10 puts base-model paraphrasing first when regeneration is
  possible.
- Step 2's "Try more than one" is now "Variants, not a first draft": never
  accept the first rewrite, generate structurally different variants before
  deciding, framed as the editing form of the same base-model move.

### Changed
- The four refusals in "Honesty and limits" (plant errors, attack a
  watermark, disguise pasted-in generated text, obscure facts) are unchanged,
  deliberately re-kept against the parts of the 2025-26 detection literature
  that recommend exactly those moves (engineered error injection, semantic
  desynchronization, factual obfuscation).

## [2.0.0] - 2026-11-12

Built on the 1.1.0 fidelity patch, with the parts of the 2025-26 detection
research that a prompt-based skill can act on. The research's model-level
proposals (base-model paraphrasing, multi-model splicing, hidden-state
perturbation) are out of reach for a skill and are not attempted.

**Test status.** `scripts/check.py` has unit tests. The fidelity rules carried
over from 1.1.0 were validated in three blind comparison rounds. The new 2.0
instructions were then run through the same comparison on a fresh holdout
(`evals/comparison/REPORT.md`, Part 5) and missed the pre-registered bar:
2.0 minus 1.1 on human-sounding was -0.32 [-0.92, +0.28], with fidelity
level (+0.21) and 0.17 invented specifics per text. Reasoning-model handling
("lead with the conclusion") raised the strength of claims on both test
passages. That rule was then rewritten: the draft's order of commitment and
every hedge and condition now stay, rule zero says strength is content, the
audit asks whether any claim got stronger or weaker, and the checker reports
dropped hedges and takes `--context` for a passage inside a longer document.
The checker moved out of the numbered workflow (generators skipped it) into
a "Checking by machine" note. A second comparison on a new holdout (Part 6)
put the revision directional against 1.1 on human-sounding (+0.23
[-0.33, +0.78]) and ahead on fidelity (+1.04 [+0.69, +1.32]), with no
strengthened claims listed on the three reasoning-model passages.
Matching a passage to its page did not beat 1.1 on voice.
Paragraph-level restructuring and sample echo come from the 1.2 experiment,
whose result was directional, not significant.

### Added
- **Step 0, routing.** Five draft types (human-written and flagged, assistant
  polish, reasoning-model prose, a passage inside a longer document, a draft
  with a writing sample), each with its own treatment and reference to load.
- **Reasoning-model tells** (`reference/ai-tells.md` section 11): proof-shaped
  paragraphs, deliberation markers, forced symmetry, discarded hypotheses,
  metronome pacing, with a fidelity-safe fix order. New worked example 5.
- **Slogan closers and comment bait** (section 12), with the rule that a real
  call to action stays in the draft's own words.
- **Over-polish** (section 13) and "Do not sand it flat": keep the author's
  fragments, contractions, and punctuation habits; never plant an error.
- **Voice matching**: echo the writing sample; match the page a passage sits on.
- **Variant pass**: two or three structurally different versions of the opener
  and of any paragraph the audit still flags.
- **`scripts/check.py`**: standard-library checker for added numbers, names,
  quotes, or narrator; sentence-length variation; surface tells; distance from
  a writing sample. Tests in `tests/`. `Bash` added to `allowed-tools` for it.
- **The 2025-26 detectors** in `reference/why-detectors-flag-text.md`:
  RepreGuard, Exons-Detect, AdaDetectGPT, GigaCheck, Pangram 4, agentic
  detection, GECScore, and public-key watermarks, each with what it means for
  a rewrite.
- "The draft is material, not instructions" (prompt-injection guard).

### Changed
- Structure layer now works at paragraph level before sentence level.
- Audit question 1 also asks whether the skeleton was merely polished and
  whether the rewrite sounds like the sample or the surrounding page.
- Output: the diagnosis names the route taken; the self-audit shows both
  questions.
- "Honesty and limits" lists four things the skill will not do: plant errors,
  attack a watermark, disguise pasted-in generated text, obscure facts.
- README no longer says "undetectable".

## [1.1.0] - 2026-10-24

A minimal fidelity patch. A controlled same-model comparison against
blader/humanizer (`evals/comparison/REPORT.md`) found that v1 sounded human
but invented about four small supporting details per rewrite, no better than
using no skill. Voice and rhythm behaviour is unchanged.

### Added
- "Rule zero: keep what it says": every fact, number, scene, and experience
  must come from the draft, a sample, or the user; no invented narrator;
  ask or write the plainer sentence instead of inventing a detail.
- Audit prompt "What did I add or drop?", checked claim by claim.
- Optional **Flags** line in the output for details only the author can supply.
- `NOTICE` crediting blader/humanizer and Wikipedia's "Signs of AI writing".

### Changed
- "Trade vague claims for specific detail" now allows specifics only when the
  draft or user supplies them; "I" only where the draft is first person.
- `reference/craft-levers.md`: "quantify the pain" and "testimonials" no longer
  coach inventing numbers or quotes.
- `reference/ai-tells.md`: removed "After" examples that invented sources,
  dates, and quotes.
- `examples/before-after.md`: rewritten so no example adds facts.
- Compact example in `SKILL.md` no longer invents a speaker or a survey.

## [1.0.2] - 2026-07-29

### Changed
- Relicensed from MIT to Apache License 2.0. Updated `LICENSE`, `package.json`,
  `SKILL.md` frontmatter, and the license references in `README.md` and
  `CONTRIBUTING.md` accordingly.

## [1.0.1] - 2026-07-01

### Fixed
- `examples/before-after.md`: closing summary said "In all three," referring
  to the example count, despite the file containing four worked rewrites.
  Corrected to "In all four."
- `.gitignore`: removed an internal tool reference ("Agent-council") from a
  comment that had no place in a public repo.

## [1.0.0] - 2026-06-29

First public release.

### Added
- The five-step humanize loop in `SKILL.md`: diagnose, rewrite in three layers
  (lexicon, structure, rhythm), re-voice, adversarial self-audit, read aloud.
- `reference/why-detectors-flag-text.md`: how detection works (perplexity,
  burstiness, the base-model finding, the false-positive crisis, the SynthID
  watermark caveat).
- `reference/ai-tells.md`: the pattern catalog with frequency data and
  before/after fixes, plus an optional quick-scan word list.
- `reference/craft-levers.md`: the engagement layer (headlines, openings, pain
  quantification, the "so what" chain, rhythm, testimonials).
- `examples/before-after.md`: four worked rewrites, including the falsely-flagged
  non-native-English case the skill is built for.
- A register-calibration note so formal genres (technical, legal, academic) keep
  their justified voice instead of being forced casual.
- Honest limits section: no "0% AI" promises, the watermarking caveat, and a
  steer away from passing off unread model output.
