import unittest

from cipherlab import caesar


class TestCaesar(unittest.TestCase):
    def test_encode_basic_shift(self):
        self.assertEqual(caesar.encode("ABC", 1), "BCD")

    def test_encode_wraps_around_alphabet(self):
        self.assertEqual(caesar.encode("XYZ", 3), "ABC")

    def test_encode_preserves_case(self):
        self.assertEqual(caesar.encode("Hello, World!", 3), "Khoor, Zruog!")

    def test_encode_leaves_non_letters_untouched(self):
        self.assertEqual(caesar.encode("123 !@#", 5), "123 !@#")

    def test_decode_reverses_encode(self):
        original = "The Quick Brown Fox Jumps Over The Lazy Dog!"
        for shift in range(-30, 30):
            with self.subTest(shift=shift):
                self.assertEqual(caesar.decode(caesar.encode(original, shift), shift), original)

    def test_negative_shift(self):
        self.assertEqual(caesar.encode("ABC", -1), "ZAB")

    def test_shift_larger_than_alphabet(self):
        # 29 and 3 are equivalent mod 26
        self.assertEqual(caesar.encode("ABC", 29), caesar.encode("ABC", 3))

    def test_zero_shift_is_identity(self):
        self.assertEqual(caesar.encode("Anything Goes 123", 0), "Anything Goes 123")


if __name__ == "__main__":
    unittest.main()
