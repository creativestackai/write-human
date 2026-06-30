# Contributing

Thanks for helping make `write-human` better. The skill lives or dies on two
things: it triggers when it should, and its rewrites actually read human. Most
useful contributions touch one of those.

## Ways to help

### Report a bad trigger

If the skill fires when it shouldn't (you asked to translate, proofread, or
write from scratch and it tried to humanize), or fails to fire when it should,
open an issue. Include the exact prompt you used and what you expected. Trigger
tuning is ongoing, and real misses are the best signal.

### Propose a new tell

If you have an AI pattern the catalog misses, open an issue or PR against
`reference/ai-tells.md`. Strong proposals include:

- The pattern, with a real before/after example.
- Why it reads as AI (rhythm, register, instruction-tuning residue, a specific
  lexical habit).
- Frequency evidence if you have it (how much more often it shows up in model
  text than human text). Evidence beats opinion.

Keep the bar high. The skill's whole premise is that a longer banned-word list
is not the answer. New entries should earn their place by being genuinely
diagnostic, not just words someone dislikes.

### Improve an example or the science

Better worked rewrites in `examples/`, or corrections and citations for
`reference/why-detectors-flag-text.md`, are welcome. For the detection science,
cite the source.

## Running the trigger eval

The `evals/` folder holds a 20-query set (10 should-trigger, 10 should-not) and
notes in `OPTIMIZING.md`. If you change the `description` in `SKILL.md`, re-run
the eval before opening the PR and report the score. The goal is to catch
near-misses like "make this more formal" or "translate this" without losing the
real humanize triggers.

## Style

This is a humanizer skill. Its own prose should pass its own test. Keep the docs
concrete, varied in rhythm, and free of the tells the skill flags. If a sentence
sounds like a chatbot being helpful, rewrite it.

## License

By contributing you agree your work is licensed under the repo's
[MIT License](LICENSE).
