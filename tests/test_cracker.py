import unittest

from cipherlab import caesar
from cipherlab.cracker import crack_caesar


class TestCracker(unittest.TestCase):
    def test_cracks_known_shift(self):
        # NOTE: this needs a reasonably long sample. Chi-squared scoring
        # is a statistical technique - with only a handful of letters
        # (e.g. "Hello, World!" has just 10), random noise can make a
        # WRONG shift score better than the real one by pure chance.
        # See test_short_ciphertext_can_fool_the_cracker below, which
        # documents that limitation instead of hiding it.
        plaintext = (
            "Hello there, this is a reasonably long test sentence so that "
            "letter frequency analysis has enough data to work with"
        )
        ciphertext = caesar.encode(plaintext, 3)
        result = crack_caesar(ciphertext)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(result.shift, 3)

    def test_short_ciphertext_can_fool_the_cracker(self):
        # This is a documented LIMITATION, not a bug: frequency analysis
        # is statistics, and statistics needs a big enough sample. A
        # 10-letter message doesn't carry enough signal to reliably beat
        # random chance. We assert the known, reproducible outcome here
        # (shift 6 currently wins over the true shift 3) specifically so
        # that if anyone "fixes" the scoring in a way that changes this,
        # they'll notice and can decide whether that's actually better.
        ciphertext = caesar.encode("Hello, World!", 3)
        result = crack_caesar(ciphertext)
        self.assertNotEqual(result.shift, 3)
        # The correct answer is still in there somewhere near the top,
        # just not guaranteed to be #1 - that's the whole point.
        top_shifts = [shift for shift, _, _ in result.all_candidates[:3]]
        self.assertIn(3, top_shifts)

    def test_cracks_longer_more_realistic_text_at_every_shift(self):
        plaintext = (
            "In cryptography a Caesar cipher is one of the simplest and most "
            "widely known encryption techniques. It is a type of substitution "
            "cipher in which each letter in the plaintext is replaced by a "
            "letter some fixed number of positions down the alphabet"
        )
        for shift in range(1, 26):
            with self.subTest(shift=shift):
                ciphertext = caesar.encode(plaintext, shift)
                result = crack_caesar(ciphertext)
                self.assertEqual(result.plaintext, plaintext)
                self.assertEqual(result.shift, shift)

    def test_all_candidates_are_sorted_best_first(self):
        ciphertext = caesar.encode("Statistics beats guessing every single time", 7)
        result = crack_caesar(ciphertext)
        scores = [score for _, _, score in result.all_candidates]
        self.assertEqual(scores, sorted(scores))
        self.assertEqual(len(result.all_candidates), 26)

    def test_empty_ciphertext_raises(self):
        with self.assertRaises(ValueError):
            crack_caesar("")


if __name__ == "__main__":
    unittest.main()
