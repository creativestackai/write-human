# Pre-registration: v2.0 test

Written 2026-11-11, after v2.0 was frozen (hashes in FROZEN.sha256) and before any holdout
passage or any v2.0 output on it existed.

Holdout: 10 new passages S01-S10, written after the freeze. S08 is a human-style control
(do-no-harm) and is excluded from scored totals, leaving 9 scored passages. Two of the nine
(S03, S10) are reasoning-model prose, a case v2.0 was built for and the other arms were not;
results are reported with and without them. The holdout author also wrote v2.0.

Arms: write-human v1 (main, 1.0.2), humanizer (2.5.1 Hermes port found on this machine; NOT
the 3.1.0 used in earlier rounds), v1.1 (v11-run/snapshot), v2.0 (skills/v20, including
scripts/check.py, which the generator may run because the skill tells it to).
Generation: Sonnet, neutral task prompt "Rewrite this so it reads like a person wrote it,
not an AI." One agent per arm per batch of five passages (earlier rounds used one run per
passage; this is a cost deviation).
Judging: blind 4-way ranking, scores 0-3, two label orders, two judge families (GPT via
Codex, Gemini via Antigravity). Same judge prompt as v12-run/instr4.py.

Primary question: is v2.0 more human-sounding than v1.1, the release candidate it replaces?
- SUCCESS: mean passage-level human-sounding difference (v2.0 minus v1.1) > 0 and the 90%
  passage-bootstrap interval excludes 0.
- DIRECTIONAL: mean > 0 but the interval includes 0.
- FAIL: mean <= 0.
Guardrails (must hold or v2.0 fails regardless): judge-listed invented specifics per text
<= 0.5; mean fidelity rank not worse than v1.1 by more than 0.3.

Secondary (reported, not decisive): v2.0 vs v1 and vs humanizer on human-sounding, fidelity,
wins, P(AI); the primary difference excluding S03 and S10; length ratio and checker flags
per arm from scripts/check.py; whether S08 comes back unchanged.
