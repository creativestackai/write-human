# write-human vs humanizer: controlled output comparison

Date: 2026-10-24. Versions: write-human `fd1a707` (SKILL.md 1.0.2), blader/humanizer `8c307f3` (SKILL.md 3.1.0).

The earlier assessment compared READMEs, instructions and published examples, not outputs from one model. This run fixes that.

## Method

- **Generation model:** Sonnet 5.5 for every rewrite, one independent run per passage and arm. 10 passages x 3 arms = 30 rewrites.
- **Arms:** (1) baseline, no skill; (2) write-human (SKILL.md + `ai-tells.md` + `craft-levers.md` loaded, i.e. best case); (3) humanizer (SKILL.md).
- **Task prompt:** identical and neutral for all arms: "rewrite so it reads like a person wrote it, not an AI." No "preserve the facts" instruction, so each skill had to supply that itself.
- **Corpus** (`corpus.json`): generic opinion (2, fabrication bait), marketing copy with 2 stats, API docs with code spans, fact-dense company profile, LinkedIn post with real facts + writer's voice sample, thread reply with context, formal abstract, support email, and one genuinely human-written passage (do-no-harm control).
- **Judging:** blind and anonymized, 2 judge families outside Claude (GPT via Codex, Gemini via Antigravity), each passage judged twice with labels rotated. Judges rank human-sounding quality and fidelity, list every unsupported specific and dropped fact, and estimate P(reads as AI).
- **Valid judgments:** 38 of 40 (two Gemini calls timed out twice). P08 excluded from rankings because two skill outputs were character-identical to the source (34 judgments).
- **Objective metrics** (`metrics.py`): dashes, AI-lexicon hits, not-X-but-Y, sentence-length variation, length ratio.

## Results

| Arm | Human-sounding (0-2) | Fidelity (0-2) | Overall wins (of 34) | Unsupported specifics / text | Dropped facts / text |
|---|---|---|---|---|---|
| Baseline | 0.88 | 0.56 | 4 | 4.21 | 2.85 |
| write-human | 0.94 | 0.56 | 4 | 3.94 | 2.91 |
| humanizer | 1.18 | **1.88** | **26** | **0.24** | 2.26 |

By judge family, human-sounding score (baseline / write-human / humanizer):
- Codex (GPT): 0.89 / 0.67 / **1.44**
- Gemini: 0.88 / **1.25** / 0.88

Head to head, human-sounding: write-human preferred 15 times, humanizer 19. Fidelity: humanizer preferred in 34 of 34.

Objective: both skills removed every em dash, banned-lexicon word and not-X-but-Y. Length vs source: baseline 1.01x, write-human 1.08x, humanizer 0.76x. Sentence-length variation: source 0.44, baseline 0.56, write-human 0.59, humanizer 0.49.

## What the evidence supports

1. **Fidelity is the clear, robust finding.** Humanizer adds about 18x fewer unsupported specifics than write-human or the baseline, in every passage, under both judges and both label orders. Write-human is statistically indistinguishable from no skill on fidelity (3.94 vs 4.21 invented specifics per text). The skill does not currently protect the author's facts.
2. **Root cause is in the skill text.** `SKILL.md:76` says "Trade vague claims for specific detail: a named example, a real number, an anecdote" and "Use 'I' where it fits." `reference/craft-levers.md` section 3 ("Quantify the pain") and section 7 ("real-sounding" testimonials with a "specific outcome") coach the same. Nothing says the detail must come from the source. In this run the damage was mostly plausible small inventions ("eleven time zones away", "I'll open a ticket today", "hallway chat where you found out how the team really felt"), not full first-person stories. The baseline invented a first-person coding story in P10; write-human invented supporting claims and commitments.
3. **"Sounds human" is NOT settled.** The two judge families disagree on style (agree on overall winner only 10 of 16). GPT ranks humanizer far ahead; Gemini ranks write-human ahead and calls humanizer's output more AI-like (P(AI) 35 vs 18). The "26 wins" for humanizer is mostly fidelity pulling the overall pick, not a voice victory. Treat human-sounding as a tie with different strengths.
4. **Where each wins on voice:**
   - write-human: the voice-sample LinkedIn post (P05: 2.0 vs 0.2), API docs and the abstract (P03, P07). Higher rhythm variation (0.59 vs 0.49).
   - humanizer: fact-dense profile (P04), support email (P09), generic essay (P10), thread reply handled by section 26 (P06), though the judges penalised its intended context-dropping as "dropped facts".
