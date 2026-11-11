#!/usr/bin/env python3
"""Mechanical checks for a write-human rewrite.

Measures what code can measure so the model does not have to assert it:

  fidelity  numbers, names, quotes, or a narrator that the rewrite has and the source lacks
  rhythm    sentence-length variation and runs of same-length sentences
  tells     counts of the loudest surface patterns
  voice     how far the rewrite sits from the author's writing sample, or from the
            paragraphs around it

Every line of output is a place to look, not a verdict. This is not an AI
detector and it cannot tell you how any detector will score the text.

Usage:
  python3 scripts/check.py REWRITE [--source DRAFT] [--sample SAMPLE] [--context PAGE] [--json] [--strict]

Standard library only. Python 3.8+.
"""

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

# A period after one of these never ends a sentence.
TITLES = ("Mr", "Mrs", "Ms", "Dr", "Prof", "St", "vs", "e.g", "i.e")
# A period after one of these ends a sentence only when a capital follows.
SUFFIXES = ("Co", "Inc", "Ltd", "Corp", "etc")
DOT = "․"  # stand-in for a period that does not end a sentence

LEXICON = (
    r"delv\w+|tapestry|multifaceted|nuanced|foster\w*|elevat\w+|landscape|pivotal|streamlin\w+|"
    r"facilitat\w+|garner\w*|leverag\w+|utiliz\w+|robust|seamless\w*|intricate|intricacies|testament|"
    r"realm|myriad|plethora|crucial|harness\w*|unlock\w*|unleash\w*|transformative|game-changer|"
    r"holistic|vibrant|boasts|nestled|renowned|breathtaking|groundbreaking|underscor\w+|showcas\w+|"
    r"empower\w*|cutting-edge|invaluable"
)
PADDING = (
    r"furthermore|moreover|additionally|it'?s worth noting|it is worth noting|"
    r"it'?s important to (?:note|understand)|it is important to (?:note|understand)|"
    r"in today'?s|when it comes to|needless to say|in order to|in conclusion|ultimately"
)
STAGED_CONTRAST = (
    r"not (?:just|only|merely|simply)\b[^.?!]{0,80}?\b(?:but|it'?s|it is)\b|"
    r"(?:isn'?t|is not|aren'?t) (?:just|merely|simply|about)\b[^.?!]{0,60}?\b(?:it'?s|it is|but)\b"
)
REASONING_MARKERS = (
    r"upon closer (?:examination|inspection)|on closer (?:examination|inspection)|"
    r"from a foundational standpoint|under this (?:analytical )?(?:framing|lens)|"
    r"it follows that|to unpack this|at first glance|a careful analysis (?:reveals|shows)|"
    r"taken together|on (?:the one|one) hand|on the other hand|that said|"
    r"this (?:suggests|implies|indicates) that|viewed through this lens|strictly speaking"
)
CLOSERS = (
    r"what'?s holding you back|what are you (?:chasing|waiting for)|the best time to start is now|"
    r"take the first step|closer to mastery|your journey (?:starts|begins)|don'?t be afraid to fail|"
    r"the future (?:of [\w ]{1,30} )?(?:is here|looks bright)|exciting times lie ahead|"
    r"i hope this helps|let me know if|thoughts\?|agree\?"
)
TRIAD = r"\b[\w-]+(?: [\w-]+)?, [\w-]+(?: [\w-]+)?,? (?:and|or) [\w-]+"

