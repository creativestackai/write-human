import json, re, statistics, difflib, sys, os
S = os.path.dirname(os.path.abspath(__file__))
corpus = {p["id"]: p for p in json.load(open(f"{S}/corpus.json"))}
ARMS = ["baseline", "wh", "hz"]

LEX = """delve|pivotal|crucial|leverag\\w*|seamless\\w*|robust|tapestry|testament|landscape|underscor\\w*|showcas\\w*|foster\\w*|
streamlin\\w*|empower\\w*|unlock\\w*|transformative|game-changer|journey|resilien\\w*|steadfast|nestled|boast\\w*|vibrant|
meticulous\\w*|intricate\\w*|enduring|furthermore|moreover|additionally|it'?s (important|worth) (to note|noting)|
in today'?s|ultimately|at its core|the key to|best-in-class|cutting-edge|harness\\w*|elevate\\w*|holistic|synerg\\w*|
i hope this helps|please do not hesitate|great (news|question)|invaluable|commitment to"""
LEX_RE = re.compile(r"\b(" + LEX.replace("\n", "") + r")\b", re.I)
NOTX = re.compile(r"\b(not (just|only|merely)\b[^.]{0,80}\bbut\b|isn'?t (just|about|merely)[^.]{0,60}(it'?s|but)|not (about|a|an|the)\b[^.;]{0,50}[;,] (it'?s|but)|rather than)", re.I)
TRIAD = re.compile(r"\b[\w-]+(?: [\w-]+)?, [\w-]+(?: [\w-]+)?,? (?:and|or) [\w-]+", re.I)
NUM = re.compile(r"(?<![\w])[€$£]?\d[\d,]*(?:\.\d+)?%?")
FIRST = re.compile(r"\b(I|I'm|I've|I'd|I'll|my|me|we|we've|our|us)\b")

def body(arm_text):
    return arm_text.strip()

def source_text(pid):
    t = corpus[pid]["text"]
    return t

def sents(t):
    parts = re.split(r"(?<=[.!?])\s+|\n+", t)
    return [p for p in parts if len(p.split()) >= 1]

def norm_nums(t):
    return {n.replace(",", "").lstrip("€$£") for n in NUM.findall(t)}

def metrics(src, out):
    w = out.split()
    ss = [len(s.split()) for s in sents(out)]
    cv = (statistics.pstdev(ss) / statistics.mean(ss)) if len(ss) > 1 and statistics.mean(ss) else 0
    sn, on = norm_nums(src), norm_nums(out)
    f_src = len(FIRST.findall(src)); f_out = len(FIRST.findall(out))
    return {
        "words": len(w),
        "len_ratio": round(len(w) / max(1, len(src.split())), 2),
        "dashes": out.count("—") + out.count("–") + out.count(" -- "),
        "lex_hits": len(LEX_RE.findall(out)),
        "not_x_but_y": len(NOTX.findall(out)),
        "triads": len(TRIAD.findall(out)),
        "sent_cv": round(cv, 2),
        "num_lost": sorted(sn - on),
        "num_new": sorted(on - sn),
        "first_person_added": f_out - f_src,
        "similarity": round(difflib.SequenceMatcher(None, src, out).ratio(), 2),
    }

if __name__ == "__main__":
    rows = {}
    for pid in corpus:
        src = source_text(pid)
        rows[pid] = {"source": metrics(src, src)}
        for a in ARMS:
            p = f"{S}/out/{a}/{pid}.txt"
            if os.path.exists(p):
                rows[pid][a] = metrics(src, body(open(p).read()))
    json.dump(rows, open(f"{S}/metrics.json", "w"), indent=1)
    keys = ["words", "len_ratio", "dashes", "lex_hits", "not_x_but_y", "triads", "sent_cv", "first_person_added", "similarity"]
    print("per-arm means over passages (source row for reference)")
    for a in ["source"] + ARMS:
        vals = [rows[p][a] for p in rows if a in rows[p]]
        if not vals: continue
        print(f"{a:9s} n={len(vals):2d} " + " ".join(f"{k}={statistics.mean(v[k] for v in vals):.2f}" for k in keys))
    print("\nnumbers lost / new per passage:")
    for pid in rows:
        for a in ARMS:
            if a in rows[pid]:
                r = rows[pid][a]
                if r["num_lost"] or r["num_new"]:
                    print(pid, a, "lost", r["num_lost"], "new", r["num_new"])
