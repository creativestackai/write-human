import json, random, os
exec(open("instr3.py").read())          # defines INSTR (3-way prompt)
c = {p["id"]: p for p in json.load(open("holdout4.json"))}
pids = [f"T{i:02d}" for i in range(1, 11)]
arms = ["v11", "v20", "v21"]
keys = {"o1": {}, "o2": {}}
for o in keys: os.makedirs(f"judgeT/in/{o}", exist_ok=True)
jobs = []
for i, pid in enumerate(pids):
    rnd = random.Random(61000 + i); od = arms[:]; rnd.shuffle(od)
    p = c[pid]
    for o, order in {"o1": od, "o2": od[::-1]}.items():
        labels = dict(zip("ABC", order)); keys[o][pid] = labels
        parts = [INSTR]
        if p.get("context"): parts.append("CONTEXT (background, not part of the text):\n" + p["context"] + "\n")
        if p.get("voice_sample"): parts.append("WRITER'S OWN SAMPLE (voice reference supplied with the task):\n" + p["voice_sample"] + "\n")
        parts.append("SOURCE TEXT:\n" + p["text"] + "\n")
        for L, a in labels.items():
            parts.append(f"=== REWRITE {L} ===\n" + open(f"out_t/{a}/{pid}.txt").read().strip() + "\n")
        open(f"judgeT/in/{o}/{pid}.txt", "w").write("\n".join(parts))
        jobs += [f"{o} {pid} codex", f"{o} {pid} gemini"]
json.dump(keys, open("judgeT/keys.json", "w"), indent=1)
open("judgeT/jobs.txt", "w").write("\n".join(jobs) + "\n")
print("built", len(pids), "x 2")
