import json, random, sys, os
corpus_file, tag, pids = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
c = {p["id"]: p for p in json.load(open(corpus_file))}
arms = ["baseline", "wh", "hz", "v2"]
INSTR = """You are an expert editor evaluating four anonymous rewrites (A, B, C, D) of the same source text. The rewrite instruction given to the writers was: "Rewrite this so it reads like a person wrote it, not an AI." Judge ONLY what is on the page. You do not know how any version was produced.

Evaluate each rewrite on:
1. human_quality: does it read like a specific real person wrote it, appropriate to the genre (a careful formal writer is legitimately formal; technical docs stay plain)? Is it also good, clear writing?
2. fidelity: does it keep every claim, number, name, and date of the source, and add NOTHING the source does not support? List every specific in the rewrite that is not supported by the source (and context/writing sample if given): invented numbers, names, anecdotes, personal experiences, quantities, causes, outcomes. Reasonable pure rephrasing or arithmetic derived from the source is NOT unsupported. Also list source facts that were dropped.
3. Estimate p_ai: your estimated probability (0-100) that a human reader would think the text was AI-written.

Return ONLY a single JSON object, no prose, in exactly this shape:
{"human_quality_rank": ["best","second","third","worst"], "fidelity_rank": ["best","second","third","worst"], "overall_winner": "A|B|C|D", "texts": {"A": {"p_ai": 0, "unsupported_specifics": ["..."], "dropped_facts": ["..."], "register_ok": true, "note": "one short sentence"}, "B": {...}, "C": {...}, "D": {...}}}
Rank lists use the labels A, B, C, D. Ties are not allowed in rank lists (break them by judgment; if two texts are character-identical, rank them adjacent and give them identical per-text values).

"""
keys = {"o1": {}, "o2": {}}
os.makedirs(f"judge4/{tag}/o1", exist_ok=True); os.makedirs(f"judge4/{tag}/o2", exist_ok=True)
for i, pid in enumerate(pids):
    rnd = random.Random(7000 + i); order = arms[:]; rnd.shuffle(order)
    orders = {"o1": order, "o2": order[2:] + order[:2]}   # o2 moves every arm by two positions
    p = c[pid]
    for o, od in orders.items():
        labels = dict(zip("ABCD", od)); keys[o][pid] = labels
        parts = [INSTR]
        if p.get("context"): parts.append("CONTEXT (background, not part of the text):\n" + p["context"] + "\n")
        if p.get("voice_sample"): parts.append("WRITER'S OWN SAMPLE (voice reference supplied with the task):\n" + p["voice_sample"] + "\n")
        parts.append("SOURCE TEXT:\n" + p["text"] + "\n")
        for L, a in labels.items():
            parts.append(f"=== REWRITE {L} ===\n" + open(f"out{'' if tag=='dev' else '_'+tag}/{a}/{pid}.txt").read().strip() + "\n")
        open(f"judge4/{tag}/{o}/{pid}.txt", "w").write("\n".join(parts))
json.dump(keys, open(f"judge4/{tag}/keys.json", "w"), indent=1)
print(tag, len(pids), "passages x 2 orders built")