UNITS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine".split())}
SMALL = {
    **{w: i for i, w in enumerate("two three four five six seven eight nine ten eleven twelve".split(), start=2)},
    **{w: i for i, w in enumerate(
        "thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split(), start=13)},
}
TENS = {w: 10 * i for i, w in enumerate(
    "twenty thirty forty fifty sixty seventy eighty ninety".split(), start=2)}
LARGE = {"hundred": 100, "thousand": 1000, "million": 1000000, "billion": 1000000000}
CALENDAR = {
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "january", "february", "march", "april", "june", "july", "august", "september",
    "october", "november", "december",
}

DIGITS = r"(?<![\w.])\d[\d,]*(?:\.\d+)?"
DIGITS_RE = re.compile(DIGITS)
COMPOUND_RE = re.compile(r"\b(%s)[- ](%s)\b" % ("|".join(TENS), "|".join(list(UNITS)[1:])), re.I)
NUMBER_WORD_RE = re.compile(r"\b(%s)\b" % "|".join({**SMALL, **TENS, **LARGE}), re.I)
SCALED_RE = re.compile(
    r"(?:(%s)|\b(%s|an?))[ -](%s)\b" % (DIGITS, "|".join({**SMALL, **TENS}), "|".join(LARGE)), re.I)
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’-]*")
QUOTE_RE = re.compile(r"[\"“]([^\"“”]{3,}?)[\"”]")
FIRST_SINGULAR_RE = re.compile(r"\bI\b|\b(?:[Mm]y|[Mm]e|[Mm]ine|[Mm]yself)\b")
FIRST_PERSON_RE = re.compile(r"\bI\b|\b(?:my|me|mine|myself|we|our|us|ours)\b", re.I)
SECOND_PERSON_RE = re.compile(r"\b(?:you|your|yours|yourself)\b", re.I)
CONTRACTION_RE = re.compile(
    r"\b\w+n['’]t\b|\b\w+['’](?:re|ve|ll|d|m)\b|"
    r"\b(?:it|that|there|here|what|who|he|she|let|how|where)['’]s\b",
    re.I,
)
# Words that carry how sure, or how conditional, a claim is. Losing one can turn
# "the trial suggests" into "the trial shows".
HEDGES = (
    "may might could would should can suggests suggest suggested appears appear seems seem "
    "indicates indicate likely unlikely probably possibly perhaps maybe roughly about around "
    "approximately almost nearly some often usually sometimes generally provided unless if "
    "whether tends tend partly largely"
).split()
HEDGE_RE = re.compile(r"\b(%s)\b" % "|".join(HEDGES), re.I)
OPENING_CONJUNCTION_RE = re.compile(r"^(?:and|but|so|or|yet|because)\b", re.I)


def strip_markup(text):
    """Remove code and markdown scaffolding so only prose is measured."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"^\s{0,3}(?:#{1,6}|[-*+]|\d+\.|>)\s+", "", text, flags=re.M)
    return text.replace("**", "").replace("__", "")


def split_sentences(text):
    prose = strip_markup(text)
    for abbr in TITLES:
        prose = re.sub(r"\b%s\." % re.escape(abbr), abbr.replace(".", DOT) + DOT, prose)
    for abbr in SUFFIXES:
        prose = re.sub(r"\b%s\.(?!\s+[A-Z])" % abbr, abbr + DOT, prose)
    parts = re.split(r"(?<=[.!?])[\"'”’)\]]*\s+|\n{2,}", prose)
    return [" ".join(p.replace(DOT, ".").split()) for p in parts if WORD_RE.search(p)]


def word_count(text):
    return len(strip_markup(text).split())


def variation(values):
    if len(values) < 2 or not statistics.mean(values):
        return 0.0
    return round(statistics.pstdev(values) / statistics.mean(values), 2)


def longest_even_run(lengths):
    """Longest stretch of consecutive sentences that are all about the same length."""
    best = 0
    for start in range(len(lengths)):
        low = high = lengths[start]
        end = start
        while end < len(lengths):
            low, high = min(low, lengths[end]), max(high, lengths[end])
            if high > low * 1.25 + 1:
                break
            end += 1
        best = max(best, end - start)
    return best


def rhythm(text):
    lengths = [len(s.split()) for s in split_sentences(text)]
    paragraphs = [len(p.split()) for p in re.split(r"\n\s*\n", strip_markup(text)) if p.strip()]
    return {
        "sentences": len(lengths),
        "mean_len": round(statistics.mean(lengths), 1) if lengths else 0.0,
        "cv": variation(lengths),
        "longest_even_run": longest_even_run(lengths),
        "paragraphs": len(paragraphs),
        "paragraph_cv": variation(paragraphs),
    }


def find_all(pattern, text):
    return [" ".join(m.group(0).lower().split()) for m in re.finditer(pattern, text, re.I)]


def tells(text):
    prose = strip_markup(text)
    return {
        "em_dashes": prose.count("—") + prose.count(" -- "),
        "lexicon": find_all(r"\b(?:%s)\b" % LEXICON, prose),
        "padding": find_all(r"\b(?:%s)\b" % PADDING, prose),
        "staged_contrast": find_all(STAGED_CONTRAST, prose),
        "reasoning_markers": find_all(r"\b(?:%s)\b" % REASONING_MARKERS, prose),
        "closers": find_all(CLOSERS, prose),
        "triads": len(re.findall(TRIAD, prose)),
    }


def canonical(value):
    """One spelling per value, so 5.0, 5 and "five" all compare equal."""
    number = float(value)
    return str(int(number)) if number == int(number) else repr(number)


def digit_value(token):
    return float(token.replace(",", "").rstrip("."))


def scaled_value(match):
    table = {**SMALL, **TENS}
    digits, word, scale = match.group(1), match.group(2), match.group(3).lower()
    base = digit_value(digits) if digits else table.get(word.lower(), 1)
    return base * LARGE[scale]


def numbers(text):
    """Every number in the text as a canonical string, digits and spelled-out alike.

    Known gaps: "one" and "zero" as words are skipped (too common as non-numbers),
    and a leading minus sign is not read, since it cannot be told from a hyphen.
    """
    table = {**SMALL, **TENS, **LARGE}
    scaled = {canonical(scaled_value(m)) for m in SCALED_RE.finditer(text)}
    rest = SCALED_RE.sub(" ", text)
    compounds = {canonical(TENS[m.group(1).lower()] + UNITS[m.group(2).lower()]) for m in COMPOUND_RE.finditer(rest)}
    rest = COMPOUND_RE.sub(" ", rest)
    digits = {canonical(digit_value(m.group(0))) for m in DIGITS_RE.finditer(rest)}
    words = {canonical(table[m.group(1).lower()]) for m in NUMBER_WORD_RE.finditer(rest)}
    return scaled | compounds | digits | words


def normalise_word(token):
    return re.sub(r"['’]s$", "", token.lower())


def proper_nouns(sentence):
    """Capitalised words after the first word of a sentence, plus any day or month.

    A sentence-initial word is skipped because its capital proves nothing; a
    multi-word name that opens a sentence is still caught by its second word.
    """
    tokens = WORD_RE.findall(sentence)
    names = []
    for index, token in enumerate(tokens):
        if not token[0].isupper() or re.match(r"I(?:['’]|$)", token):
            continue
        if index > 0 or normalise_word(token) in CALENDAR:
            names.append(re.sub(r"['’]s$", "", token))
    return names


def squash(text):
    return re.sub(r"[^a-z0-9 ]", "", " ".join(text.lower().split()))


MODAL_CONTRACTION_RE = re.compile(r"\b(could|would|should|might)n['’]t\b", re.I)
CANNOT_RE = re.compile(r"\b(can)(?:not|['’]t)\b", re.I)


def hedge_counts(text):
    # "could not" and "couldn't" carry the same hedge, so count them alike.
    text = CANNOT_RE.sub(r"\1 not", MODAL_CONTRACTION_RE.sub(r"\1 not", text))
    counts = {}
    for match in HEDGE_RE.finditer(text):
        word = match.group(1).lower()
        counts[word] = counts.get(word, 0) + 1
    return counts


def fewer(first, second):
    """Words that occur fewer times in `second` than in `first`."""
    return sorted(word for word, count in first.items() if second.get(word, 0) < count)


def fidelity(source, rewrite):
    # Numbers are read from the raw text so that figures inside code spans count.
    source_numbers, rewrite_numbers = numbers(source.replace("`", " ")), numbers(rewrite.replace("`", " "))
    source, rewrite = strip_markup(source), strip_markup(rewrite)
    source_words = {normalise_word(t) for t in WORD_RE.findall(source)}
    names = []
    for sentence in split_sentences(rewrite):
        for name in proper_nouns(sentence):
            if normalise_word(name) not in source_words and name not in names:
                names.append(name)
    # Only words the draft itself put in quotation marks may be quoted in the rewrite.
    source_quotes = [squash(q) for q in QUOTE_RE.findall(source)]
    quotes = [q.strip() for q in QUOTE_RE.findall(rewrite) if not any(squash(q) in s for s in source_quotes)]
    source_len = len(source.split())
    source_hedges, rewrite_hedges = hedge_counts(source), hedge_counts(rewrite)
    return {
        "numbers_added": sorted(rewrite_numbers - source_numbers, key=float),
        "numbers_dropped": sorted(source_numbers - rewrite_numbers, key=float),
        "names_added": names,
        "quotes_added": quotes,
        "hedges_dropped": fewer(source_hedges, rewrite_hedges),
        "hedges_added": fewer(rewrite_hedges, source_hedges),
        "narrator_added": bool(FIRST_SINGULAR_RE.search(rewrite)) and not FIRST_SINGULAR_RE.search(source),
        "length_ratio": round(len(rewrite.split()) / source_len, 2) if source_len else 0.0,
    }


def per_hundred(count, total):
    return round(100.0 * count / total, 1) if total else 0.0


def profile(text):
    """A small stylometric fingerprint of one writer's sample."""
    prose = strip_markup(text)
    sentences = split_sentences(text)
    lengths = [len(s.split()) for s in sentences]
    total_words, total_sentences = len(prose.split()), len(sentences)
    word_lengths = [len(w) for w in WORD_RE.findall(prose)]
    return {
        "mean_sentence_len": round(statistics.mean(lengths), 1) if lengths else 0.0,
        "mean_word_len": round(statistics.mean(word_lengths), 1) if word_lengths else 0.0,
        "sentence_cv": variation(lengths),
        "fragment_share": round(sum(1 for n in lengths if n <= 3) / total_sentences, 2) if lengths else 0.0,
        "contractions_per_100w": per_hundred(len(CONTRACTION_RE.findall(prose)), total_words),
        "first_person_per_100w": per_hundred(len(FIRST_PERSON_RE.findall(prose)), total_words),
        "second_person_per_100w": per_hundred(len(SECOND_PERSON_RE.findall(prose)), total_words),
        "commas_per_sentence": round(prose.count(",") / total_sentences, 1) if lengths else 0.0,
        "question_share": round(sum(1 for s in sentences if s.endswith("?")) / total_sentences, 2) if lengths else 0.0,
        "conjunction_opener_share": round(
            sum(1 for s in sentences if OPENING_CONJUNCTION_RE.match(s)) / total_sentences, 2) if lengths else 0.0,
    }


# metric: (relative tolerance, absolute floor). A gap is flagged only if it exceeds both.
TOLERANCES = {
    "mean_sentence_len": (0.3, 3.0),
    "mean_word_len": (0.12, 0.4),
    "sentence_cv": (0.35, 0.15),
    "fragment_share": (0.5, 0.1),
    "contractions_per_100w": (0.5, 1.5),
    "first_person_per_100w": (0.5, 2.0),
    "second_person_per_100w": (0.5, 2.0),
    "commas_per_sentence": (0.5, 0.7),
    "question_share": (0.5, 0.1),
    "conjunction_opener_share": (0.5, 0.1),
}


def compare(sample_profile, rewrite_profile):
    rows = []
    for metric, (relative, floor) in TOLERANCES.items():
        sample, rewrite = sample_profile[metric], rewrite_profile[metric]
        gap = abs(sample - rewrite)
        rows.append({
            "metric": metric,
            "sample": sample,
            "rewrite": rewrite,
            "flag": gap > floor and gap > relative * max(sample, rewrite),
        })
    return rows


def build_report(rewrite, source=None, sample=None, context=None):
    report = {"rhythm": rhythm(rewrite), "tells": tells(rewrite)}
    if source is not None:
        report["fidelity"] = fidelity(source, rewrite)
        report["source_rhythm"] = rhythm(source)
    if sample is not None:
        report["voice"] = compare(profile(sample), profile(rewrite))
    if context is not None:
        report["context_voice"] = compare(profile(context), profile(rewrite))
    return report


def fidelity_failed(report):
    f = report.get("fidelity", {})
    return bool(f.get("numbers_added") or f.get("names_added") or f.get("quotes_added") or f.get("narrator_added"))


def render(report):
    lines = ["write-human check: places to look, not verdicts. Not an AI detector.", ""]
    f = report.get("fidelity")
    if f:
        lines.append("FIDELITY (rewrite against the draft)")
        lines.append("  numbers not in the draft : %s" % (", ".join(f["numbers_added"]) or "none"))
        lines.append("  numbers dropped          : %s" % (", ".join(f["numbers_dropped"]) or "none"))
        lines.append("  names not in the draft   : %s" % (", ".join(f["names_added"]) or "none"))
        lines.append("  quotes not in the draft  : %s" % ("; ".join(f["quotes_added"]) or "none"))
        lines.append("  hedges dropped           : %s" % (", ".join(f["hedges_dropped"]) or "none"))
        lines.append("  hedges added             : %s" % (", ".join(f["hedges_added"]) or "none"))
        lines.append("  narrator added           : %s" % ("YES, the draft has no 'I'" if f["narrator_added"] else "no"))
        note = "" if 0.75 <= f["length_ratio"] <= 1.2 else "  (far from the draft's length: summarised or padded?)"
        lines.append("  length vs draft          : %sx%s" % (f["length_ratio"], note))
        lines.append("  A number produced by arithmetic on the draft's own figures is fine. Check each one.")
        lines.append("  A dropped hedge may be harmless rewording, or a claim made stronger than the draft made it.")
        lines.append("")
    r = report["rhythm"]
    lines.append("RHYTHM")
    lines.append("  sentences %d, mean %s words, variation %s%s" % (
        r["sentences"], r["mean_len"], r["cv"],
        "  (even: under 0.4)" if r["sentences"] >= 5 and r["cv"] < 0.4 else ""))
    lines.append("  longest run of same-length sentences: %d%s" % (
        r["longest_even_run"], "  (break it up)" if r["longest_even_run"] >= 4 else ""))
    if r["paragraphs"] >= 3:
        lines.append("  paragraphs %d, length variation %s%s" % (
            r["paragraphs"], r["paragraph_cv"], "  (same-size blocks)" if r["paragraph_cv"] < 0.25 else ""))
    if "source_rhythm" in report:
        lines.append("  draft variation was %s" % report["source_rhythm"]["cv"])
    lines.append("")
    t = report["tells"]
    lines.append("TELLS")
    lines.append("  em dashes        : %d" % t["em_dashes"])
    for key in ("lexicon", "padding", "staged_contrast", "reasoning_markers", "closers"):
        lines.append("  %-17s: %s" % (key.replace("_", " "), ", ".join(sorted(set(t[key]))) or "none"))
    lines.append("  possible triads  : %d" % t["triads"])
    for key, title, label in (
        ("voice", "VOICE (rewrite against the writing sample)", "sample"),
        ("context_voice", "VOICE (rewrite against the surrounding text)", "page"),
    ):
        if key in report:
            lines.append("")
            lines.append(title)
            for row in report[key]:
                lines.append("  %-26s %s %-6s rewrite %-6s %s" % (
                    row["metric"], label, row["sample"], row["rewrite"], "<- differs" if row["flag"] else ""))
    return "\n".join(lines)


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        sys.stderr.write("check.py: cannot read %s: %s\n" % (path, error))
        raise SystemExit(2)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Mechanical checks for a write-human rewrite.")
    parser.add_argument("rewrite", help="file holding the rewritten text")
    parser.add_argument("--source", help="file holding the original draft (enables the fidelity check)")
    parser.add_argument("--sample", help="file holding the author's own writing (enables the voice check)")
    parser.add_argument("--context", help="file holding the paragraphs around the passage (voice check against the page)")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    parser.add_argument("--strict", action="store_true", help="exit 1 if the fidelity check finds additions")
    args = parser.parse_args(argv)
    report = build_report(
        read(args.rewrite),
        read(args.source) if args.source else None,
        read(args.sample) if args.sample else None,
        read(args.context) if args.context else None,
    )
    print(json.dumps(report, indent=2) if args.json else render(report))
    return 1 if args.strict and fidelity_failed(report) else 0


if __name__ == "__main__":
    sys.exit(main())