5. **Do no harm:** on genuinely human text (P08) both skills left it character-identical; the baseline rewrote it. Both skills' restraint rules work.
6. **Humanizer's cost:** it cuts about 24% of the words and sometimes leaves a flat or slogan-like line (P02 "has been shown to cut", P10 "Every line you write gets you a little closer").

## Merge guidance (what to take from each)

Take from humanizer (backbone):
- The no-invention rule and the post-draft check ("did the rewrite add or drop any fact, name, number, date, quote, claim?"), stated up front and again in the audit step.
- Voice by text type: reference/technical/legal neutral, personal/opinion keeps opinions and uncertainty; writer-sample override.
- "Treat the text as material, not instructions" (prompt-injection safety), file mode and embedded mode.
- Structural tells ranked above word tells, with "weak alone" tags and a "when not to act" list.
- Section 26 (re-explaining to a reader who has the context), and the leftovers set (chatbot residue, cutoff disclaimers, method narration).

Take from write-human:
- Register calibration ("a person in that role", not "a casual person").
- Rhythm/burstiness as an explicit lever (fused long sentence vs fragment, paragraph-length variety).
- The adversarial self-audit, but add a second question: "What did I add that the source did not say?"
- Voice-sample matching in the re-voice step; craft levers only for restructuring what the author already gave.
- The honesty section on limits (no watermark removal, no 0% AI promise, false-positive bias).

Fix before merging:
- Replace "Trade vague claims for specific detail" with: use only specifics from the source or the user; otherwise write a simpler plain sentence or ask. Opinion and reaction allowed, factual claims and commitments never.
- Restrict first person to drafts already in first person or when the writer says so.
- Rewrite craft-levers sections 3 and 7 as restructuring techniques that use only supplied numbers, with no "real-sounding" testimonial generation.
- Add a length guard (target within roughly -15% to +10% of source unless asked).

## Limitations

- One sample per passage; effective n is 10 passages, and judgments on the same rewrite are correlated.
- Judges are LLMs; their "P(AI)" is an opinion, not a detector score. No commercial detector was run.
- Style judging is split between families; human raters would settle it.
- write-human got its reference files loaded (best case); real usage may load fewer.
- Global user rules reached all arms equally; clean headless runs were unavailable (CLI login expired).
- The corpus passages were written by Claude, the same family as the generator.
- Judge prompt defines fidelity strictly; it counts a deliberate cut of context (P06) as a dropped fact.

## Files

`corpus.json`, `inputs/`, `out/{baseline,wh,hz}/`, `judge/` (blind packets, keys, raw judge outputs, `parsed.json`), `metrics.py`, `aggregate.py`.

---

# Part 2: the merged v2 skill, tested

Date: 2026-10-24. v2 = branch `v2-merged` (SKILL.md 2.0.0). Same method as Part 1, with these changes: 4-way blind ranking (baseline, write-human v1, humanizer, v2; scores are 0-3), each passage judged under 2 label orders by 2 judge families, and a **holdout set** of 6 fresh passages (`v2-run/holdout.json`) written before v2 was run on them. v2 was frozen (hash in `v2-run/FROZEN.sha256`) before any holdout generation and was not edited afterwards. Raw packets, judge outputs and parsed results are in `v2-run/`; tables are in `v2-run/results_v2.txt`.

