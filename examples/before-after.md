# Worked examples

Four full rewrites in different registers, each showing the whole loop: diagnosis, rewrite, the adversarial self-audit, and the final. The last one is the falsely-flagged non-native-English case the skill is really for. Study the self-audit step. It is what separates a real humanize pass from a word swap.

---

## Example 1: marketing / landing page

**Before:**
> In today's fast-paced digital landscape, businesses are constantly seeking innovative solutions to streamline their operations. Our cutting-edge platform leverages the power of AI to foster collaboration, enhance productivity, and unlock new opportunities for growth. It's not just a tool, it's a partner in your journey. Whether you're a startup or an enterprise, our comprehensive suite of features empowers your team to achieve more. Experience the seamless integration that transforms how you work. The future of productivity is here.

**Diagnosis:**
- Sweeping opener ("In today's fast-paced digital landscape")
- Dense AI lexicon: streamline, cutting-edge, leverages, foster, enhance, unlock, comprehensive, seamless, empowers, transforms
- Negative parallelism ("not just a tool, it's a partner")
- Rule of three ("foster collaboration, enhance productivity, and unlock opportunities")
- Zero specifics, zero voice, no actual claim about what the product does
- Generic upbeat closer ("The future of productivity is here")
- Even rhythm throughout

**Rewrite:**
> Most teams don't need another tool. They need to stop losing two hours a day to the same handful of repetitive tasks. That is the thing we actually fix. Connect your stack, and the busywork that used to eat your mornings (chasing approvals, copy-pasting between apps, re-typing the same updates) mostly just stops. Startups use it to skip hiring an ops person too early. Bigger teams use it to claw back the hours nobody admits they're losing. You will know it's working when your Monday doesn't start with forty minutes of admin.

**What still reads as AI?**
- "claw back the hours nobody admits they're losing" is a touch slogan-y
- The rhythm is good but the middle sentence runs long and could use a break for contrast
- "Connect your stack" is slightly jargon-flat

**Final:**
> Most teams don't need another tool. They need to stop losing two hours a day to the same repetitive junk. That's what we fix. You plug in the apps you already use, and the busywork that used to eat your mornings mostly stops: chasing approvals, copy-pasting between tabs, re-typing the same status update for the third time. Smaller teams use it to put off hiring an ops person. Bigger ones use it to recover hours they'd stopped noticing. You'll know it's working the first Monday you don't open your laptop to forty minutes of admin.

---

## Example 2: technical / documentation

**Before:**
> Caching is a crucial component of modern application architecture. By leveraging a robust caching layer, developers can significantly enhance performance and reduce latency. It is important to note that caching serves as a vital mechanism for improving scalability. Furthermore, an effective caching strategy not only reduces database load but also improves the overall user experience, ensuring that applications remain responsive under heavy traffic.

**Diagnosis:**
- AI lexicon: crucial, leveraging, robust, enhance, vital, effective
- Copula avoidance ("caching serves as a vital mechanism") instead of plain "is"
- Transition padding ("It is important to note that," "Furthermore")
- Negative parallelism ("not only reduces load but also improves experience")
- Superficial "-ing" tail ("ensuring that applications remain responsive")
- No concrete detail: what kind of cache, how much latency, when it bites you
- Note: technical writing is also where humans get *falsely* flagged, so the goal here is to keep it precise but add the variance and concreteness that real engineers write with

**Rewrite:**
> A cache is just a copy of an answer you already computed, kept somewhere fast so you don't have to compute it again. The win is obvious when a query is expensive and the answer rarely changes: a product page that hits the database on every load might take 200ms, but serve it from Redis and you're looking at 2 to 5ms. The catch is that caches go stale. The hard part of caching was never adding the cache. It's deciding when to throw the old answer away.

**What still reads as AI?**
- Mostly clean. "The win is obvious" is a small tic.
- Could use one more concrete failure mode to feel lived-in rather than explained

**Final:**
> A cache is a copy of an answer you already computed, parked somewhere fast so you don't pay to compute it twice. It pays off when a query is expensive and the result rarely changes. A product page that hits the database on every load might take 200ms; served from Redis it's more like 2 to 5ms. Then the answer changes and your cache doesn't know, and now you're shipping a stale price to a customer. Adding the cache was never the hard part. Knowing when to throw the old copy away is the whole job, and it's where most of the bugs live.

---

## Example 3: essay / reflective

**Before:**
> The rise of remote work has fundamentally transformed the modern workplace. This paradigm shift offers a multitude of benefits, including increased flexibility, improved work-life balance, and enhanced productivity. However, it is not without its challenges. Despite these challenges, remote work continues to thrive as organizations adapt to this evolving landscape. Ultimately, the future of work is hybrid, blending the best of both worlds to create a more dynamic and inclusive environment for all.

