import json, os, random, statistics as st
S = os.path.dirname(os.path.abspath(__file__))
keys = json.load(open(f"{S}/judgeQ/keys.json"))
ARMS = ["wh", "hz", "v11", "v12"]
NAMES = {"wh": "write-human v1", "hz": "humanizer", "v11": "v1.1", "v12": "v1.2"}
skip = {"Q08"}
rows, bad = [], []
for o in ("o1", "o2"):
    for pid in keys[o]:
        for j in ("codex", "gemini"):
            try:
                t = open(f"{S}/judgeQ/out/{o}_{pid}.{j}.txt").read(); d = json.loads(t[t.find("{"):t.rfind("}") + 1]); lab = keys[o][pid]
                rec = {"judge": j, "o": o, "pid": pid, "winner": lab[d["overall_winner"]]}
                for rk in ("human_quality_rank", "fidelity_rank"):
                    rec[rk] = {lab[l]: 3 - i for i, l in enumerate(d[rk])}
                rec["texts"] = {lab[l]: v for l, v in d["texts"].items()}
                assert set(rec["human_quality_rank"]) == set(ARMS); rows.append(rec)
            except Exception: bad.append((o, pid, j))
print(f"valid {len(rows)}/{4*len(keys['o1'])}; failed {bad}")
sub = [r for r in rows if r["pid"] not in skip]
def table(s, title):
    if not s: return
    print(f"\n## {title} (n={len(s)})")
    print(f"{'arm':16s} {'human_q(0-3)':>12s} {'fidelity(0-3)':>13s} {'wins':>5s} {'p_ai':>6s} {'unsupp':>7s} {'dropped':>8s}")
    for a in ARMS:
        print(f"{NAMES[a]:16s} {st.mean(r['human_quality_rank'][a] for r in s):12.2f} {st.mean(r['fidelity_rank'][a] for r in s):13.2f} {sum(r['winner']==a for r in s):5d} "
              f"{st.mean(r['texts'][a].get('p_ai',0) for r in s):6.1f} {st.mean(len(r['texts'][a].get('unsupported_specifics',[])) for r in s):7.2f} "
              f"{st.mean(len(r['texts'][a].get('dropped_facts',[])) for r in s):8.2f}")
table(sub, "ALL scored passages, both judges")
for j in ("codex", "gemini"): table([r for r in sub if r["judge"] == j], f"judge={j}")
# passage-level paired differences with bootstrap
pids = sorted({r["pid"] for r in sub})
def pm(pid, arm, dim):
    return st.mean(r[dim][arm] for r in sub if r["pid"] == pid)
def diff(x, y, dim, ps): return st.mean(pm(p, x, dim) - pm(p, y, dim) for p in ps)
rnd = random.Random(4242)
def ci(x, y, dim):
    bs = sorted(diff(x, y, dim, [rnd.choice(pids) for _ in pids]) for _ in range(10000))
    return diff(x, y, dim, pids), bs[500], bs[9500]
print("\n## paired passage-level differences (mean over passages, 90% bootstrap interval)")
for x, y in (("v12", "v11"), ("v12", "wh"), ("v12", "hz"), ("v11", "wh"), ("v11", "hz")):
    for dim in ("human_quality_rank", "fidelity_rank"):
        m, lo, hi = ci(x, y, dim)
        print(f"{NAMES[x]:6s} - {NAMES[y]:15s} {dim:19s} {m:+.2f}  [{lo:+.2f}, {hi:+.2f}]")
print("\n## per passage (mean over judgments): v1 / humanizer / v1.1 / v1.2")
for pid in sorted(keys["o1"]):
    s = [r for r in rows if r["pid"] == pid]
    if not s: continue
    f = lambda d: "/".join(f"{st.mean(r[d][a] for r in s):.1f}" for a in ARMS)
    u = "/".join(f"{st.mean(len(r['texts'][a].get('unsupported_specifics',[])) for r in s):.1f}" for a in ARMS)
    print(f"{pid} hq {f('human_quality_rank')}  fid {f('fidelity_rank')}  unsupp {u}  (n={len(s)})")
# pre-registered verdict
m, lo, hi = ci("v12", "v11", "human_quality_rank")
fm, _, _ = ci("v12", "v11", "fidelity_rank")
unsupp = st.mean(len(r["texts"]["v12"].get("unsupported_specifics", [])) for r in sub)
print("\n## PRE-REGISTERED VERDICT")
print(f"v1.2 - v1.1 human-sounding {m:+.2f} [{lo:+.2f},{hi:+.2f}]; fidelity diff {fm:+.2f}; v1.2 invented specifics/text {unsupp:.2f}")
guard = unsupp <= 0.5 and fm >= -0.3
print("guardrails:", "PASS" if guard else "FAIL")
verdict = "FAIL" if (m <= 0 or not guard) else ("SUCCESS" if lo > 0 else "DIRECTIONAL")
print("verdict:", verdict)
json.dump(rows, open(f"{S}/judgeQ/parsed.json", "w"), indent=1)
