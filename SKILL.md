---
name: write-human
version: 1.0.0
description: >-
  Rewrite an existing draft so it reads like a person wrote it, not a model: natural rhythm,
  real voice, concrete detail, and none of the tells AI detectors flag. Use whenever writing
  "sounds like AI", "like ChatGPT", or reads robotic, stiff, corporate, or generic; when
  humanizing, de-slopping, or removing AI patterns (em dashes, "it's important to note", rule of
  three, buzzwords like "leverage" and "seamless"); when a human author keeps getting falsely
  flagged by a detector and wants to read human without changing their argument; or as the final
  voice pass on an article, blog post, essay, email, cover letter, landing page, LinkedIn post, or
  newsletter before it ships. Also: "make this sound human", "give it a real voice", "less
  corporate", "de-slop this", "fix the AI tells". Edits text you already have; does not
  generate from a blank prompt, score or detect whether text is AI, fix only grammar/typos,
  translate, or just make writing more formal.
license: MIT
metadata:
  author: Sarthhak Kaluucha
  tags: writing editing voice humanize ai-detection
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Write Human

You take a draft and rewrite it so it reads like a specific person actually wrote it. Two things happen at once: the writing stops tripping AI detectors, and it gets better to read. Those are the same job, which is the whole insight behind this skill.

## The one idea that makes this work

Most "humanizers" hand you a banned-word list and tell you to swap "delve" for "explore." That helps a little and misses the point. Word-swapping leaves the text flat, evenly paced, and opinion-free, which still flags as AI and now also reads worse.

Here is what detectors actually measure, and it is not "machine-ness." Recent work (see `reference/why-detectors-flag-text.md`) found that detectors classify the raw output of *base* language models as overwhelmingly human, while heavily penalizing *instruction-tuned* output. In plain terms: detectors are tracking the residue of RLHF training, the habits a model picks up from being made polite, balanced, evenly structured, and careful. They score two things above all:

- **Perplexity**: how predictable each next word is. AI takes the safest, most likely path every time, so the score stays unnaturally low. Humans surprise the reader.
- **Burstiness**: how much sentence length and structure vary across a passage. AI clusters tightly around an average. Humans swing from three-word fragments to long, winding clauses.

So the move is not "remove forbidden words." The move is: **rewrite so the text reads like a specific person continuing a thought, with opinions, uneven rhythm, and concrete detail.** That single shift raises perplexity and burstiness at the same time, and it is also exactly what makes writing land. Engaging and undetectable are the same target hit from two sides.

Hold that idea the whole way through. Every technique below is in service of it.

## When to use this

Editing or polishing any draft that "sounds like AI." De-slopping AI-assisted content before it ships. Rewriting prose that reads corporate, robotic, or hollow. Helping a non-native English writer who keeps getting falsely flagged. Use it as the last pass on articles, essays, emails, landing pages, social posts, and reports.

Not for: generating brand-new content from a blank page (this skill edits an existing draft), or for fact-checking (it changes voice, not truth, so keep the facts the author gave you).

If what you actually want is an exhaustive banned-word lint, with severity tiers, context profiles, and a flag-only mode, that is a different tool (the `avoid-ai-writing` skill). This one is the voice-and-rhythm method, not a word blacklist. The two pair well: rewrite here for voice, then run that as a final lint if you like.

## Workflow

### 1. Diagnose first (fast)

Read the draft once, ideally aloud in your head. Name the tells you hear in three to six quick bullets before you touch anything. This keeps the rewrite targeted instead of a vague "make it better." If you are unsure what to look for, open `reference/ai-tells.md`, which catalogs every pattern with a fix.

The fastest tells to listen for: every sentence the same length, no opinion anywhere, lists of exactly three, "It's important to note," em dashes doing a comma's job, a sweeping "In today's world" opener, and a tidy summary conclusion that adds nothing.

### 2. Rewrite in three layers

Do these together, not as separate passes, but it helps to know which lever you are pulling.

**Lexicon.** Replace the high-frequency AI vocabulary with plainer, context-specific words. Not mechanically, in context. "Delve into" becomes "dig into" or just "look at." "Underscores the importance of" becomes "shows" or "matters because." Kill transition padding outright: "It's worth noting that," "Furthermore," "Moreover," "Additionally." If a point is worth making, make it. The full tables with replacements live in `reference/ai-tells.md`.

**Structure.** Break the formulas. Reduce a rule-of-three list to two items or stretch it to an uneven four. Rewrite negative parallelisms ("it's not just X, it's Y") into direct statements. Put back the plain verbs the model avoided: "serves as a testament to" becomes "is." Delete synonym cycling (the protagonist, the main character, the central figure, the hero, all for one person) and use a pronoun. Fix the formatting tells: em dashes, mechanical boldface, emoji bullets, curly quotes, Title Case In Headings.

**Rhythm.** This is the burstiness lever and it is underused. Make sure no three consecutive sentences share the same length or cadence. Cut one sentence to a fragment. Fuse two into a long one with a subordinate clause. Vary paragraph length too: same-length paragraphs scream AI. Read it back. If the meter is even and marching, break it.

### 3. Re-voice (the part most editors skip)

A draft can be technically clean and still obviously synthetic because there is no person in it. This step adds the person.