**Diagnosis:**
- AI lexicon: fundamentally transformed, paradigm shift, multitude, enhanced, evolving landscape, dynamic
- Rule of three ("flexibility, balance, and productivity")
- Formulaic "challenges" section ("not without its challenges. Despite these challenges...")
- Negative-parallelism-flavored closer ("best of both worlds")
- Generic upbeat conclusion that asserts a tidy resolution
- No first person, no real opinion, no specific experience
- Marching, even rhythm

**Rewrite:**
> I've worked from home for six years and I still don't fully trust the productivity claims. Some of it is real: I get my best two hours of focus before anyone in a different timezone is awake, and no open-plan office ever gave me that. But "work-life balance" is doing a lot of lifting in those articles. When the office is the next room, the workday doesn't end so much as fade out around 9pm. The honest version is that remote work didn't fix anything. It traded one set of problems (commutes, interruptions, presenteeism) for another (isolation, blurred hours, the slow realization that you haven't spoken out loud all day). Which set you'd rather have is a real question, and I notice the people who answer it confidently usually only have experience with one.

**What still reads as AI?**
- Genuinely strong now. The parenthetical lists are slightly tidy, bordering on a rule-of-three rhythm.
- The last sentence is a little aphoristic; fine here because it reads as the author's actual opinion rather than a manufactured insight

**Final:** (only a small trim to the parentheticals)
> I've worked from home for six years and I still don't fully trust the productivity claims. Some of it is real. I get my best two hours of focus before anyone east of me is awake, and no open-plan office ever gave me that. But "work-life balance" is doing a lot of lifting in those articles. When the office is the next room, the workday doesn't end. It just fades out somewhere around 9pm. The honest version is that remote work didn't fix anything; it swapped commutes and interruptions for isolation and hours that never quite close. Which trade you prefer is a real question. I notice the people who answer it fast usually only have experience with one side of it.

---

## Example 4: falsely-flagged non-native English (keep the argument, restore the writer)

This is the case the skill exists for. The author wrote every word. The text gets flagged anyway, not because a machine wrote it, but because careful non-native English shares the same statistical profile as model output: short, even sentences, correct standard grammar, a narrow and safe vocabulary, visible scaffolding. The job here is different from the others. There are almost no buzzwords to strip. You restore variance, a real point of view, and one or two concretes the author actually has, while changing the argument by zero. You are not turning this person into a casual native blogger. You are letting their own voice through.

**Before:**
> In this essay I will discuss the importance of public transportation in big cities. Public transportation has many advantages. It reduces traffic congestion. It also reduces air pollution. Moreover, it is cheaper than using private cars. Many people depend on buses and trains every day. The government should invest more money in this sector. In conclusion, public transportation is very important for the development of modern cities.

**Diagnosis:**
- Uniform short declarative sentences end to end: the lowest-burstiness possible, which is the single strongest flag
- Meta opener ("In this essay I will discuss") and scaffolded closer ("In conclusion")
- "Moreover" as connective padding
- Correct but narrow vocabulary; nothing a model would not also pick
- Generic claims with no specific the writer actually owns
- The cause is register, not authorship. The fix must keep every part of the argument (congestion, pollution, cost, invest more) and must not impose a chatty native-speaker voice the author never had

**Rewrite:**
> Public transport is the difference between a city that moves and one that seizes up. In the city where I grew up, the morning bus to the centre was full by the second stop, and even then it was faster than driving and far cheaper. That is the case I want to make. Buses and trains carry people for a fraction of the cost, they take cars off the road, and by midday you can see the difference in the air. More roads will not fix that. Only moving people in bulk will. If a government is serious about a modern city, this is where the money should go.

**What still reads as AI?**
- "for a fraction of the cost, they take cars off the road, and by midday..." is edging back toward a tidy rule-of-three; break it
- Otherwise the argument is intact and the rhythm now varies, which is the whole point

**Final:** (triad broken, register kept serious rather than casual)
> Public transport is the difference between a city that moves and one that seizes up. In the city where I grew up, the morning bus to the centre was full by the second stop. It was still faster than driving, and far cheaper. That is the case I want to make. Buses and trains carry people in bulk, for a fraction of what cars cost, and by midday the difference shows in the air over the city. More roads have never solved this anywhere. If a government is serious about a modern city, this is where the money goes.

The argument did not change. Congestion, pollution, cost, and the call to invest are all still there, in the same order of priority. What changed is that the sentences now breathe, there is a concrete the writer plausibly lived (the bus full by the second stop), and a clear position carries it. The register stayed where the author put it: considered, a little formal, not pretending to be anyone else.

---

## What to take from these

In all three, the lexical and formatting cleanup was the easy 20%. The work that made them read human was:

1. **A person showing up.** First-person experience, an actual opinion, a willingness to say the popular claim is oversold.
2. **Specifics replacing abstractions.** 200ms versus 2ms. Six years. Forty minutes of Monday admin. Numbers and scenes, not adjectives.
3. **Rhythm that varies.** Short sentence. Then a long one that wanders. Then a fragment. Look at the shape, not just the words.
4. **The self-audit.** Every final draft is better than its first rewrite because the "what still reads as AI?" pass caught the leftover tidiness. Never skip it.
