import unittest

from cipherlab.frequency import ENGLISH_FREQUENCIES, chi_squared_score, letter_counts


class TestFrequency(unittest.TestCase):
    def test_letter_counts_is_case_insensitive(self):
        counts = letter_counts("AaAa")
        self.assertEqual(counts["a"], 4)

    def test_letter_counts_ignores_non_letters(self):
        counts = letter_counts("a1 b2! c3?")
        self.assertEqual(sum(counts.values()), 3)

    def test_english_frequencies_sum_to_roughly_100(self):
        total = sum(ENGLISH_FREQUENCIES.values())
        self.assertAlmostEqual(total, 100.0, delta=0.5)

    def test_empty_text_scores_infinity(self):
        self.assertEqual(chi_squared_score("1234 !!!"), float("inf"))

    def test_real_english_scores_lower_than_gibberish(self):
        real_english = (
            "the quick brown fox jumps over the lazy dog while the sun "
            "sets slowly behind the hills and the wind begins to blow"
        )
        # A string dominated by rare letters (q, x, z, j) should score
        # much worse than natural English text.
        gibberish = "zzzqqqxxxjjjzzzqqqxxxjjjzzzqqqxxxjjj"

        self.assertLess(chi_squared_score(real_english), chi_squared_score(gibberish))


if __name__ == "__main__":
    unittest.main()
