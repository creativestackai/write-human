# Why detectors flag text

Read this when you want to understand *why* a rewrite works, or when you need to explain detection to a user. You do not need it to do a rewrite; the techniques in `ai-tells.md` stand on their own. But knowing the mechanics tells you which edits matter most and stops you from cargo-culting fixes that do nothing.

## Table of contents

1. The core: next-token prediction leaves a signature
2. Perplexity (predictability)
3. Burstiness and the Fano factor (rhythm)
4. Type-token ratio and nominal loading (vocabulary)
5. The strategic key: detectors track instruction-tuning, not "machine-ness"
6. What the commercial detectors actually do
7. The 2025-26 detectors, and what a rewrite can and cannot do about them
8. The false-positive crisis (why this is a real problem, not cheating)
9. Watermarking: the thing you cannot edit away
10. What this means for how you rewrite

## 1. The core

A language model writes by predicting the most probable next word, over and over. That objective leaves a statistical fingerprint. The text is too smooth, too safe, too evenly built, because at every step the model took the high-probability path. Human cognition does not work that way. We get distracted, change our minds mid-sentence, reach for an odd word, and follow a tangent. Detectors are built to spot the smoothness.

Almost every technique that humanizes text is really doing one thing: putting the unpredictability back.

## 2. Perplexity

Perplexity measures how "surprised" a reference model is by each word in a sequence. Low perplexity means the text was easy to predict. Because models optimize for the most likely continuation, their output sits at unnaturally low perplexity for hundreds of words at a stretch, and that consistency is itself the flag.

A human writer spikes the perplexity constantly: an unexpected metaphor, a culturally specific reference, a blunt aside, a word choice no model would rank first. You do not raise perplexity by adding rare words at random (that reads as thesaurus abuse and detectors catch it too). You raise it by writing with a real point of view, because opinions and specifics are inherently less predictable than balanced summary.

## 3. Burstiness and the Fano factor

Burstiness is variation in sentence length and structure across a passage. Human writing is bursty: a four-word sentence slammed against a forty-word one, a fragment, then a complex multi-clause thought. AI writing is homogeneous, with sentence lengths clustered tightly around a mean and a repeated topic-sentence-then-support-then-tidy-close shape.

Computational linguists quantify this with the Fano factor, the variance of sentence lengths divided by the mean. Low Fano factor reads as artificial uniformity, and it is the second pillar (with perplexity) of detectors like GPTZero and Originality.ai.

This is the most actionable detection fact in the whole report. You can directly attack it. Make sure no three consecutive sentences share the same length or cadence. Cut one to a fragment, fuse two into a long one. Vary paragraph length the same way. This single habit moves the burstiness number more than any word swap.

## 4. Type-token ratio and nominal loading

Type-token ratio (TTR) is unique words divided by total words, a rough measure of lexical diversity. AI tends to run a lower TTR than a skilled human writer.

More telling is "nominal loading": AI prose is noun-heavy and adjective-heavy, leaning on abstract nouns and cohesive devices instead of varied verbs and natural pronoun reference. Part-of-speech analysis flags this even when the grammar is flawless. The fix is to convert heavy noun phrases into active verbs ("the implementation of the optimization" becomes "we optimized it") and to let pronouns do their job instead of cycling synonyms.

## 5. The strategic key: detectors track instruction-tuning

This is the most important finding for your purposes, so it gets its own section.

Researchers showed that AI detectors classify the raw output of *base* models (pre-trained only, never fine-tuned to be a helpful assistant) as overwhelmingly human, while heavily flagging *instruction-tuned* models. The detectors are not really detecting "a machine wrote this." They are detecting the artifacts of RLHF and instruction-tuning: the politeness, the balance, the hedging, the tidy structure, the eagerness to be comprehensive and neutral.

