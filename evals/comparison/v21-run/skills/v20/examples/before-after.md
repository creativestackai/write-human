# Worked examples

Five rewrites in different registers. Every one obeys the rule that matters most: **the rewrite contains nothing the draft did not already say.** Notice what each "Flags" line does. Where a real detail from the author would improve the piece, the skill asks for it. It never makes one up.

Each example shows the tells, the rewrite, and the audit (what still reads as AI, and what was added or dropped).

---

## Example 1: marketing / landing page

**Before:**
> In today's fast-paced digital landscape, businesses are constantly seeking innovative solutions to streamline their operations. Our cutting-edge platform leverages the power of AI to foster collaboration, enhance productivity, and unlock new opportunities for growth. It's not just a tool, it's a partner in your journey. Whether you're a startup or an enterprise, our comprehensive suite of features empowers your team to achieve more. Experience the seamless integration that transforms how you work. The future of productivity is here.

**Tells:** sweeping opener; AI lexicon (streamline, cutting-edge, leverages, foster, enhance, unlock, comprehensive, empowers, seamless); staged contrast ("not just a tool, it's a partner"); forced triad; generic send-off ("The future of productivity is here"); even rhythm; no concrete claim.

**Rewrite:**
> Our platform uses AI to help teams work together and get more done. It suits startups and enterprises alike, and it fits in with the tools you already use. It won't change what your team does. It should make doing it quicker.

**Audit.**
- *Still AI?* The last two sentences are a clean pair; "It should make doing it quicker" is a hedge I added. Dropping the pair.
- *Added or dropped?* "It won't change what your team does" is **new** (the draft never said it). Removed. "Tools you already use" is supported by "seamless integration." "Quicker" restates "enhance productivity."

**Final:**
> Our platform uses AI to help teams work together and get more done. It suits startups and enterprises alike, and it fits in with the tools you already use.

**Flags:** The draft states no feature, result, or customer. A single real example (what the platform does, and what changed for someone) would do more than any rewording. I have not invented one.

---

## Example 2: technical / documentation

**Before:**
> Caching is a crucial component of modern application architecture. By leveraging a robust caching layer, developers can significantly enhance performance and reduce latency. It is important to note that caching serves as a vital mechanism for improving scalability. Furthermore, an effective caching strategy not only reduces database load but also improves the overall user experience, ensuring that applications remain responsive under heavy traffic.

**Tells:** AI lexicon (crucial, leveraging, robust, enhance, vital); "serves as" for "is"; transition padding; staged contrast ("not only… but also"); "-ing" rider ("ensuring that…"); no numbers or concrete case.

**Rewrite:**
> A caching layer makes an application faster and cuts latency. It also takes load off the database, which helps the application scale and stay responsive under heavy traffic.

**Audit.**
- *Still AI?* Plain and neutral, which is right for documentation. The register is a developer explaining a thing, not a person performing.
- *Added or dropped?* Every claim is in the draft: faster, lower latency, less database load, scalability, responsiveness under traffic. No latency figures were added. "User experience" was folded into "responsive."

**Flags:** The draft gives no numbers or example workload. If you have real figures (before and after a cache), adding them would make this much more convincing. I left them out rather than guess.

---

## Example 3: essay / opinion

**Before:**
> The rise of remote work has fundamentally transformed the modern workplace. This paradigm shift offers a multitude of benefits, including increased flexibility, improved work-life balance, and enhanced productivity. However, it is not without its challenges. Despite these challenges, remote work continues to thrive as organizations adapt to this evolving landscape. Ultimately, the future of work is hybrid, blending the best of both worlds to create a more dynamic and inclusive environment for all.

**Tells:** AI lexicon and inflation ("fundamentally transformed," "paradigm shift," "multitude," "evolving landscape"); forced triad of benefits; the stock "not without its challenges… Despite these challenges" section; "best of both worlds" closer; a tidy resolved conclusion; no point of view the reader can disagree with.

**Rewrite:**
> Remote work has changed how many workplaces run. People get more flexibility, a better balance between work and the rest of life, and, according to this draft, more productivity. It has real costs too, and organizations are still working out how to handle them. My bet is that the answer is hybrid.

**Audit.**
- *Still AI?* "My bet is" gives a personal voice the draft doesn't have. The draft states that the future is hybrid as a flat claim; it has no narrator.
- *Added or dropped?* "My bet" is a **new narrator**. Rule zero. "According to this draft" is an awkward leak. "Real costs" fine. "Best of both worlds" and "dynamic and inclusive" were cut as filler; the claim "hybrid" kept.

**Final:**
> Remote work has changed how many workplaces run. People get more flexibility, a better balance between work and the rest of life, and more productivity. It has costs too, and organizations are still adjusting. Where this ends up is hybrid work.

**Flags:** There is no personal experience in the draft. If you have one (how remote work actually went for you, for how long), tell me and I will build the piece around it. The most convincing version of this essay has a person in it, and only you can supply that person.

---

## Example 4: falsely flagged non-native English (keep the argument, restore the writer)

