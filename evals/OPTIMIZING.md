# Tuning the trigger description

The `description` field in `SKILL.md` is what decides whether Claude reaches for this skill. This folder holds a 20-query eval set (`trigger-eval.json`) and the notes from one tuning pass.

## What changed and why

The first description had good recall (it fired on the cases it should) but invited false positives on near-miss requests that share keywords. The fixes:

- **Said "an existing draft" and added a hard exclusion line.** The original listed surfaces like "article, blog post, report," which risked firing on "write me a blog post" (generation, which this skill does not do). The description now ends with what the skill is *not* for: generating from a blank prompt, scoring or detecting AI, fixing only grammar or typos, translating, or just making text more formal.
- **Led with the symptoms users actually type** ("sounds like AI," "robotic," "stiff," "generic," "reads corporate") and named concrete tells ("em dashes," "it's important to note," "leverage," "seamless") so the match is about voice, not about the word "edit."
- **Kept the false-positive (falsely-flagged author) case explicit**, since that is a primary honest use.

## The eval set

`trigger-eval.json` has 10 should-trigger queries and 10 should-not. The negatives are deliberately tricky near-misses (proofread for grammar, "is this AI? give a percentage," refactor code, make an email more formal, translate, summarize, design a logo that "feels human"). Easy negatives test nothing.

## Hand-judged result

This pass was judged by hand, because the automated loop needs a logged-in `claude` CLI and the environment it was built in was not authenticated. Reasoning each query against the new description: all 10 positives match on symptom or named tell; all 10 negatives are now caught by either the "existing draft / does not generate" framing or the explicit exclusion line (grammar-only, detection/scoring, translation, formality-only). Predicted score 20/20. Treat that as a strong hypothesis to confirm with the real loop, not a measured number.

## Run the automated loop yourself (recommended before publishing)

In a logged-in Claude Code, from the `skill-creator` skill directory:

```bash
python -m scripts.run_loop \
  --eval-set /path/to/write-human/evals/trigger-eval.json \
  --skill-path /path/to/write-human \
  --model <your-session-model-id> \
  --max-iterations 5 \
  --runs-per-query 3 \
  --verbose
```

It splits the set 60/40 train/test, runs each query three times to get a stable trigger rate, proposes description improvements based on failures, and re-tests. It selects the winner by held-out test score to avoid overfitting, and prints `best_description`. If that beats the current description, paste it into `SKILL.md`. Requires the `claude` CLI to be authenticated (`claude` then `/login`), since the loop launches `claude -p` for every query.
