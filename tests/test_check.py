import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check  # noqa: E402

SOURCE = (
    "After 9 years in banking, I left my role in March to open a bakery called "
    "Crumb & Co. in Leeds. Within six weeks, we had 85 subscribers."
)


class SplitSentences(unittest.TestCase):
    def test_splits_on_terminal_punctuation(self):
        self.assertEqual(
            check.split_sentences("It broke. Why? Nobody knew! We fixed it."),
            ["It broke.", "Why?", "Nobody knew!", "We fixed it."],
        )

    def test_abbreviations_do_not_split(self):
        sents = check.split_sentences("Dr. Rao joined Crumb & Co. in Leeds. She stayed.")
        self.assertEqual(len(sents), 2)

    def test_company_suffix_ends_a_sentence_before_a_capital(self):
        self.assertEqual(
            check.split_sentences("We hired Acme Inc. They delivered. No. We stopped."),
            ["We hired Acme Inc.", "They delivered.", "No.", "We stopped."],
        )

    def test_code_blocks_are_ignored(self):
        text = "Call the endpoint.\n\n```\nx = 1. Y = 2. Z = 3.\n```\n\nThen wait."
        self.assertEqual(len(check.split_sentences(text)), 2)


class Rhythm(unittest.TestCase):
    def test_uniform_sentences_have_low_variation_and_a_long_even_run(self):
        text = " ".join(["The cat sat on the mat."] * 6)
        r = check.rhythm(text)
        self.assertEqual(r["sentences"], 6)
        self.assertEqual(r["cv"], 0.0)
        self.assertEqual(r["longest_even_run"], 6)

    def test_varied_sentences_score_higher(self):
        text = (
            "No. The second sentence here runs a good deal longer than the first one "
            "did, with a clause attached. Short again. Then another long, winding "
            "sentence that takes its time getting anywhere at all."
        )
        r = check.rhythm(text)
        self.assertGreater(r["cv"], 0.6)
        self.assertLess(r["longest_even_run"], 3)


class Tells(unittest.TestCase):
    def test_finds_each_category(self):
        text = (
            "Furthermore, we leverage a robust platform — it's not just a tool, "
            "it's a partner. Upon closer examination, this holds. What's holding you back?"
        )
        t = check.tells(text)
        self.assertEqual(t["em_dashes"], 1)
        self.assertIn("leverage", t["lexicon"])
        self.assertIn("robust", t["lexicon"])
        self.assertTrue(t["padding"])
        self.assertTrue(t["staged_contrast"])
        self.assertTrue(t["reasoning_markers"])
        self.assertTrue(t["closers"])

    def test_clean_text_has_no_hits(self):
        t = check.tells("We moved the cache in front of the database. Load dropped.")
        self.assertEqual(t["em_dashes"], 0)
        for key in ("lexicon", "padding", "staged_contrast", "reasoning_markers", "closers"):
            self.assertEqual(t[key], [])


class Fidelity(unittest.TestCase):
    def test_faithful_rewrite_is_clean(self):
        rewrite = (
            "I spent nine years in banking. In March I left to open Crumb & Co., a "
            "bakery in Leeds. Six weeks in we had 85 subscribers."
        )
        f = check.fidelity(SOURCE, rewrite)
        self.assertEqual(f["numbers_added"], [])
        self.assertEqual(f["numbers_dropped"], [])
        self.assertEqual(f["names_added"], [])
        self.assertFalse(f["narrator_added"])

    def test_flags_invented_numbers_names_and_quotes(self):
        rewrite = (
            "After 9 years in banking I left in March and opened Crumb & Co. in Leeds. "
            'By Friday we had 85 subscribers and a note from Priya saying "best loaf '
            'in Yorkshire". That took 12 days.'
        )
        f = check.fidelity(SOURCE, rewrite)
        self.assertEqual(f["numbers_added"], ["12"])
        self.assertEqual(f["numbers_dropped"], ["6"])
        self.assertIn("Friday", f["names_added"])
        self.assertIn("Priya", f["names_added"])
        self.assertIn("Yorkshire", f["names_added"])
        self.assertEqual(f["quotes_added"], ["best loaf in Yorkshire"])

    def test_spelled_numbers_match_digits(self):
        f = check.fidelity("We hired twenty-two people in 3 months.", "22 hires in three months.")
        self.assertEqual(f["numbers_added"], [])
        self.assertEqual(f["numbers_dropped"], [])

    def test_scale_words_multiply(self):
        f = check.fidelity("We hired two hundred people for 3 million.", "200 hires, 3,000,000 spent.")
        self.assertEqual(f["numbers_added"], [])
        self.assertEqual(f["numbers_dropped"], [])

    def test_equal_values_in_different_notation_match(self):
        f = check.fidelity("The price was 5.0 and the tax 40%.", "Price 5, tax 40 percent.")
        self.assertEqual(f["numbers_added"], [])
        self.assertEqual(f["numbers_dropped"], [])

    def test_numbers_inside_code_are_checked(self):
        f = check.fidelity("A value of `42` is required.", "A value of `99` is required.")
        self.assertEqual(f["numbers_added"], ["99"])
        self.assertEqual(f["numbers_dropped"], ["42"])

    def test_turning_a_claim_into_a_quotation_is_flagged(self):
        f = check.fidelity("The claim is false.", 'She said "the claim is false".')
        self.assertEqual(f["quotes_added"], ["the claim is false"])

    def test_a_quotation_the_draft_already_had_is_not_flagged(self):
        f = check.fidelity('He called it "a mess" on day one.', 'On day one he called it "a mess".')
        self.assertEqual(f["quotes_added"], [])

    def test_dropped_hedges_are_counted(self):
        f = check.fidelity(
            "The trial suggests shorter shifts may reduce errors, provided six pickers are hired.",
            "Shorter shifts reduce errors. Hire six pickers.",
        )
        self.assertEqual(f["hedges_dropped"], ["may", "provided", "suggests"])
        self.assertEqual(f["hedges_added"], [])

    def test_kept_hedges_are_not_flagged(self):
        f = check.fidelity(
            "This appears to help, and it might last.", "It appears to help. It might last."
        )
        self.assertEqual(f["hedges_dropped"], [])

    def test_contracting_a_modal_is_not_a_dropped_hedge(self):
        f = check.fidelity(
            "We could not reproduce it and it cannot be ruled out.",
            "We couldn’t reproduce it and it can't be ruled out.",
        )
        self.assertEqual(f["hedges_dropped"], [])
        self.assertEqual(f["hedges_added"], [])

    def test_profile_survives_text_with_no_words(self):
        self.assertEqual(check.profile("--- 123 456")["mean_word_len"], 0.0)

    def test_added_hedges_are_counted(self):
        f = check.fidelity("The cache cut latency.", "The cache probably cut latency.")
        self.assertEqual(f["hedges_added"], ["probably"])

    def test_flags_a_narrator_the_source_did_not_have(self):
        f = check.fidelity(
            "Caching reduces database load.", "I have found that caching reduces database load."
        )
        self.assertTrue(f["narrator_added"])

    def test_length_ratio(self):
        f = check.fidelity("one two three four", "one two")
        self.assertEqual(f["length_ratio"], 0.5)