One revision was made between the first draft and the frozen version, using only development-set feedback (judges called the first draft "compressed", "staccato", "executive summary"): don't-shrink-into-a-summary rule, courtesy kept, pep-talk closers, writing-sample echo, a second audit prompt. Both versions are reported.

## Results

| Set | Arm | Human-sounding (0-3) | Fidelity (0-3) | Overall wins | Invented specifics / text | P(AI) |
|---|---|---|---|---|---|---|
| Dev, first draft (n=32) | baseline | 1.34 | 0.59 | 2 | 4.09 | 23 |
| | write-human v1 | 1.69 | 0.50 | 1 | 4.16 | 23 |
| | humanizer | 1.75 | 2.28 | 16 | 0.34 | 26 |
| | **v2** | 1.22 | **2.62** | 13 | **0.16** | 31 |
| Dev, frozen v2 (n=34) | baseline | 1.44 | 0.65 | 2 | 4.06 | 24 |
| | write-human v1 | 1.53 | 0.44 | 1 | 4.06 | 22 |
| | humanizer | **1.88** | **2.53** | **20** | 0.29 | 27 |
| | v2 | 1.15 | 2.38 | 11 | 0.21 | 35 |
| **Holdout (n=18)** | baseline | 1.33 | 0.72 | 0 | 3.50 | 24 |
| | write-human v1 | 1.61 | 0.28 | 0 | 3.78 | 24 |
| | humanizer | **2.00** | 2.44 | **11** | 0.39 | 21 |
| | v2 | 1.06 | **2.56** | 7 | **0.06** | 32 |

Holdout head to head, v2 vs humanizer: human-sounding 3 vs 15 judgments; fidelity 10 vs 8. v2 vs v1: human-sounding 7 vs 11; fidelity 18 vs 0.

## What this says

1. **The fidelity fix worked.** v1 invented about 4 specifics per rewrite (no better than no skill); v2 invents about 0.1-0.2. That is a real, repeatable change (18 of 18 holdout judgments prefer v2 to v1 on fidelity).
2. **v2 does not beat humanizer.** On the clean holdout it ties humanizer on fidelity (2.56 vs 2.44, 10-8) but loses clearly on human-sounding (1.06 vs 2.00, 3-15). It also scores lowest of the four arms on human-sounding, below even the no-skill baseline (1.33), and judges estimate it reads most AI-like (P(AI) 32 vs 21 for humanizer). The one revision did not move this.
3. **Why, from the outputs and judge notes.** v2 is faithful but does a sentence-by-sentence polish of the draft ("mechanical", "formulaic AI paraphrase"). It keeps the draft's skeleton, including engagement-bait closers ("What goal are you chasing?") and pep-talk lines. Humanizer restructures at paragraph level, cuts the bait, and lets a voice sample change the register. v1 sounded better than v2 because it freely rephrased and embellished; v2 removed the embellishment but not the underlying template.
4. **So the original merge hypothesis is only half confirmed.** "Take humanizer's fidelity rules" is confirmed: they are what fixes write-human. "Keep write-human's voice and rhythm work" did not survive contact with the test: in v2 it did not produce the voice advantage v1 showed on the voice-sample post, API docs and abstract.

## Caveats specific to Part 2

- Judges still split on style: Gemini is much harsher on v2 (P(AI) about 40) than Codex, though both rank it below humanizer on human-sounding.
- Both v2 passes shaped the revision using dev-set feedback, so dev numbers are optimistic for v2; the holdout is the fair read. The holdout is now also seen and cannot be reused to tune v2.
- 2-4 judge calls per set timed out and are excluded.
- Same-model generation (Sonnet), LLM judges, small n. Real readers or a real detector could rank differently.

## Recommendation

