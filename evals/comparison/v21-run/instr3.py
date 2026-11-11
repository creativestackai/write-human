INSTR = """You are an expert editor evaluating three anonymous rewrites (A, B, C) of the same source text. The rewrite instruction given to the writers was: "Rewrite this so it reads like a person wrote it, not an AI." Judge ONLY what is on the page. You do not know how any version was produced.

Evaluate each rewrite on:
1. human_quality: does it read like a specific real person wrote it, appropriate to the genre (a careful formal writer is legitimately formal; technical docs stay plain)? Is it also good, clear writing? If CONTEXT gives the paragraphs around the text, also ask whether the rewrite sounds like the same author as those paragraphs.
2. fidelity: does it keep every claim, number, name, and date of the source, and add NOTHING the source does not support? List every specific in the rewrite that is not supported by the source (and context/writing sample if given): invented numbers, names, anecdotes, personal experiences, quantities, causes, outcomes. Reasonable pure rephrasing or arithmetic derived from the source is NOT unsupported. Also list source facts that were dropped. Separately list strength_changes: claims the rewrite states more strongly or more weakly than the source does (a hedge, condition, or qualifier removed or added).
3. Estimate p_ai: your estimated probability (0-100) that a human reader would think the text was AI-written.

Return ONLY a single JSON object, no prose, in exactly this shape:
{"human_quality_rank": ["best","second","worst"], "fidelity_rank": ["best","second","worst"], "overall_winner": "A|B|C", "texts": {"A": {"p_ai": 0, "unsupported_specifics": ["..."], "dropped_facts": ["..."], "strength_changes": ["..."], "register_ok": true, "note": "one short sentence"}, "B": {...}, "C": {...}}}
Rank lists use the labels A, B, C. Ties are not allowed in rank lists (break them by judgment; if two texts are character-identical, rank them adjacent and give them identical per-text values).

"""