That reframes the entire task. You are not scrubbing away "machine-ness." You are removing the assistant's training: the reflex to be even-handed, to cover all angles, to hedge every claim, to organize everything into clean parallel lists, to never have an opinion. A base model rambling with a clear voice reads as human. So write like that. Take the position the author holds. Be uneven. Say "I think" where the author does. (Rule zero in `SKILL.md` still governs: the opinions and the facts are the author's, never yours.)

The strongest form of this fix is not an edit at all. Because a base model has none of the assistant habits, its raw output reads as human to classifiers — so passing a draft through one strips the polish an edit can only trim. The technique is Humanization by Iterative Paraphrasing (HIP): paraphrase through a non-instruction-tuned model (a base Llama or Qwen) in short chunks, two or three passes. The output is loose and unvoiced, so it still needs the voice pass from `SKILL.md` step 3, and it still must keep the draft's facts (rule zero). Full recipe in `SKILL.md`, "The deepest lever, when it is available."

## 6. What the commercial detectors actually do

Useful context so you can set expectations honestly.

- **Turnitin**: trained on academic student writing, processes text in 250-word overlapping chunks, and deliberately suppresses scores under 20% to keep false positives low (around 1 to 3%). Conservative.
- **GPTZero**: leans on perplexity and burstiness plus a classifier, highlights sentence by sentence, runs more aggressive than Turnitin with somewhat higher false positives.
- **Originality.ai**: the most aggressive, tuned for SEO and publishers, built to catch paraphrased text, and accepting a 5 to 9% false-positive rate as the cost.
- **Copyleaks**: enterprise, semantics plus perplexity, conservative on false positives.

The practical takeaway: the same text scores differently on each. "Passing" one is not passing all. Never promise a specific score.

## 7. The 2025-26 detectors

Perplexity and burstiness scanners are the first generation. Newer systems measure other things, and it is worth knowing which, because it changes what an honest rewrite can claim. Figures below are the authors' own reported results, not independent tests.

| Detector | What it reads | What that means for a rewrite |
| --- | --- | --- |
| **RepreGuard** (TACL 2025, arXiv 2508.13152) | The internal activation pattern a reference model produces while reading the text. Reports about 95% AUROC out of distribution, and robustness to paraphrasing. | Nothing at the word level reaches it. Only text that is actually built differently (structure, content, voice) reads differently. |
| **Exons-Detect** (ACL 2026) | A small set of high-signal tokens, found through hidden-state differences between two models, then amplified. | Swapping the flagged word for a synonym leaves the sentence's construction, and the signal, in place. Rebuild the sentence. |
| **AdaDetectGPT** (NeurIPS 2025, arXiv 2510.01268) | Token probabilities, with a learned scoring function and statistical error guarantees. | A sturdier version of the perplexity idea. Same remedy as section 2: a real point of view, not rare words. |
| **GigaCheck** (Findings of ACL 2026, arXiv 2410.23728) | Treats generated passages as objects to locate, and draws character spans around them inside a mixed document. | A passage whose voice differs from the page around it stands out. An author's document should hold one voice, theirs. |
| **Pangram 4** (2026) | A learned map of writing styles in which the major assistants occupy known regions; flags documents whose passages point to different regions. | Generic "clean" prose sits where the assistants sit. A writer's own habits, taken from their own sample, sit somewhere else. |
| **Agentic detectors** (Cui et al., Findings of EMNLP 2026) | An LLM agent that combines several detectors with web search and reasons about where the text's content came from. | Style is only part of the evidence. Content the author actually supplied, sourced and specific, is what holds up. |
| **GECScore** (COLING 2025, arXiv 2405.04286) | Runs a grammar corrector and measures how little it had to change. Humans leave more for it to fix. Reports about 98.6% AUROC. | Do not over-correct a human draft (`ai-tells.md` section 13). Do not plant errors either. |

Three practical conclusions.

**Word swaps are finished.** They were the smallest lever in section 10 already; against detectors that read structure and representation, they are no lever at all.