Do not publish v2.0.0 as it stands: it replaces a skill that invents details with one that is faithful but reads worse than the alternative it is meant to improve on. Options: (a) one more iteration aimed at the diagnosed gap (paragraph-level restructuring as a hard step, engagement-bait and CTA closers as a first-class tell, voice-sample matching as the standard), tested on a **new** holdout; (b) ship humanizer-derived fidelity rules as a patch to v1 (smaller change, keeps v1's voice behaviour), or (c) point users at humanizer for fidelity-critical work and keep write-human as the voice-first option with a clear warning.

---

# Part 3: v1.1, the minimal fidelity patch to v1

Date: 2026-10-24. Branch `v1.1-fidelity` (git worktree off `main`); the patch is saved as `v11-run/v1.1-fidelity.patch` and a full snapshot of the changed files is in `v11-run/snapshot/`.

## What the patch changes (and what it leaves alone)

Changed, all fidelity-related: a short "Rule zero: keep what it says" section (every fact, number, scene, and experience must come from the draft, a sample, or the user; no invented narrator; ask or write the plainer sentence); the v1 line "Trade vague claims for specific detail" now allows specifics only when supplied, and "I" only where the draft is first person; a third audit prompt "What did I add or drop?"; an optional Flags line in the output; the compact example in SKILL.md; the invented "After" examples in `reference/ai-tells.md`; the guardrails in `reference/craft-levers.md` (quantify-the-pain and testimonials); and `examples/before-after.md` rewritten so no example adds facts.

Left alone: the voice workflow, the three-layer rewrite, rhythm, re-voice, the read-aloud test, the output structure, `why-detectors-flag-text.md`, and the v1 pattern catalog (no new tells added). The SKILL.md change is 18 lines added and 8 changed.

## Method

Same as Parts 1-2: Sonnet 5.5 rewrites with the identical neutral task prompt; v1.1 frozen (hash in `v11-run/FROZEN.sha256`) before any run; run on all 16 passages (10 development, 6 holdout); blind 5-way ranking (baseline, v1, humanizer, v2, v1.1; scores 0-4) by GPT and Gemini under two label orders; 64 judgments, all valid after retrying 3 timeouts. P08 and H06 (genuinely human-written controls) are excluded from the totals: n = 56 judgments. Tables: `v11-run/results_v11.txt`.

## Results

| Set | Arm | Human-sounding (0-4) | Fidelity (0-4) | Overall wins | Invented specifics / text | P(AI) |
|---|---|---|---|---|---|---|
| **All (n=56)** | baseline | 1.95 | 0.66 | 2 | 4.14 | 22 |
| | write-human v1 | **2.25** | 0.46 | 2 | 4.21 | 22 |
| | humanizer | 2.23 | 2.64 | **21** | 0.50 | 29 |
| | v2 (merged) | 1.57 | **3.12** | 13 | **0.20** | 35 |
| | **v1.1 (patch)** | 2.00 | 3.11 | 18 | 0.32 | 30 |
| Dev (n=36) | v1 | 2.33 | 0.53 | 2 | 4.31 | 22 |
| | humanizer | 2.25 | 2.72 | 15 | 0.44 | 31 |
| | v1.1 | 1.67 | **3.31** | 12 | 0.36 | 35 |
| **Holdout (n=20)** | v1 | 2.10 | 0.35 | 0 | 4.05 | 21 |
| | humanizer | 2.20 | 2.50 | 6 | 0.60 | 26 |
| | v2 | 1.55 | **3.55** | **7** | **0.00** | 31 |
| | **v1.1** | **2.60** | 2.75 | 6 | 0.25 | 22 |

Human-sounding by judge: Codex ranks humanizer 2.68, v1.1 2.04, v2 1.93, v1 1.82, baseline 1.54; Gemini ranks v1 2.68, baseline 2.36, v1.1 1.96, humanizer 1.79, v2 1.21.

Head to head, v1.1 (judgments preferring v1.1 vs the other; ties dropped): vs v1, human-sounding 26:30, fidelity 56:0; vs humanizer, human-sounding 25:31, fidelity 37:19; vs v2, human-sounding 33:23, fidelity 25:31.

## What this says

1. **The patch fixes the fidelity problem.** Invented specifics fall from 4.21 per rewrite (v1) to 0.32, level with v2 (0.20) and below humanizer (0.50). Every one of the 56 judgments prefers v1.1 to v1 on fidelity.
2. **It keeps most of the voice.** Human-sounding is 2.00 vs v1's 2.25, head to head 26:30: close to a tie with a small loss. That is far better than the full v2 rewrite (1.57; v1.1 beats v2 33:23).
3. **Against humanizer, v1.1 is more faithful (37:19) and slightly less human-sounding overall (25:31).** The two judge families split: Codex prefers humanizer, Gemini ranks v1.1 above it. On the six fresh holdout passages v1.1 is ahead of humanizer on both axes (2.60 vs 2.20 human-sounding, 2.75 vs 2.50 fidelity), but six passages is too few to call it.
4. **Dev and holdout disagree about the voice cost.** On the development set v1.1 loses clearly to v1 on human-sounding (1.67 vs 2.33; weakest on P04, P05, P09, P10, P02); on the holdout it does not (2.60 vs 2.10). Treat the true voice cost as "small, with high uncertainty". Judge noise is real: v1.1 changed one punctuation mark in the human-written P08 (a comma to a period) and the judges' ranking of that text swung from average to first/last.
5. **Known gap that the patch does not touch:** stock motivational and engagement-bait closers survive in places (P10 "Every line you write gets you a little closer to mastery"; H04 "What are you chasing?"). Neither v1 nor v1.1 lists them as a tell. Adding them would be the obvious next change, but it would be untested until run on a new holdout.

## Caveats

- The patch was designed from the Part 1 findings, which came from the development passages, so the development numbers favor it; the holdout was not used to design it, though I had seen holdout outputs of the other arms.
- One sample per passage, Sonnet-generated, LLM-judged, no real detector, no human readers. Judge style rankings conflict; the fidelity ranking does not.
- Three judge calls timed out and were retried; none are missing from the totals.

## Recommendation

Make v1.1 the working candidate for the public release. It removes the documented weakness (invented details) while changing the least, and it is the only arm that is near the top on both axes. Before publishing, consider one follow-up (v1.2): add stock motivational closers and engagement-bait questions to the tell catalog, then test on a new holdout. Do not ship v2.

---

# Part 4: v1.2 (voice recovery on top of v1.1), tested on a new holdout

Date: 2026-10-24. Branch `v1.2-voice`. Patch over v1.1: `v12-run/v1.2-over-v1.1.patch`; full patch against main: `v12-run/v1.2-full.patch`; frozen files: `v12-run/snapshot/`, hashes in `v12-run/FROZEN.sha256`.

## What changed in v1.2

Four additions to v1.1, none of which permits adding facts: (1) pep-talk closers and engagement-bait questions as tells, with a catalog section (keep a real call to action); (2) "work at paragraph level, not sentence by sentence"; (3) a register rule for contractions and direct address, plus a stronger writing-sample standard; (4) three extra audit prompts (skeleton merely polished? pep-talk survived? sounds like the sample?).

## Method, with the success criterion fixed in advance

`v12-run/prereg_v12.md` was written after v1.2 was frozen and before any v1.2 output existed. Success = v1.2 minus v1.1 human-sounding > 0 with a 90% passage-bootstrap interval excluding 0; directional = positive mean, interval includes 0; fail = mean <= 0. Guardrails: invented specifics <= 0.5 per text and fidelity not worse than v1.1 by more than 0.3.

New holdout: 8 passages (Q01-Q08) written after freezing, never seen by any arm's design; 4 arms (v1, humanizer, v1.1, v1.2), each generated by Sonnet 5.5 with the same neutral prompt; blind 4-way ranking (0-3) by GPT and Gemini under two label orders. 30 of 32 judgments valid (two Gemini calls on Q01 timed out twice). Q08 (human-written control) excluded: 7 passages, 26 judgments.

## Results

| Arm | Human-sounding (0-3) | Fidelity (0-3) | Wins | Invented specifics / text | P(AI) |
|---|---|---|---|---|---|
| write-human v1 | **2.15** | 0.42 | 3 | 3.96 | 18 |
| humanizer | 1.54 | 1.23 | 4 | 1.00 | 27 |
| v1.1 | 0.96 | **2.23** | **11** | **0.19** | 32 |
| v1.2 | 1.35 | 2.12 | 8 | 0.38 | 28 |

Paired passage-level differences (mean, 90% bootstrap interval):
- v1.2 - v1.1, human-sounding: **+0.3 [about -0.6, +1.2]**; fidelity -0.11 [-0.71, +0.50].
- v1.2 - v1, human-sounding: -0.96 [-1.75, -0.21]; fidelity +1.75 [+0.93, +2.43].
- v1.2 - humanizer, human-sounding: -0.32 [-1.11, +0.46]; fidelity +0.93 [+0.43, +1.43].
- v1.1 - humanizer, human-sounding: -0.61 [-1.18, -0.04].

**Pre-registered verdict: DIRECTIONAL.** The mean is positive and both guardrails pass (0.38 invented per text; fidelity -0.11), but the interval includes zero, so success was not demonstrated.

## What this says

1. **v1.2 is not shown to be better than v1.1.** The +0.3 gain is smaller than the judge noise I can see in the data: on the human-written Q08, v1.2 changed one punctuation mark and the judges' ranking of it swung from 1.0 to 3.0 against three character-identical texts.
2. **The fidelity gain from v1.1 survives a second fresh holdout.** v1.1 and v1.2 invent 0.2-0.4 specifics per text vs 4.0 for v1 and 1.0 for humanizer.
3. **v1 still wins human-sounding by a clear, significant margin on this set** (v1.2 is 0.96 below it), as in every round.
4. **Exploratory split, chosen after seeing the data.** On the three passages where v1 invented the most (Q01-Q03: the career post, the pep-talk essay, the launch email), human-sounding was v1 2.5, humanizer 1.7, v1.1 1.6, **v1.2 0.25**. On the four where v1 invented little (Q04-Q07), it was v1 2.0, **v1.2 2.0**, humanizer 1.5, v1.1 0.5. So the paragraph-level and sample-echo changes may have recovered voice where there is nothing to invent, while the pep-talk and call-to-action cuts may have hurt exactly the passages they target. These are confounded (four changes at once) and rest on 3 and 4 passages.
5. **A concrete v1.2 defect:** on Q03 it softened "Start your free trial today!" to "whenever you're ready", which the judges counted as a dropped call to action, against its own "keep a real call to action" rule.

## Caveats

Three holdout rounds now exist; each added evidence but none large. Seven scored passages, one sample each, Sonnet-generated, LLM-judged, no real detector or human readers. The invention-concentration split in point 4 is post hoc and the threshold is not sharp (v1 invented 3.8 on Q03 and 3.0 on Q05).

## Recommendation

Do not ship v1.2 as it stands: it missed the pre-registered success bar and the call-to-action cut is a real defect. v1.1 remains the release candidate (the fidelity fix is well supported across three test rounds; the voice cost relative to v1 is real but smaller than the fabrication it removes). If more voice work is wanted, test the four v1.2 changes one at a time rather than together, starting with paragraph-level restructuring and sample-echo, and drop the closer-cut rule or limit it to questions and slogans while keeping the draft's call-to-action wording.

---

# Part 5: v2.0 (research-driven upgrade on top of v1.1), tested on a third fresh holdout

Date: 2026-11-11. Branch `v2.0`. Frozen files and hashes: `v20-run/skills/`, `v20-run/FROZEN.sha256`. Pre-registration: `v20-run/prereg_v20.md`, written after the freeze and before the holdout existed. Tables: `v20-run/results_v20.txt`.

## What v2.0 adds to v1.1

A routing step (five draft types), reasoning-model handling (lead with the conclusion, drop deliberation markers, weight by what the draft concludes), paragraph-level restructuring and sample echo (from v1.2), "match the page it sits on", "do not sand it flat", a variant pass, a narrowed closer rule, and `scripts/check.py`.

## Method

Same as Part 4 with these differences. Holdout: 10 new passages (S01-S10), 9 scored; S08 is a human-style control. Two scored passages (S03, S10) are reasoning-model prose, which v2.0 targets and the other arms do not. Arms: v1, humanizer **2.5.1** (a local port; the 3.1.0 used in Parts 1-4 was no longer on disk, so this column is not comparable with earlier parts), v1.1, v2.0. Generation: Sonnet, one agent per arm per batch of five passages (earlier parts used one run per passage). Judging: blind 4-way, GPT and Gemini, two label orders; 39 of 40 judgments valid, 35 scored.

## Results

| Arm | Human-sounding (0-3) | Fidelity (0-3) | Wins | Invented specifics / text | P(AI) |
|---|---|---|---|---|---|
| write-human v1 | 1.26 | 0.57 | 3 | 2.31 | 25 |
| humanizer 2.5.1 | 1.34 | 0.57 | 2 | 1.54 | 24 |
| v1.1 | **1.86** | 2.31 | 15 | **0.14** | 27 |
| v2.0 | 1.54 | **2.54** | 15 | 0.17 | 29 |

Paired passage-level differences (mean, 90% bootstrap interval):
- v2.0 - v1.1, human-sounding: **-0.32 [-0.92, +0.28]**; fidelity +0.21 [-0.39, +0.74].
- Excluding S03 and S10: human-sounding -0.38 [-1.06, +0.32].
- v2.0 - v1: human-sounding +0.24 [-0.72, +1.19]; fidelity +1.95 [+1.37, +2.47].

**Pre-registered verdict: FAIL.** Guardrails pass (0.17 invented per text; fidelity not worse), but the mean human-sounding difference against v1.1 is negative. The interval includes zero, so v2.0 is not shown to be worse either; it is not shown to be better, which was the bar.

Mechanical check (`scripts/check.py` over the nine scored passages): flags per text v1 0.78, humanizer 0.44, v1.1 0.00, v2.0 0.00. Length against the draft: 0.87, 0.82, 0.75, 0.76. The control S08 came back character-identical from v1, humanizer and v2.0; v1.1 edited it.

## What this says

1. **The fidelity rules hold on a fourth holdout.** v1.1 and v2.0 invent about 0.15 specifics per text against 2.3 for v1, and share 30 of the 35 wins.
2. **v2.0's additions did not buy voice.** On six of the nine scored passages the v1.1 and v2.0 outputs are close to the same text.
3. **Judge noise is as large as the effect.** S05 and S04 are nearly word-for-word identical between the two arms, yet S05 scored 2.2 against 0.0 and S04 scored 1.5 against 3.0. Seven or nine passages cannot resolve a difference of a few tenths with this instrument.
4. **"Lead with the conclusion" changes what the text claims.** On S03 the judges found v2.0 more human-sounding (2.2 against 1.2) and less faithful (1.8 against 3.0): stating the recommendation first turned "the trial complicates this concern" into "the cost is outweighed", and added "the six extra hires are meant to fix that". On S10 it was worse on both counts (0.0 human-sounding): the hedged opening became a flat assertion and the piece ended on the counterpoint. Reordering an argument is not fidelity-neutral.
5. **Where v2.0 did better, n is one.** The passage inside a longer post (S06: 2.5 against 2.0, fidelity 3.0 against 2.0) and the untouched control.
6. **The closer rule is still contested.** On S01 v2.0 cut the "What dream are you putting off?" question; Codex listed it as a dropped fact in both orders, and Gemini preferred the v1.1 version that kept it.
7. **The generator never ran the checker.** Both v2.0 agents had a shell and the instruction, and neither ran `scripts/check.py`. As a step inside the skill it is optional in practice.

## Caveats

The holdout author also wrote v2.0. Batched generation, Sonnet only, LLM judges, no real detector, no human readers. One Gemini judgment missing. The humanizer arm is an older port.

## Recommendation

Do not publish v2.0 on the claim that it sounds more human than v1.1; the test does not support it. What the evidence does support shipping: the v1.1 instructions, the checker as a tool for the user rather than a workflow step, the light-touch route for human-written drafts, and the updated detector reference. The reasoning-model rule needs rewriting before it ships (remove markers and staged symmetry, keep the draft's order and its hedges), and that rewrite would be untested. This holdout is now seen and cannot be reused.

---

# Part 6: revised 2.0 (2026-11-12)

Run folder: `v21-run/`. Pre-registration: `v21-run/prereg_v21.md`, written after the freeze and
before the holdout. Raw table: `v21-run/results_v21.txt`.

**What changed after Part 5.** The reasoning-model rule no longer leads with the conclusion: it
keeps the draft's order of commitment and every hedge and condition. Rule zero says strength is
content. The audit asks whether any claim got stronger or weaker. The checker left the numbered
workflow.

**Design.** New holdout T01-T10: four passages inside a longer document, three reasoning-model
drafts with hedged conclusions, two ordinary drafts, one human-style control (unscored). Arms:
v1.1, frozen 2.0, revised 2.0. Sonnet generation, blind 3-way ranking (0-2), two label orders,
GPT and Gemini. 39 of 40 judgments valid (one GPT judgment on T05 failed twice). The GPT
judgments for T05-T10 were run a few hours after the rest, once the Codex workspace had
credits again; inputs and prompt were unchanged.

**Result (35 scored judgments, 9 passages).**

| | human-sounding (0-2) | fidelity (0-2) | wins | strength changes / text |
| --- | --- | --- | --- | --- |
| v1.1 | 1.06 | 0.63 | 4 | 1.29 |
| 2.0 frozen | 0.69 | 0.71 | 6 | 1.31 |
| 2.0 revised | 1.26 | 1.66 | 25 | 0.77 |

- Primary, revised minus v1.1 on human-sounding: +0.23 [-0.33, +0.78]. Pre-registered verdict:
  **DIRECTIONAL**. Guardrails pass (0.03 invented specifics per text; fidelity +1.04
  [+0.69, +1.32] against v1.1).
- Both judges put the revision first on fidelity (GPT 1.65, Gemini 1.67) and gave it the most
  wins (11 of 17, 14 of 18). On human-sounding they disagree: GPT has v1.1 marginally ahead
  (1.18 vs 1.12), Gemini has the revision ahead (0.94 vs 1.39).
- Reasoning passages (3 passages, 11 judgments): revised minus frozen 2.0 on fidelity +1.81
  [+1.69, +1.92]; revised minus v1.1 on human-sounding +0.94 [+0.44, +1.44]. Judges listed no
  strength changes for the revised arm in any judgment, against 1.82 per text for v1.1 and 1.36
  for frozen 2.0. The revision won all 11.
- Passage-in-document cases (4 passages, 16 judgments): revised minus v1.1 on human-sounding
  -0.25 [-1.00, +0.50]. Passage matching is not shown to help voice. Fidelity was better there
  (1.75 vs 0.81).
- Frozen 2.0 against v1.1 on human-sounding: -0.31 [-0.83, +0.26], repeating Part 5 (-0.32).
- Control T10: all three arms returned it unchanged.
- No generator ran the checker.

**Reading.** The fix did what it was written to do. On reasoning drafts the strengthened claims
are gone, and the sinking assumption (that the shape can stay and the text still read less
machine-made) held on three passages. Across all nine passages the revision is ahead of v1.1 on
fidelity with an interval clear of zero; whether it sounds more human than v1.1 is still not
shown. Passage matching, the other thing this round set out to strengthen, did not beat v1.1
on voice. Nine passages, one generation per arm, a holdout written by the skill's author.