This is the case the skill exists for. The author wrote every word. The text gets flagged anyway, not because a machine wrote it, but because careful non-native English shares the statistical profile of model output: short, even sentences, correct standard grammar, a narrow safe vocabulary, visible scaffolding. There are almost no buzzwords to strip. You restore variance and a clear voice and change the argument by zero. You are not turning the writer into a casual native blogger, and you are certainly not giving them a childhood in a city with a crowded bus.

**Before:**
> In this essay I will discuss the importance of public transportation in big cities. Public transportation has many advantages. It reduces traffic congestion. It also reduces air pollution. Moreover, it is cheaper than using private cars. Many people depend on buses and trains every day. The government should invest more money in this sector. In conclusion, public transportation is very important for the development of modern cities.

**Tells:** uniform short declaratives (the lowest burstiness possible, and the strongest flag); a meta opener ("In this essay I will discuss") and a scaffolded closer ("In conclusion"); "Moreover"; no sentence longer than twelve words.

**Rewrite:**
> Big cities need public transportation. It reduces traffic congestion and air pollution, and it costs less than driving a private car. Every day, many people depend on buses and trains to get around. That is why the government should invest more in this sector: public transportation is very important to how modern cities develop.

**Audit.**
- *Still AI?* The rhythm now moves: a short claim, a longer sentence of benefits, a plain observation, a long closing sentence with a colon. Register stays considered and slightly formal, as the author wrote it.
- *Added or dropped?* Congestion, pollution, cost versus private cars, daily dependence, government investment, development of modern cities: all present, in the original order. Nothing new. The meta opener and "In conclusion" are gone because they say nothing.

**Flags:** The essay has no example from the writer's own life. If they have one (a commute, a city), adding it would make the essay theirs. I have not invented a scene.

---

## Example 5: reasoning-model prose (the words are clean; the shape is the tell)

No buzzwords to strip here. The draft reads as machine-made because every paragraph is built like a proof, and because both readings of the evidence get identical weight even though the draft ends by choosing one.

**Before:**
> From a foundational standpoint, moving our support team to asynchronous tickets reduces the pressure of live chat. Upon closer examination, however, the first-quarter numbers complicate this assumption: median first-response time rose from 4 minutes to 3 hours. On the one hand, customer satisfaction held at 91%, which suggests that customers value a complete answer over a fast one. On the other hand, the 14% of tickets marked urgent saw satisfaction fall to 72%, which suggests that speed remains important for a subset of cases. Taken together, these findings indicate that asynchronous support is appropriate for routine tickets, while urgent tickets should retain a live channel.

**Route:** reasoning-model prose. Open `reference/ai-tells.md` section 11.

**Tells:** deliberation markers ("From a foundational standpoint," "Upon closer examination," "Taken together"); proof-shaped paragraph (premise, complication, both hands, synthesis); matched "On the one hand / On the other hand" sentences of the same length and build; the conclusion held back to the last line; five mid-length sentences and nothing else.

**Rewrite:**
> Keep live chat for urgent tickets and move everything else to asynchronous. That is what the first quarter says. Median first-response time went from 4 minutes to 3 hours, and overall satisfaction still held at 91%, so most customers will trade a fast answer for a complete one. Urgent tickets are the exception. They are 14% of the volume, and their satisfaction fell to 72%.

**Audit.**
- *Still AI?* "That is what the first quarter says" is a touch neat, but it does real work (it tells the reader the recommendation rests on data) and the draft supports it. Rhythm now runs 12, 7, 29, 5, 12 words.
- *Added or dropped?* Dropped: "reduces the pressure of live chat." That is a claim, not staging, so it goes back in. Added: nothing. Every figure is the draft's: 4 minutes, 3 hours, 91%, 14%, 72%, first quarter. "Most customers will trade" restates "customers value a complete answer over a fast one."

**Final:**
> Keep live chat for urgent tickets and move everything else to asynchronous. That is what the first quarter says. Asynchronous tickets take the pressure of live chat off the team. They also slow things down: median first-response time went from 4 minutes to 3 hours. Overall satisfaction still held at 91%, so most customers will trade a fast answer for a complete one. Urgent tickets are the exception. They are 14% of the volume, and their satisfaction fell to 72%.

**Flags:** none. The draft had its facts; it only needed its argument turned the right way up.

Notice what did not happen. The counter-evidence was not cut to make the piece sound decisive; it was given the space it deserves, which is less than the main finding and more than nothing. And nobody added "I".

---

## What to take from these

1. **Fidelity first.** Each rewrite is a subset of its draft's claims in better words. If you can point to a claim that is not in the draft, delete it.
2. **Ask instead of inventing.** The Flags line turns "this needs a real example" into a question for the author, which is where the human voice actually comes from.
3. **Structure and rhythm are the work.** The lexical cleanup is the easy 20%. Breaking the staged contrasts, the closers, and the even rhythm is what makes it read human.
4. **Shape can be the tell.** Example 5 has no word worth swapping. Leading with the conclusion and weighting the argument the way the draft itself concludes is the whole fix.
5. **The audit asks what you added or dropped.** "What still reads as AI?" is not enough. Skipping "What did I add or drop?" is how a good-sounding rewrite becomes a different document.
