# Pre-registration: revised 2.0 test

Written 2026-11-12, after the revised skill was frozen (hashes in FROZEN.sha256, skills/v21)
and before any holdout passage or any output on it existed.

What changed between frozen 2.0 (skills/v20) and the revision (skills/v21): the
reasoning-model rule keeps the draft's order of commitment and every hedge and condition
instead of leading with the conclusion; rule zero says strength is content; the audit asks
whether any claim got stronger or weaker; the checker left the numbered workflow; "Match the
page it sits on" mentions `--context`. Nothing else.

Holdout: 10 new passages T01-T10, written after the freeze by the same author as the skill.
- T01-T04: one passage inside a longer document, surrounding paragraphs supplied (kind
  "passage"). The four surrounding voices differ (casual, formal, technical, first-person
  reflective).
- T05-T07: reasoning-model prose with hedged or conditional conclusions (kind "reasoning").
- T08-T09: ordinary assistant drafts (kind "ordinary").
- T10: human-style control, excluded from scored totals (kind "control").
Nine scored passages.

Arms: v1.1 (skills/v11), frozen 2.0 (skills/v20), revised 2.0 (skills/v21).
Generation: Sonnet, neutral task prompt "Rewrite this so it reads like a person wrote it,
not an AI." One agent per arm per batch of five passages, as in Part 5.
Judging: blind 3-way ranking, scores 0-2, two label orders, two judge families (GPT via
Codex, Gemini via Antigravity). Judge prompt is instr3.py: the Part 5 prompt cut to three
texts, with two additions decided before the holdout existed: a per-text `strength_changes`
list, and one sentence asking, where surrounding paragraphs are given, whether the rewrite
sounds like the same author.

Primary question: is the revised 2.0 more human-sounding than v1.1?
- SUCCESS: mean passage-level human-sounding difference (revised minus v1.1) > 0 and the 90%
  passage-bootstrap interval excludes 0.
- DIRECTIONAL: mean > 0 but the interval includes 0.
- FAIL: mean <= 0.
Guardrails (must hold or the revision fails regardless): judge-listed invented specifics per
text <= 0.5; mean fidelity rank not worse than v1.1 by more than 0.3.

Secondary (reported, not decisive):
- revised minus frozen 2.0 on fidelity over the three reasoning passages, and judge-listed
  strength changes per text for each arm there. This is the direct test of the fix.
- revised minus v1.1 on human-sounding over the four passage-in-document cases.
- revised minus v1.1 on human-sounding over the three reasoning passages (the sinking
  assumption: that the shape can stay and the text still read less machine-made).
- whether T10 comes back unchanged.

Known weaknesses, stated in advance: nine passages, one generation per arm, judge noise that
Part 5 showed to be large (near-identical texts ranked oppositely), and a holdout written by
the skill's author. A SUCCESS here would be modest evidence; anything else is not evidence of
harm either.