class Profile(unittest.TestCase):
    CASUAL = (
        "Honestly I almost didn't post this. I'm not a writer. I'm a guy who bakes "
        "and who keeps a spreadsheet of everything. Anyway. It's fine, I think."
    )
    FORMAL = (
        "The organisation has determined that the proposed adjustment will require "
        "additional review by the committee. The committee will convene in the "
        "following quarter to assess the available evidence and reach a decision."
    )

    def test_profile_captures_voice_markers(self):
        casual, formal = check.profile(self.CASUAL), check.profile(self.FORMAL)
        self.assertGreater(casual["contractions_per_100w"], 5)
        self.assertEqual(formal["contractions_per_100w"], 0)
        self.assertGreater(casual["first_person_per_100w"], formal["first_person_per_100w"])
        self.assertLess(casual["mean_sentence_len"], formal["mean_sentence_len"])
        self.assertGreater(casual["fragment_share"], 0)

    def test_compare_flags_a_mismatch_and_passes_a_match(self):
        sample = check.profile(self.CASUAL)
        flagged = {row["metric"] for row in check.compare(sample, check.profile(self.FORMAL)) if row["flag"]}
        self.assertIn("contractions_per_100w", flagged)
        self.assertIn("mean_sentence_len", flagged)
        same = [row for row in check.compare(sample, check.profile(self.CASUAL)) if row["flag"]]
        self.assertEqual(same, [])


class Context(unittest.TestCase):
    def test_context_report_flags_a_passage_that_does_not_match_its_page(self):
        report = check.build_report(Profile.FORMAL, context=Profile.CASUAL)
        flagged = {row["metric"] for row in report["context_voice"] if row["flag"]}
        self.assertIn("contractions_per_100w", flagged)
        self.assertIn("mean_sentence_len", flagged)

    def test_profile_includes_word_length(self):
        self.assertGreater(
            check.profile(Profile.FORMAL)["mean_word_len"], check.profile(Profile.CASUAL)["mean_word_len"]
        )


class CommandLine(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check.py"), *args],
            capture_output=True,
            text=True,
        )

    def test_json_report_and_strict_exit_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp) / "src.txt", Path(tmp) / "out.txt"
            src.write_text(SOURCE, encoding="utf-8")
            out.write_text("After 9 years in banking I opened a bakery with 400 customers.", encoding="utf-8")
            result = self.run_cli(str(out), "--source", str(src), "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertIn("400", report["fidelity"]["numbers_added"])
            self.assertIn("rhythm", report)
            self.assertIn("tells", report)
            strict = self.run_cli(str(out), "--source", str(src), "--strict")
            self.assertEqual(strict.returncode, 1)

    def test_context_flag_adds_a_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            out, ctx = Path(tmp) / "out.txt", Path(tmp) / "ctx.txt"
            out.write_text(Profile.FORMAL, encoding="utf-8")
            ctx.write_text(Profile.CASUAL, encoding="utf-8")
            result = self.run_cli(str(out), "--context", str(ctx))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("surrounding text", result.stdout)

    def test_missing_file_is_a_clear_error(self):
        result = self.run_cli("/nonexistent/draft.txt")
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot read", result.stderr)


if __name__ == "__main__":
    unittest.main()
