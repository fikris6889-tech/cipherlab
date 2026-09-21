import unittest

from cipherlab import vigenere


class TestVigenere(unittest.TestCase):
    def test_textbook_example(self):
        self.assertEqual(vigenere.encode("Attack at dawn", "LEMON"), "Lxfopv ef rnhr")

    def test_decode_reverses_encode(self):
        self.assertEqual(vigenere.decode("Lxfopv ef rnhr", "LEMON"), "Attack at dawn")

    def test_round_trip_with_punctuation_and_spaces(self):
        original = "Meet me at the old bridge, midnight!"
        key = "shadow"
        ciphertext = vigenere.encode(original, key)
        self.assertEqual(vigenere.decode(ciphertext, key), original)
        # Sanity check the round trip actually changed the text.
        self.assertNotEqual(ciphertext, original)

    def test_key_case_is_irrelevant(self):
        self.assertEqual(vigenere.encode("HELLO", "key"), vigenere.encode("HELLO", "KEY"))

    def test_key_with_non_letters_ignores_them(self):
        # "k-e-y" should behave identically to "key": punctuation in the
        # key is stripped out rather than treated as a zero-shift.
        self.assertEqual(vigenere.encode("HELLO WORLD", "k-e-y"), vigenere.encode("HELLO WORLD", "key"))

    def test_non_letters_do_not_consume_key_position(self):
        # If spaces advanced the key index, encoding "AA AA" with key "AB"
        # would NOT come back cleanly matched to encoding "AAAA" position-
        # by-position. This test guards the exact bug described in the
        # module docstring.
        no_space = vigenere.encode("AAAA", "AB")
        with_space = vigenere.encode("AA AA", "AB").replace(" ", "")
        self.assertEqual(no_space, with_space)

    def test_empty_key_raises(self):
        with self.assertRaises(ValueError):
            vigenere.encode("HELLO", "")

    def test_key_with_no_letters_raises(self):
        with self.assertRaises(ValueError):
            vigenere.encode("HELLO", "1234!!!")


if __name__ == "__main__":
    unittest.main()
