# Pre-registration: v1.2 test (written 2026-10-24 12:42 local, before any v1.2 output exists)

Frozen v1.2 hashes: see skills/v12/FROZEN.sha256 (SKILL.md 0644e0ff7daf...).
Holdout: 8 new passages Q01-Q08, written after v1.2 was frozen, never shown to any arm's design.
Arms: write-human v1, humanizer, v1.1, v1.2 (baseline and v2 dropped). 4-way blind ranking, scores 0-3, 2 label orders, 2 judge families.
Q08 is a human-written control and is excluded from scored totals.

Primary question: is v1.2 more human-sounding than v1.1?
- SUCCESS: mean passage-level human-sounding difference (v1.2 minus v1.1) > 0 and a 90% passage-bootstrap interval excludes 0.
- DIRECTIONAL: mean > 0 but the interval includes 0.
- FAIL: mean <= 0.
Guardrails (must hold or v1.2 fails regardless): invented specifics per text <= 0.5; mean fidelity rank not worse than v1.1 by more than 0.3.
Secondary (reported, not decisive): v1.2 vs v1 and vs humanizer on human-sounding, fidelity, wins, P(AI).
