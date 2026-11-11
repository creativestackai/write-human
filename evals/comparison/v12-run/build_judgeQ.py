import json, random, os
exec(open("instr4.py").read())          # defines INSTR (4-way prompt)
c = {p["id"]: p for p in json.load(open("holdout2.json"))}
pids = [f"Q{i:02d}" for i in range(1, 9)]
arms = ["wh", "hz", "v11", "v12"]
keys = {"o1": {}, "o2": {}}
for o in keys: os.makedirs(f"judgeQ/in/{o}", exist_ok=True)
for i, pid in enumerate(pids):
    rnd = random.Random(31000 + i); od = arms[:]; rnd.shuffle(od)
    p = c[pid]
    for o, order in {"o1": od, "o2": od[::-1]}.items():
        labels = dict(zip("ABCD", order)); keys[o][pid] = labels
        parts = [INSTR]
        if p.get("context"): parts.append("CONTEXT (background, not part of the text):\n" + p["context"] + "\n")
        if p.get("voice_sample"): parts.append("WRITER'S OWN SAMPLE (voice reference supplied with the task):\n" + p["voice_sample"] + "\n")
        parts.append("SOURCE TEXT:\n" + p["text"] + "\n")
        for L, a in labels.items():
            parts.append(f"=== REWRITE {L} ===\n" + open(f"out_q/{a}/{pid}.txt").read().strip() + "\n")
        open(f"judgeQ/in/{o}/{pid}.txt", "w").write("\n".join(parts))
json.dump(keys, open("judgeQ/keys.json", "w"), indent=1)
print("built", len(pids), "x 2")
