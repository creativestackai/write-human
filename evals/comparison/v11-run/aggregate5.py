import json, os, sys, statistics as st
S = os.path.dirname(os.path.abspath(__file__))
keys = json.load(open(f"{S}/judge5/keys.json"))
ARMS = ["baseline", "wh", "hz", "v2", "v11"]
NAMES = {"baseline": "baseline", "wh": "write-human v1", "hz": "humanizer", "v2": "v2 (merged)", "v11": "v1.1 (patch)"}
skip = {"P08", "H06"}   # human-written controls: skill outputs identical to source
rows, bad = [], []
for o in ("o1", "o2"):
    for pid in keys[o]:
        for j in ("codex", "gemini"):
            try:
                t = open(f"{S}/judge5/out/{o}_{pid}.{j}.txt").read(); d = json.loads(t[t.find("{"):t.rfind("}") + 1]); lab = keys[o][pid]
                rec = {"judge": j, "o": o, "pid": pid, "set": "dev" if pid[0] == "P" else "holdout", "winner": lab[d["overall_winner"]]}
                for rk in ("human_quality_rank", "fidelity_rank"):
                    rec[rk] = {lab[l]: 4 - i for i, l in enumerate(d[rk])}
                rec["texts"] = {lab[l]: v for l, v in d["texts"].items()}
                assert set(rec["human_quality_rank"]) == set(ARMS); rows.append(rec)
            except Exception: bad.append((o, pid, j))
print(f"valid {len(rows)}/{4*len(keys['o1'])}; failed {bad}")
def table(sub, title):
    sub = [r for r in sub if r["pid"] not in skip]
    if not sub: return
    print(f"\n## {title} (n={len(sub)})")
    print(f"{'arm':16s} {'human_q(0-4)':>12s} {'fidelity(0-4)':>13s} {'wins':>5s} {'p_ai':>6s} {'unsupp':>7s} {'dropped':>8s}")
    for a in ARMS:
        print(f"{NAMES[a]:16s} {st.mean(r['human_quality_rank'][a] for r in sub):12.2f} {st.mean(r['fidelity_rank'][a] for r in sub):13.2f} {sum(r['winner']==a for r in sub):5d} "
              f"{st.mean(r['texts'][a].get('p_ai',0) for r in sub):6.1f} {st.mean(len(r['texts'][a].get('unsupported_specifics',[])) for r in sub):7.2f} "
              f"{st.mean(len(r['texts'][a].get('dropped_facts',[])) for r in sub):8.2f}")
table(rows, "ALL passages, both judges")
table([r for r in rows if r["set"] == "dev"], "DEV passages")
table([r for r in rows if r["set"] == "holdout"], "HOLDOUT passages")
for j in ("codex", "gemini"): table([r for r in rows if r["judge"] == j], f"judge={j}")
sub = [r for r in rows if r["pid"] not in skip]
print("\n## head to head (judgments preferring first arm; ties dropped)")
for x, y in (("v11", "wh"), ("v11", "hz"), ("v11", "baseline"), ("v11", "v2")):
    for dim in ("human_quality_rank", "fidelity_rank"):
        a = sum(r[dim][x] > r[dim][y] for r in sub); b = sum(r[dim][x] < r[dim][y] for r in sub)
        print(f"{NAMES[x]} vs {NAMES[y]:15s} {dim:19s} {a}:{b}")
print("\n## per passage (mean over judgments): baseline / v1 / humanizer / v2 / v1.1")
for pid in keys["o1"]:
    s = [r for r in rows if r["pid"] == pid]
    if not s: continue
    f = lambda d: "/".join(f"{st.mean(r[d][a] for r in s):.1f}" for a in ARMS)
    u = "/".join(f"{st.mean(len(r['texts'][a].get('unsupported_specifics',[])) for r in s):.1f}" for a in ARMS)
    print(f"{pid} hq {f('human_quality_rank')}  fid {f('fidelity_rank')}  unsupp {u}  (n={len(s)})")
json.dump(rows, open(f"{S}/judge5/parsed.json", "w"), indent=1)