**The remedies that still work are the ones that make writing better.** Paragraphs rebuilt around the author's point, one consistent voice taken from the author's own writing, the author's real specifics, and their natural irregularities left in. That is the whole workflow in `SKILL.md`, and it is no coincidence: each of these detectors is, in its own way, measuring how generic the text is.

**No rewrite can promise a result.** Several of these systems were designed to survive paraphrasing and report that they do. A skill that edits style has no access to hidden states or search results, and no way to test against them. Anyone promising to beat them is guessing.

A note on reasoning models. Drafts from "thinking" models are often described as having their own signature: proof-shaped paragraphs, deliberation phrases, both sides at equal length. As far as we can find, that description comes from detector vendors' blogs, not from peer-reviewed work. The patterns are still real editorial problems and `ai-tells.md` section 11 covers them, as craft, without detection claims attached.

## 8. The false-positive crisis

This matters because it is the honest reason this skill should exist.

Detection is biased against people who did nothing wrong. A Stanford study ran 91 TOEFL essays, all written by human non-native English speakers, through seven detectors. They falsely flagged 61% of them as AI, and in nearly 20% of cases all seven agreed, unanimously wrong. Native-speaker eighth-grade essays were classified correctly almost every time.

The mechanism is structural. Non-native writers use a narrower vocabulary, simpler syntax, and more standard grammar as they aim for correctness. That profile is mathematically close to a model's safe, standard output, so the scanner cannot tell them apart. The same penalty hits law, medicine, engineering, and technical writing, where precise, templated, low-entropy prose is the professional norm. Some institutions, including Vanderbilt, have turned the detectors off over exactly this.

So a large share of "AI-flagged" text was written by humans whose only crime was writing clearly in a second language or a structured field. Helping those writers add the rhythm and voice that proves their humanity is legitimate and good. Keep that framing front and center.

## 9. Watermarking: the thing you cannot edit away

Be honest about the ceiling. The industry is moving from after-the-fact detection toward watermarking baked into generation. Google DeepMind's SynthID-Text biases the model's sampling (via "tournament sampling" seeded by a secret key) so the output carries a statistical signature that survives light paraphrasing, translation, and copy-paste, while reading identically to a human.

Newer schemes go further: public-key designs such as DHMark (arXiv 2608.03093) let a third party verify the mark without holding the secret, and semantic-level schemes such as PMark (arXiv 2509.21057) tie it to sentence meaning rather than word choice.

Surface humanization does not reliably remove a hard watermark. Aggressive enough attacks can degrade the signal, but usually only by degrading the text into unreadability. This skill rewrites stylometry; it does not touch cryptographic provenance. If a user is up against a watermark, tell them the truth: the fix is to actually rewrite the substance themselves, not to run a humanizer. This skill does not attempt reordering or resegmentation tricks aimed at breaking a watermark, and will not.

## 10. What this means for how you rewrite

Everything above collapses into a short priority list. One move outranks even the list, when it is available: if you can generate rather than edit, start from a base-model paraphrase (HIP, section 5) and then apply the priorities below on top. Otherwise:

1. **Put back the variance.** Uneven sentence and paragraph length attacks burstiness, the most measurable flag. Highest leverage.
2. **Put back a point of view.** The author's opinions, the draft's own specifics, and a real voice raise perplexity and erase the instruction-tuned smoothness. The deepest fix.
3. **Strip the instruction-tuned habits.** Hedging, balance-for-its-own-sake, tidy parallel structure, comprehensive coverage. These are what the detector is really keyed to.
4. **Keep one voice per document.** Match the author's sample, or the page the passage sits on.
5. **Leave the author's slack in.** Fragments, contractions, habits of punctuation. Do not sand a human draft flat, and never plant an error.
6. **Then clean the lexicon and formatting.** Word swaps and punctuation fixes matter, but they are the smallest lever. Do them, do not stop there.

All of it sits under one rule that outranks detection entirely: the rewrite says only what the draft said.

Word-swapping alone is the classic mistake: it produces flat, low-burstiness, voiceless prose that still flags, and now reads worse. Rhythm and voice are the real work.
