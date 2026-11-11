# The AI tells catalog

Your working reference during a rewrite. Each pattern has a why and a fix. The patterns are ordered by how strongly they give text away, roughly. Lexicon and formatting are easy wins; structure, rhythm, and voice are where the real work is (see `why-detectors-flag-text.md` for why).

Do not apply these as a find-and-replace. Swapping words off a list mechanically produces flat prose that still flags. Read the sentence, understand what it is trying to say, and rewrite it the way a person who cared would.

## Table of contents

1. The high-frequency AI lexicon
2. Transition padding and hedged openers
3. Significance inflation and promotional tone
4. Vague attribution and notability puffery
5. Structural tells (rule of three, negative parallelism, copula avoidance, synonym cycling, false ranges)
6. Manufactured-insight hooks and cliche openers
7. Superficial "-ing" tails
8. Formatting tells (em dash, boldface, lists, title case, emoji, curly quotes)
9. Chatbot artifacts, disclaimers, sycophancy
10. Filler and hedging phrases
11. Reasoning-model tells (the argument's shape)
12. Slogan closers and comment bait
13. Over-polish (what not to fix)
14. A scannable trigger word list

---

## 1. The high-frequency AI lexicon

These words appear far more often in post-2023 model text than in human writing. The multipliers are approximate figures from frequency studies; treat them as "this one is a loud tell" rather than exact science. They also tend to cluster: where you find one, you find three.

| AI word or phrase | How much louder | Plainer human swap |
| --- | --- | --- |
| delve (into) | ~48x | dig into, look at, get into, examine |
| underscore / highlight (as verbs) | ~53x | show, point to, stress, matters because |
| tapestry (figurative) | ~35x | mix, web, blend, range |
| multifaceted | ~28x | complex, has many sides, layered |
| nuanced | ~22x | subtle, careful, fine-grained, it depends |
| foster / elevate | ~14 to 20x | build, encourage, grow, lift, improve |
| landscape (figurative) | ~19x | field, market, space, world, scene |
| pivotal | ~16x | key, central, decisive, the turning point |
| streamline / facilitate | ~10 to 11x | simplify, speed up, help, ease |
| garner | high | get, attract, win, collect |
| leverage (as a verb) | high | use, apply, draw on, put to work |
| utilize | high | use |
| robust | high | strong, solid, reliable, holds up |
| seamless / seamlessly | high | smooth, easy, no friction, just works |
| intricate / intricacies | high | detailed, complicated, the fine print |
| testament (a testament to) | high | shows, proof of, says a lot about |
| realm (in the realm of) | high | area, field, world of, when it comes to |
| myriad / plethora | high | many, lots of, a pile of, countless |
| crucial / vital / essential (stacked) | high | important, needed, or just cut it |
| navigate (figurative) | high | handle, deal with, work through, get through |
| harness | high | use, tap, put to work |
| unlock / unleash | high | open up, free up, let you, make possible |
| game-changer / transformative | high | a real shift, it changes the math, big deal |
| comprehensive / holistic | high | full, complete, covers everything, whole |
| vibrant / rich (figurative) | high | lively, busy, full, deep |

Rule of thumb: if a verb sounds like it belongs in a strategy deck, it is probably a tell. The plainest accurate word almost always reads more human.

---

## 2. Transition padding and hedged openers

Models bolt on logical-connective phrases to sound balanced and careful. Humans rarely use these at the same density. Most can be deleted with no loss.

| Padding phrase | Frequency vs human | Fix |
| --- | --- | --- |
| It's worth noting that | ~31x | delete; if it is worth noting, just note it |
| It is important to understand / note that | ~20x | delete |
| Furthermore | ~15x | delete, or start the sentence with the actual point |
| Moreover | ~14x | delete |
| Additionally | ~12x | delete, or "also," or just the next sentence |
| Broadly speaking / In general | high | delete |
| When it comes to | high | delete; rewrite "When it comes to pricing, we..." as "Our pricing..." |
| In order to | high | "to" |
| Needless to say | high | then do not say it |

The test: read the sentence without the opener. If it still works, and it almost always does, the opener was padding.

---

## 3. Significance inflation and promotional tone

Models puff up importance and slip into brochure voice, especially on culture, places, and history.

**Words to watch:** stands/serves as, a testament/reminder, a vital/crucial/pivotal role, underscores its significance, reflects broader, marking a shift, evolving landscape, boasts, nestled, in the heart of, breathtaking, renowned, must-visit, stunning, groundbreaking, rich heritage, natural beauty.

**Before:**
> Nestled in the breathtaking region of Gonder, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty, marking a pivotal chapter in the region's evolving story.

**After:**
> Alamata Raya Kobo is a town in the Gonder region.

The fix is almost always to state the plain fact and cut the adjectives. If the draft itself names a specific (a market, a church, a date), keep it; if it does not, the plain sentence is the whole answer. Do not supply a specific to replace the praise.

---

## 4. Vague attribution and notability puffery

Models attribute opinions to nobody in particular, and pile up proof of importance without context.

**Watch:** experts argue, observers have noted, industry reports suggest, studies show (with no study named), critics say, has been featured in [list of outlets], maintains an active social media presence, widely regarded as.

**Before:**
> Experts believe the river plays a crucial role in the ecosystem. Her work has been cited in The New York Times, BBC, and Financial Times, and she has a strong social media following.

**After:**
> The river matters to the ecosystem. Her work has been cited in The New York Times, the BBC, and the Financial Times, and she has a large following on social media.

Name the source if the draft names it; otherwise cut the unsupported claim ("experts believe") or reduce it to what the draft actually says. Never supply a source, a survey, or a quote the draft did not contain. One real citation beats a list of logos, and a missing one is better than an invented one.

---

## 5. Structural tells

These are the deep ones. They survive word-swapping, and they are what makes "clean" text still read as synthetic.

### Rule of three

Models force ideas into triads to feel comprehensive, even when two or four is the honest count.

**Before:** The event offers keynotes, panels, and networking, delivering innovation, inspiration, and insight.
**After:** The event has talks and panels, plus networking.

Fix: cut to two, or stretch to an uneven four, or just say the real number of things.

### Negative parallelism

"It's not just X, it's Y." "Not merely a tool, but a movement." Humans use this once, for real emphasis. Models use it as a tic.

**Before:** It's not just about the beat under the vocals; it's about the whole aggression of the track.
**After:** The heavy beat is what makes the track feel aggressive.

### Copula avoidance

Models dodge plain "is/are/was/were" in favor of inflated verbs: serves as, stands as, represents, embodies, functions as, acts as.

**Before:** The museum serves as a vital testament to the region's cultural landscape.
**After:** The museum documents the region's culture.

Put "is" back. It strips the pretension instantly.

### Elegant variation (synonym cycling)

Models have anti-repetition code, so they swap synonyms for the same noun in consecutive sentences instead of using a pronoun.

**Before:** The protagonist faces a choice. The main character hesitates. The central figure decides. The hero leaves.
**After:** The protagonist hesitates, then decides to leave.

Fix: pick one noun, then use "she/he/it/they."

### False ranges

"From X to Y" where X and Y are not on any real scale.

**Before:** Our journey spans from the birth of stars to the dance of dark matter, from the Big Bang to the cosmic web.
**After:** The book covers the Big Bang, how stars form, and current ideas about dark matter.

---

## 6. Manufactured-insight hooks and cliche openers

Two failure modes at the start of a piece.

**Sweeping generalization openers:** "In today's fast-paced digital landscape," "As the world continues to evolve," "In an era where," "Throughout history." These say nothing. Delete and open on something concrete: a fact, a number, a scene, a claim.

**Fake-edge hooks** (when a model is told to write "engaging" or "viral"): "But here's the truth," "The result?", "Then I realized," "Hot take:", "Let that sink in," "Plot twist:". They simulate insight on a predictable schedule, which is exactly why they read as fake. Cut them and let the actual point carry the weight.

**Before:** In today's fast-paced world, productivity is everything. But here's the truth: most advice is wrong. Let that sink in.
**After:** Most productivity advice is wrong.

Stop there. Do not grow the cut sentence into a new argument that the draft never made.

---

## 7. Superficial "-ing" tails

Models tack a present-participle clause onto a sentence to fake depth: highlighting, underscoring, reflecting, symbolizing, ensuring, showcasing, fostering, contributing to, emphasizing.

**Before:** The temple uses blue and gold, reflecting the community's deep connection to the land and symbolizing its enduring heritage.
**After:** The temple uses blue and gold.

Fix: if the "-ing" tail carries a real fact the draft supports, turn it into its own plain sentence. If it is just decoration, delete it. Do not replace the tail with a new explanation or a quote from someone.

---

## 8. Formatting tells

Surface, but instant giveaways, and the easiest to fix.

**Em dash overuse.** Models scatter em dashes (—) to fake punchy rhythm, often where a comma, period, or parenthesis belongs.
Before: The term is promoted by institutions—not the people—yet it persists—even officially.
After: The term is promoted by institutions, not the people, yet it persists even in official use.

**Mechanical boldface.** Bolding key phrases in every sentence or bolding the lead-in of every list item.
Before: It blends **OKRs**, **KPIs**, and the **Balanced Scorecard**.
After: It blends OKRs, KPIs, and the Balanced Scorecard.

**Inline-header vertical lists.** Every bullet starts with a bolded label and a colon, turning prose into a database.
Before:
> - **Performance:** Load times improved.
> - **Security:** Encryption was added.
After: The update speeds up load times and adds end-to-end encryption.
(Often the right fix is to dissolve the list back into a sentence or two.)

**Title Case In Headings.** Models capitalize Every Major Word. Humans usually write sentence case. Fix: "Strategic negotiations and partnerships."

**Decorative emoji.** 🚀 ✅ 💡 leading headings or bullets. Delete them unless the platform and voice genuinely call for it.

**Curly quotes and apostrophes.** ChatGPT emits typographic quotes ("..." and ') where a person typing would often produce straight ones. Match whatever the rest of the document uses; if in doubt for plain text, use straight quotes.

---

## 9. Chatbot artifacts, disclaimers, sycophancy

Residue from the assistant being an assistant. Always delete from published text.

**Conversational wrappers:** "Sure! Here's...", "Certainly!", "I hope this helps!", "Let me know if you'd like...", "Great question!", "Of course!", "Here is an overview of..."

**Knowledge-cutoff disclaimers:** "As of my last update," "While specific details are limited," "based on available information," "I don't have access to."
Before: While specific details about the founding are scarce, it appears the company began sometime in the 1990s.
After: The company's founding date is not given in the available sources. (Or cut the sentence. Never fill the gap with a plausible date or source.)

**Sycophancy:** "You're absolutely right!", "That's an excellent point," "What a fascinating topic." Cut it. State the substance.

---

## 10. Filler and hedging phrases

Tighten these on sight.

- "In order to achieve this goal" to "To do this"
- "Due to the fact that" to "Because"
- "At this point in time" to "Now"
- "In the event that" to "If"
- "Has the ability to" to "can"
- "It is important to note that the data shows" to "The data shows"
- "A wide variety of" to "many" or a number
- "Plays a key role in" to a plain verb ("shapes," "drives," "decides")

**Excessive hedging stacks:** "It could potentially possibly be argued that this might have some effect." Real writers commit. "This probably affects outcomes," or "I think this affects outcomes, though I am not certain." One hedge, not four. And note: an honest "I am not sure" reads far more human than a stack of soft qualifiers, because models are trained to hedge and trained away from admitting plain uncertainty.

**Generic upbeat conclusions:** "The future looks bright. Exciting times lie ahead on this journey toward excellence." Cut entirely. End on the most concrete thing the draft contains, even if it is small (a stated plan, a last fact). If it has none, just end earlier.

---

## 11. Reasoning-model tells (the argument's shape)

Drafts from "thinking" models often carry few of the buzzwords above and still read as machine-made. The giveaway moved from the words to the shape of the argument. This section is an editor's observation, not a published finding: the patterns are easy to see once named, but nobody has measured them the way the lexicon in section 1 was measured. Use them as things to listen for.

**The proof-shaped paragraph.** Every paragraph runs the same four beats: a general premise, a condition tested against it, a counterpoint weighed, a synthesis. One such paragraph is fine. Five in a row is a template.

**Deliberation markers.** Phrases left over from working the problem out: "Upon closer examination," "From a foundational standpoint," "Under this framing," "It follows that," "Taken together," "At first glance... however." They narrate thinking instead of stating the result.

**Forced symmetry.** Each side of a question gets the same number of sentences at the same length, whatever each one needs. People give a point the words it takes, and no more.

**The discarded hypothesis.** "One might initially assume X. However, Y." The first half is a position nobody in the piece holds, raised only to be put down.

**Metronome pacing.** Long runs of mid-length sentences, each grammatically complete, none short, none sprawling.

**Before:**
> From a foundational standpoint, a four-day week reduces the hours available for work. Upon closer examination, however, the pilot data complicates this picture: output per employee held steady across the six-month trial. On the one hand, this suggests that the lost hours were low-value. On the other hand, it may reflect a novelty effect that fades over time. Taken together, the evidence supports a cautious extension of the pilot rather than a permanent change.

**After:**
> A four-day week means fewer hours of work. The pilot complicates that: output per employee held steady across the six-month trial. That suggests the lost hours were low-value. It may also be a novelty effect, and those fade. So the evidence supports extending the pilot cautiously, not making the change permanent.

Every claim survives at the strength the draft gave it: fewer hours, steady output over six months, a reading that is only suggested, a second that only may be true, and a recommendation that stays cautious. The order is the draft's. What went is the staging.

Fix, in order:

1. **Delete the deliberation markers.** They never hold content.
2. **Keep the order of commitment.** What the draft asserts, what it only suggests, and what it concludes stay in that order. Reordering is how a tentative reading turns into a finding.
3. **Keep every hedge and condition** on the claim it belongs to. "Suggests", "may", "provided that", and "cautious" are content. A rewrite that says "adopt it" where the draft said "adopt it if six pickers are hired" has changed the recommendation.
4. **Unstage the two hands.** Replace "On the one hand / On the other hand" with plain sentences that say what each fact shows, each as long as it needs. A counterargument the author made stays in, and the piece does not end on it unless the draft did.
5. **Move the conclusion up only when it is unqualified.** If the draft states its conclusion flatly, it can open the piece, in the draft's own strength. If it carries a condition or a hedge, it stays after the reasons that qualify it.
6. **Do not pick a side the draft did not pick.** If it ends undecided, say so in one plain sentence ("I can't call this one yet") rather than a balanced essay, and only in the first person if the draft is.
7. **Cut the discarded hypothesis** unless the reversal is the author's actual story ("I assumed X for two years; I was wrong").
8. **Then break the pacing** as in the rhythm step.

---

## 12. Slogan closers and comment bait

Posts, essays, and newsletters from a model end on a push: a motivational line or a question aimed at the comment section. They say nothing the piece has not already said, and they arrive on schedule, which is why they read as machine-made.

**Slogan closers:** "Don't be afraid to fail." "Every step brings you closer to mastery." "The best time to start is now." "Your journey starts today."
**Comment bait:** "What's holding you back?" "What goal are you chasing?" "Agree?" "Thoughts?" "Tag someone who needs this."

**Before:** The first three months were rough, and we lost money every week. Then the Saturday subscription took off. If you're thinking about making a leap of your own, the best time to start is now. What's holding you back?
**After:** The first three months were rough, and we lost money every week. Then the Saturday subscription took off.

Fix: cut the push and end on the last concrete thing the draft says. Never replace a cut closer with a new claim or a lesson the author did not draw.

**Keep a real call to action, in the draft's words.** A link, a sign-up, a deadline, a price, "Start your free trial today," "Reply to this email": these are content, not slogans. Do not soften them ("whenever you're ready") or trade them for something gentler. A softened call to action is a dropped one.

---

## 13. Over-polish (what not to fix)

This section is a list of things to leave alone. Text with no grammatical slack at all reads as machine-made, and one zero-shot detector (GECScore, COLING 2025) is built on exactly that: it runs a grammar corrector over the text and treats "nothing needed correcting" as evidence of a model. An editor who tidies every loose end pushes a human draft toward that profile.

Leave these when the author wrote them and the register allows:

- Sentence fragments. On purpose.
- Sentences that open with "And," "But," "So," or "Because."
- A dropped "that" ("the report she sent" for "the report that she sent").
- Contractions, and the author's regional spelling and idiom.
- Their punctuation habits: a comma splice they clearly like, no serial comma, a fondness for parentheses.
- A slightly long sentence that got away from them and still parses.
- A word repeated because it is the right word.

Fix these: a genuine error that changes the meaning or would embarrass the author (wrong word, broken agreement in a short sentence, a typo), and anything the author asked you to correct.

**Never add an error.** Planting a typo, a dangling modifier, or a deliberate slip to look human is the one move that makes writing both worse and dishonest, and planted errors do not look like real ones: people's mistakes follow their habits, planted ones are scattered. If a draft has no slack because a model wrote it, the cure is the structural and voice work in sections 5 and 11, not damage.

For a falsely flagged human author this is most of the job. Their own irregularities are the best evidence they wrote it. Restore variance where the draft is uniform, and otherwise take your hands off.

---

## 14. Optional: a quick-scan list (a prompt to revise, not a find-and-replace)

This is a convenience, not the method. The whole skill exists because swapping words off a list produces flat, evenly paced, voiceless prose that still flags as AI. Use this list only to *locate* suspect passages fast; then do the real structural and voice work from sections 5 through 13. A hit is not automatically wrong. It is a place to look, and context decides.

If you specifically want an exhaustive, tiered banned-word workflow (severity levels, context profiles, a flag-only mode), that is a different tool: the `avoid-ai-writing` skill owns it. This list stays deliberately short.

For a quick grep over a draft:

```
delve, underscore, tapestry, multifaceted, nuanced, foster, elevate, landscape,
pivotal, streamline, facilitate, garner, leverage, utilize, robust, seamless,
intricate, testament, realm, myriad, plethora, crucial, vital, navigate, harness,
unlock, unleash, transformative, game-changer, comprehensive, holistic, vibrant,
boasts, nestled, renowned, breathtaking, groundbreaking,
furthermore, moreover, additionally, "it's worth noting", "it is important to note",
"in today's", "in the realm of", "when it comes to", "not just", "not only",
"serves as", "stands as", "a testament to", "plays a key role",
"i hope this helps", "great question", "let me know", "certainly!", "of course!",
"upon closer examination", "from a foundational standpoint", "taken together", "it follows that",
"what's holding you back", "the best time to start", "closer to mastery"
```

When you find clusters of these in one passage, that passage almost certainly needs the structural and voice work in sections 5 through 13, not just a word swap.
