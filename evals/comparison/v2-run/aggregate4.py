import json, os, sys, statistics as st
tag = sys.argv[1]; skip = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else set()
S = os.path.dirname(os.path.abspath(__file__))
keys = json.load(open(f"{S}/judge4/{tag}/keys.json"))
ARMS = ["baseline", "wh", "hz", "v2"]
NAMES = {"baseline": "baseline", "wh": "write-human v1", "hz": "humanizer", "v2": "write-human v2"}
rows, bad = [], []
for o in ("o1", "o2"):
    for pid in keys[o]:
        for j in ("codex", "gemini"):
            path = f"{S}/judge4/{tag}/out/{o}_{pid}.{j}.txt"
            try:
                t = open(path).read(); d = json.loads(t[t.find("{"):t.rfind("}") + 1]); lab = keys[o][pid]
                rec = {"judge": j, "o": o, "pid": pid, "winner": lab[d["overall_winner"]]}
                for rk in ("human_quality_rank", "fidelity_rank"):
                    rec[rk] = {lab[l]: 3 - i for i, l in enumerate(d[rk])}
                rec["texts"] = {lab[l]: v for l, v in d["texts"].items()}
                assert set(rec["human_quality_rank"]) == set(ARMS)
                rows.append(rec)
            except Exception as e:
                bad.append((o, pid, j))
print(f"[{tag}] valid {len(rows)} / {2*len(keys['o1'])*2}; failed {bad}")
def table(sub, title):
    sub = [r for r in sub if r["pid"] not in skip]
    if not sub: return
    print(f"\n## {title} (n={len(sub)})")
    print(f"{'arm':16s} {'human_q(0-3)':>12s} {'fidelity(0-3)':>13s} {'wins':>5s} {'p_ai':>6s} {'unsupp':>7s} {'dropped':>8s}")
    for a in ARMS:
        print(f"{NAMES[a]:16s} {st.mean(r['human_quality_rank'][a] for r in sub):12.2f} {st.mean(r['fidelity_rank'][a] for r in sub):13.2f} {sum(r['winner']==a for r in sub):5d} "
              f"{st.mean(r['texts'][a].get('p_ai',0) for r in sub):6.1f} {st.mean(len(r['texts'][a].get('unsupported_specifics',[])) for r in sub):7.2f} "
              f"{st.mean(len(r['texts'][a].get('dropped_facts',[])) for r in sub):8.2f}")
table(rows, "ALL judges, both orders")
for j in ("codex", "gemini"): table([r for r in rows if r["judge"] == j], f"judge={j}")
sub = [r for r in rows if r["pid"] not in skip]
print("\n## head to head (judgments preferring first arm)")
for x, y in (("v2", "wh"), ("v2", "hz"), ("v2", "baseline")):
    for dim in ("human_quality_rank", "fidelity_rank"):
        a = sum(r[dim][x] > r[dim][y] for r in sub); b = sum(r[dim][x] < r[dim][y] for r in sub)
        print(f"{NAMES[x]} vs {NAMES[y]:14s} {dim:19s} {x}:{a}  {y}:{b}")
print("\n## per passage (mean over judgments)  order: baseline / v1 / humanizer / v2")
for pid in keys["o1"]:
    s = [r for r in rows if r["pid"] == pid]
    if not s: continue
    f = lambda d: "/".join(f"{st.mean(r[d][a] for r in s):.1f}" for a in ARMS)
    u = "/".join(f"{st.mean(len(r['texts'][a].get('unsupported_specifics',[])) for r in s):.1f}" for a in ARMS)
    p = "/".join(f"{st.mean(r['texts'][a].get('p_ai',0) for r in s):.0f}" for a in ARMS)
    w = "/".join(str(sum(r['winner']==a for r in s)) for a in ARMS)
    print(f"{pid}  hq {f('human_quality_rank')}  fid {f('fidelity_rank')}  wins {w}  p_ai {p}  unsupp {u}  (n={len(s)})")
json.dump(rows, open(f"{S}/judge4/{tag}/parsed.json", "w"), indent=1)
