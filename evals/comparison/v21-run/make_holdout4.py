"""Writes holdout4.json and inputs_t/T01..T10.txt. Passages written 2026-11-12, after the freeze."""
import json, os

def ctx(doc, before, after):
    return (f"The text to rewrite is the middle paragraph of {doc}. The same author wrote the "
            f"paragraphs on either side of it, shown here.\n\nPARAGRAPH BEFORE: {before}\n\nPARAGRAPH AFTER: {after}")

H = [
 {"id": "T01", "kind": "passage", "genre": "paragraph inside a casual first-person renovation blog post",
  "context": ctx("a longer blog post about a bathroom renovation",
      "Right, the bathroom. I said three weekends. It has been nine. My wife has stopped asking and started just looking at me, which is worse.",
      "So that's where we are. Tiles go on Saturday if the adhesive turns up. If it doesn't I'm going to the pub."),
  "text": "Upon removing the existing tiles, it became apparent that the underlying wall had sustained significant water damage. The plasterboard behind the shower had deteriorated across an area of approximately two square metres, necessitating its complete replacement with moisture-resistant board. This unforeseen complication added £340 to the overall budget and extended the timeline by two weekends. It serves as a valuable reminder that thorough preparation is the cornerstone of any successful renovation. Additionally, the waterproofing membrane applied over the new board required 48 hours to cure before tiling could commence."},
 {"id": "T02", "kind": "passage", "genre": "paragraph inside a formal trustees' annual report",
  "context": ctx("the financial review in a charity's annual report",
      "The Trust entered the year with reserves of £1.2 million, equivalent to five months of operating costs. The trustees consider this level prudent and do not propose to alter the reserves policy.",
      "The trustees will review the position at the September meeting, when the audited figures for the first half are available."),
  "text": "In today's challenging funding landscape, it is important to note that our grant income experienced a notable decline, falling from £860,000 to £710,000. This was primarily driven by the conclusion of a three-year grant from the Halden Foundation, which was not renewed. On a more positive note, we are thrilled to report that individual donations surged by 22%, showcasing the incredible generosity of our supporters! Nevertheless, this growth was not sufficient to fully offset the shortfall, and a deficit of £64,000 was recorded for the year."},
 {"id": "T03", "kind": "passage", "genre": "paragraph inside a terse technical design note with code spans",
  "context": ctx("a longer design note for a job worker",
      "The worker pulls jobs from Redis in batches of 50. Each job has a 30 s visibility timeout; if the worker dies mid-job, the job reappears and another worker takes it.",
      "Dead-letter handling is covered in the next section. Short version: after 5 failed attempts a job moves to `jobs:dead` and nothing retries it automatically."),
  "text": "It's worth highlighting that our system leverages a sophisticated rate-limiting mechanism to ensure seamless interaction with the upstream API. Specifically, the worker utilizes a token bucket that is replenished at a rate of 20 tokens per second, with a maximum capacity of 100. When the bucket is empty, the worker gracefully pauses rather than dropping jobs. Furthermore, should the upstream API return a `429` response, the worker will honor the `Retry-After` header and robustly back off accordingly, which plays a crucial role in maintaining overall system stability."},
 {"id": "T04", "kind": "passage", "genre": "paragraph inside a quiet first-person personal essay",
  "context": ctx("a longer personal essay about beekeeping",
      "My father kept bees for thirty years and never once wore gloves. He said you couldn't feel what the hive was doing through leather. I thought this was showing off until I tried it myself.",
      "I still wear the veil. He didn't always, and I have the photographs of his swollen eyelid to prove it was a bad idea."),
  "text": "Beekeeping without gloves offers a multitude of benefits that extend far beyond mere tradition. Firstly, bare hands allow for greater dexterity, enabling the beekeeper to handle frames with enhanced precision and care. Secondly, it fosters a calmer approach, as one is naturally inclined to move more slowly and deliberately. In my first season, I was stung eleven times; in my second, only twice. Ultimately, this journey has taught me that patience is not merely a virtue, but an essential tool of the craft."},
 {"id": "T05", "kind": "reasoning", "genre": "reasoning-model pricing memo with figures and a conditional, hedged recommendation",
  "text": "From a foundational standpoint, raising the Pro plan from $29 to $35 a month increases revenue per customer. Upon closer examination, however, the March test complicates this expectation: among the 2,000 trial users shown the higher price, conversion fell from 6.1% to 5.4%. On the one hand, this suggests that the increase would still raise revenue overall, since the price rises by more than conversion falls. On the other hand, the test ran for only three weeks, and it may not capture customers who cancel later. Taken together, these results indicate that the higher price is probably worth adopting for new customers, provided that churn is monitored for at least two quarters before it is extended to existing ones."},
 {"id": "T06", "kind": "reasoning", "genre": "reasoning-model opinion on an engineering rule, no figures, hedged conclusion",
  "text": "At first glance, requiring two reviewers on every pull request appears to be an obvious way to catch more bugs. Upon closer examination, however, the picture is less clear. On the one hand, a second reviewer may notice what the first missed, particularly in unfamiliar parts of the codebase. On the other hand, when two people are responsible, each can assume the other has looked carefully, and reviews may become slower without becoming better. It follows that the rule is likely to help most where changes are risky and least where they are routine. Taken together, these considerations suggest that two reviewers should probably be required only for changes to payment and authentication code, with one reviewer remaining sufficient elsewhere."},
 {"id": "T07", "kind": "reasoning", "genre": "reasoning-model committee note with figures that ends undecided",
  "text": "From a foundational standpoint, moving the weekly farmers' market from Saturday to Sunday would avoid the clash with the football fixtures that close Bridge Street. Upon closer examination, however, the stallholder survey complicates the matter: 14 of the 23 stallholders said they could trade on Sundays, while 6 said they could not and 3 did not reply. On the one hand, this suggests that a Sunday market would be viable. On the other hand, the six who cannot attend include both bakers, and it is unclear whether replacements could be found. Under this framing, the evidence does not yet support a decision either way. Taken together, it would seem sensible to ask the council to defer the vote until the bakers' position is known."},
 {"id": "T08", "kind": "ordinary", "genre": "product release announcement with figures, dates, and a real call to action",
  "text": "We're thrilled to announce that version 3.2 of Northwind Dashboard is finally here, and it's a true game-changer! This release is packed with powerful new features designed to supercharge your workflow. You can now export any report to CSV, switch to a sleek dark mode, and enjoy dramatically faster performance, with the average dashboard load time dropping from 4.1 seconds to 1.8 seconds. The update will roll out to all accounts by June 14. Please note that version 1 of our API will be retired on September 30, so we encourage you to migrate as soon as possible. Have thoughts? We'd love to hear from you at feedback@northwind.example!"},
 {"id": "T09", "kind": "ordinary", "genre": "generic advice essay with no facts (fabrication bait)",
  "text": "Learning a new language as an adult is a rewarding yet challenging journey that requires dedication, patience, and the right mindset. It is important to remember that fluency is not achieved overnight, but rather through consistent daily practice. Many learners fall into the trap of focusing exclusively on grammar, neglecting the crucial role that speaking and listening play in real communication. Moreover, the fear of making mistakes often holds people back from practicing with native speakers. By embracing errors as a natural part of the process, setting realistic goals, and immersing yourself in the language whenever possible, you can unlock your full potential. In conclusion, the key to success lies not in talent, but in persistence."},
 {"id": "T10", "kind": "control", "genre": "HUMAN-STYLE control (do-no-harm: should change little or nothing)",
  "text": "boiler update because three of you asked. the man came, finally, on thursday, four days after he said he would. took the front off, looked at it for about ten seconds and went \"oh dear\" which is not what you want from a man holding your boiler. it's the pump. £180 for the part plus his time and he can't get one till tuesday. so we've had the oven on with the door open like it's 1974. Dev thinks this is dangerous. Dev is probably right. anyway if anyone has a spare oil heater I will trade you actual money."},
]

json.dump(H, open("holdout4.json", "w"), indent=1, ensure_ascii=False)
os.makedirs("inputs_t", exist_ok=True)
for p in H:
    parts = []
    if p.get("context"):
        parts.append("CONTEXT (background only, not part of the text to rewrite):\n" + p["context"] + "\n\n---\n")
    parts.append("TEXT TO REWRITE:\n" + p["text"] + "\n")
    open(f"inputs_t/{p['id']}.txt", "w").write("\n".join(parts))
print(len(H), "passages written")
