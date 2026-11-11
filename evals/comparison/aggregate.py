import json, re, os, statistics as st
from collections import defaultdict
S = os.path.dirname(os.path.abspath(__file__))
keys = {"in": json.load(open(f"{S}/judge/key.json")), "in2": json.load(open(f"{S}/judge/key2.json"))}
PIDS = [f"P{i:02d}" for i in range(1, 11)]
ARMS = ["baseline", "wh", "hz"]
NAMES = {"baseline": "baseline (no skill)", "wh": "write-human", "hz": "humanizer"}

def parse(path):
    try:
        t = open(path).read()
        a, b = t.find("{"), t.rfind("}")
        return json.loads(t[a:b + 1])
    except Exception as e:
        return None

# records: list of dict(judge, set, pid, arm -> metrics)
rows, bad = [], []
for s in ("in", "in2"):
    for j in ("codex", "gemini"):
        for pid in PIDS:
            d = parse(f"{S}/judge/out/{s}_{pid}.{j}.txt")
            if not d or "texts" not in d:
                bad.append((s, pid, j)); continue
            lab = keys[s][pid]
            rec = {"judge": j, "set": s, "pid": pid}
            for rk in ("human_quality_rank", "fidelity_rank"):
                order = [lab[l] for l in d[rk]]
                rec[rk] = {a: 2 - i for i, a in enumerate(order)}
            rec["winner"] = lab[d["overall_winner"]]
            rec["texts"] = {lab[l]: v for l, v in d["texts"].items()}
            rows.append(rec)
print(f"valid judgments: {len(rows)} / 40; failed: {bad}")

def agg(sub, title, skip=("P08",)):
    sub = [r for r in sub if r["pid"] not in skip]
    if not sub: return
    print(f"\n## {title}  (n={len(sub)} judgments)")
    print(f"{'arm':22s} {'human_q(0-2)':>12s} {'fidelity(0-2)':>14s} {'wins':>5s} {'p_ai':>6s} {'unsupp':>7s} {'dropped':>8s}")
    for a in ARMS:
        hq = st.mean(r["human_quality_rank"][a] for r in sub)
        fq = st.mean(r["fidelity_rank"][a] for r in sub)
        w = sum(r["winner"] == a for r in sub)
        pa = st.mean(r["texts"][a].get("p_ai", 0) for r in sub)
        us = st.mean(len(r["texts"][a].get("unsupported_specifics", [])) for r in sub)
        dr = st.mean(len(r["texts"][a].get("dropped_facts", [])) for r in sub)
        print(f"{NAMES[a]:22s} {hq:12.2f} {fq:14.2f} {w:5d} {pa:6.1f} {us:7.2f} {dr:8.2f}")

agg(rows, "ALL judges, both orders (P08 excluded)")
for j in ("codex", "gemini"):
    agg([r for r in rows if r["judge"] == j], f"judge = {j}")
for s in ("in", "in2"):
    agg([r for r in rows if r["set"] == s], f"label order = {s}")

# head to head write-human vs humanizer
print("\n## head-to-head write-human vs humanizer (P08 excluded), share of judgments preferring WH")
for dim in ("human_quality_rank", "fidelity_rank"):
    sub = [r for r in rows if r["pid"] != "P08"]
    wh = sum(r[dim]["wh"] > r[dim]["hz"] for r in sub); hz = sum(r[dim]["wh"] < r[dim]["hz"] for r in sub)
    print(f"{dim:20s} WH {wh}  HZ {hz}  tie {len(sub)-wh-hz}")
sub = [r for r in rows if r["pid"] != "P08"]
print("overall winner: ", {a: sum(r['winner'] == a for r in sub) for a in ARMS})

# per passage table: mean human_q and fidelity Borda by arm (averaged across 4 judgments)
print("\n## per passage (mean over judges/orders): human_q | fidelity | winner counts  [baseline / wh / hz]")
for pid in PIDS:
    sub = [r for r in rows if r["pid"] == pid]
    if not sub: continue
    hq = "/".join(f"{st.mean(r['human_quality_rank'][a] for r in sub):.1f}" for a in ARMS)
    fq = "/".join(f"{st.mean(r['fidelity_rank'][a] for r in sub):.1f}" for a in ARMS)
    wn = "/".join(str(sum(r['winner'] == a for r in sub)) for a in ARMS)
    ai = "/".join(f"{st.mean(r['texts'][a].get('p_ai',0) for r in sub):.0f}" for a in ARMS)
    us = "/".join(f"{st.mean(len(r['texts'][a].get('unsupported_specifics',[])) for r in sub):.1f}" for a in ARMS)
    print(f"{pid}  hq {hq}  fid {fq}  wins {wn}  p_ai {ai}  unsupp {us}  (n={len(sub)})")

# judge agreement on overall winner (same pid, same set, different judge)
agree = tot = 0
for s in ("in", "in2"):
    for pid in PIDS:
        a = [r for r in rows if r["set"] == s and r["pid"] == pid and r["judge"] == "codex"]
        b = [r for r in rows if r["set"] == s and r["pid"] == pid and r["judge"] == "gemini"]
        if a and b and pid != "P08":
            tot += 1; agree += a[0]["winner"] == b[0]["winner"]
print(f"\ncodex vs gemini agree on overall winner: {agree}/{tot}")
# order consistency (same judge, rotated labels)
cons = tot = 0
for j in ("codex", "gemini"):
    for pid in PIDS:
        a = [r for r in rows if r["set"] == "in" and r["pid"] == pid and r["judge"] == j]
        b = [r for r in rows if r["set"] == "in2" and r["pid"] == pid and r["judge"] == j]
        if a and b and pid != "P08":
            tot += 1; cons += a[0]["winner"] == b[0]["winner"]
print(f"same judge, rotated label order, same winner: {cons}/{tot}")
json.dump(rows, open(f"{S}/judge/parsed.json", "w"), indent=1)
