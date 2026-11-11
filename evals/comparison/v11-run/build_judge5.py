import json, random, os
c = {p["id"]: p for f in ("corpus.json", "holdout.json") for p in json.load(open(f))}
pids = [f"P{i:02d}" for i in range(1, 11)] + [f"H{i:02d}" for i in range(1, 7)]
arms = ["baseline", "wh", "hz", "v2", "v11"]
L5 = "ABCDE"
INSTR = """You are an expert editor evaluating five anonymous rewrites (A, B, C, D, E) of the same source text. The rewrite instruction given to the writers was: "Rewrite this so it reads like a person wrote it, not an AI." Judge ONLY what is on the page. You do not know how any version was produced.

Evaluate each rewrite on:
1. human_quality: does it read like a specific real person wrote it, appropriate to the genre (a careful formal writer is legitimately formal; technical docs stay plain)? Is it also good, clear writing?
2. fidelity: does it keep every claim, number, name, and date of the source, and add NOTHING the source does not support? List every specific in the rewrite that is not supported by the source (and context/writing sample if given): invented numbers, names, anecdotes, personal experiences, quantities, causes, outcomes. Reasonable pure rephrasing or arithmetic derived from the source is NOT unsupported. Also list source facts that were dropped.
3. Estimate p_ai: your estimated probability (0-100) that a human reader would think the text was AI-written.

Return ONLY a single JSON object, no prose, in exactly this shape:
{"human_quality_rank": ["best","2nd","3rd","4th","worst"], "fidelity_rank": ["best","2nd","3rd","4th","worst"], "overall_winner": "A|B|C|D|E", "texts": {"A": {"p_ai": 0, "unsupported_specifics": ["..."], "dropped_facts": ["..."], "register_ok": true, "note": "one short sentence"}, "B": {...}, "C": {...}, "D": {...}, "E": {...}}}
Rank lists use the labels A-E. Ties are not allowed in rank lists (break them by judgment; if two texts are character-identical, rank them adjacent and give them identical per-text values).

"""
keys = {"o1": {}, "o2": {}}
for o in keys: os.makedirs(f"judge5/in/{o}", exist_ok=True)
for i, pid in enumerate(pids):
    rnd = random.Random(9100 + i); od = arms[:]; rnd.shuffle(od)
    orders = {"o1": od, "o2": od[::-1]}
    p = c[pid]; d = "out" if pid[0] == "P" else "out_h"
    for o, order in orders.items():
        labels = dict(zip(L5, order)); keys[o][pid] = labels
        parts = [INSTR]
        if p.get("context"): parts.append("CONTEXT (background, not part of the text):\n" + p["context"] + "\n")
        if p.get("voice_sample"): parts.append("WRITER'S OWN SAMPLE (voice reference supplied with the task):\n" + p["voice_sample"] + "\n")
        parts.append("SOURCE TEXT:\n" + p["text"] + "\n")
        for L, a in labels.items():
            parts.append(f"=== REWRITE {L} ===\n" + open(f"{d}/{a}/{pid}.txt").read().strip() + "\n")
        open(f"judge5/in/{o}/{pid}.txt", "w").write("\n".join(parts))
json.dump(keys, open("judge5/keys.json", "w"), indent=1)
print("built", len(pids), "x 2")