React, don't just report. "I genuinely don't know how to feel about this" beats a neutral pros-and-cons list. Admit mixed feelings and uncertainty, which models are trained out of. Use "I" where it fits, because first person is honest, not unprofessional. Trade vague claims for specific detail: a named example, a real number, an anecdote. Delete the cliché opener and write a real one (a direct challenge, a concrete result, a confession, a small scene). Delete the summary conclusion; end on the sharpest concrete thing you have.

For the craft of making the rewrite genuinely engaging (headlines, openings, quantifying the pain, the "so what" chain, open loops, testimonials), pull `reference/craft-levers.md`. These turn a de-AI'd draft into one that actually pulls the reader forward.

**Calibrate to the register.** The target is "a person wrote this," not "a casual person wrote this." An engineer documenting an API, a lawyer drafting a brief, a researcher writing an abstract: each has a real voice that is legitimately formal and reserved. For those, the human signal comes from a clear point of view, concrete detail, and varied rhythm, not from forcing in an "I" or a chatty aside. Match the voice of a competent human writing in that genre, then make sure that voice is actually present. Do not strip justified formality in the name of sounding human; that just trades one kind of off-ness for another.

### 4. Adversarial self-audit

This catches the tells you missed. After your rewrite, run two prompts on yourself:

1. "What still makes this read as AI-generated?" Answer honestly in a few bullets. There is almost always something: rhythm a touch too tidy, a contrast that is too clean, a closer that went slogan-y, placeholder-sounding specifics.
2. "Now fix exactly those." Revise and present the result.

This two-step is the single highest-value habit in the skill. Do not skip it.

### 5. Read it aloud

The strongest test there is. If a sentence sounds like a textbook, a press release, or a chatbot being helpful, rewrite it until it sounds like a person. Calibrate "a person" to the genre: a person talking, a person briefing a client, a person writing a careful technical note. The test is whether a real human in that role would actually write the sentence, not whether it sounds casual. The fundamentals of good writing have not changed in a hundred years. The packaging just has to sound like a human made it.

## Output format

Unless the user asks for just the final text, present:

1. **Diagnosis**: 3 to 6 bullets naming the tells you found.
2. **Rewrite**: the humanized draft.
3. **Self-audit**: "What still reads as AI?" answered in a few honest bullets.
4. **Final**: the revised version after the audit.
5. **(Optional)** a short list of the main changes, only if it helps the user learn the pattern.

If the user asks for "just the text," "only the rewrite," or "skip the working," give them the final version alone and offer the diagnosis if they want it. Still run the self-audit pass internally, even when you do not show it; it is what makes the final draft better than the first rewrite.

## Honesty and limits

Be straight with users about what this does. It changes surface stylometry, the things a statistical detector measures. It does not, and cannot reliably, remove a hard cryptographic watermark like Google's SynthID, which is embedded in the generation itself. Do not promise a guaranteed "0% AI" score; detectors are probabilistic and inconsistent, and the same text scores differently across tools.

The honest use of this skill is to write genuinely human, well-made prose: the kind that does not deserve to be falsely flagged and actually reads well. AI detectors have a documented bias against non-native English speakers (one Stanford study had seven detectors falsely flag 61% of TOEFL essays written by humans) and against tightly structured technical writing. Helping a real author sound like themselves is the point. Helping someone pass off unread, unedited model output as their own original work, in a context that forbids it, is not, and you should gently steer away from that framing if it comes up.

## Reference files

Read these as needed; they are not all loaded up front.

- `reference/why-detectors-flag-text.md`: how detection actually works (perplexity, burstiness, Fano factor, type-token ratio, nominal loading), the base-model insight, the false-positive crisis, and the watermarking caveat. Read it when you want the why or need to explain detection to a user.
- `reference/ai-tells.md`: the complete pattern catalog. Lexicon tables with frequency data and replacements, transition padding, structural tells, formatting tells, and chatbot artifacts, each with a before and after. This is your working reference during a rewrite.
- `reference/craft-levers.md`: the craft of engaging prose. Headlines, openings, pain quantification, the "so what" chain, rhythm, open loops, testimonials. Pull this when the goal is not just "not-AI" but "actually good."
- `examples/before-after.md`: full worked rewrites across marketing, technical, and essay registers, plus a falsely-flagged non-native-English passage (the skill's central use case), each showing diagnosis and the self-audit pass.

## A compact example

**Before:**
> In today's rapidly evolving digital landscape, leveraging AI tools has become a pivotal strategy for businesses. It's important to note that these solutions not only streamline workflows but also foster innovation, enhancing productivity across teams.

**Diagnosis:** sweeping "today's landscape" opener, AI lexicon ("leveraging," "pivotal," "streamline," "foster," "enhancing"), negative parallelism ("not only X but also Y"), transition padding ("It's important to note"), even rhythm, zero voice or specifics.

**After:**
> Most teams I talk to bought an AI tool last year and still can't tell you what it changed. The ones who can usually point to something small and concrete: a support team that stopped writing the same three replies forty times a day. That is the whole game. Not "innovation," just fewer hours lost to work nobody wanted to do.

Shorter and longer sentences mixed, a real opinion, a specific scene, the buzzwords gone, and a person clearly behind it.
