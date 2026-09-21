"""
caesar.py
---------

The Caesar cipher: the "hello world" of cryptography. Every letter in
the plaintext is shifted a fixed number of places through the alphabet.
Shift by 3 and 'A' becomes 'D', 'B' becomes 'E', and so on, wrapping
back around from 'Z' to 'A'.

Design choices worth noticing (common beginner trip-ups called out
explicitly):

1. We preserve the ORIGINAL CASE of every letter. 'Hello' shifted by 3
   should stay looking like a word ('Khoor'), not turn into all
   uppercase or all lowercase.
2. Non-alphabetic characters (spaces, punctuation, digits, emoji...)
   pass through completely untouched. Only a-z/A-Z are shifted.
3. The shift wraps around using modulo 26, and Python's `%` operator
   already handles negative shifts correctly (e.g. -3 % 26 == 23), so
   `decode` can just be `encode` with a negated shift - no special
   casing required.
"""

from __future__ import annotations

ALPHABET_SIZE = 26


def _shift_char(char: str, shift: int) -> str:
    """Shift a single character by `shift` positions, preserving case.

    Non-letters are returned unchanged.
    """
    if char.isupper():
        base = ord("A")
    elif char.islower():
        base = ord("a")
    else:
        return char

    offset = ord(char) - base
    shifted = (offset + shift) % ALPHABET_SIZE
    return chr(base + shifted)


def encode(text: str, shift: int) -> str:
    """Encrypt `text` with a Caesar cipher of the given `shift`.

    >>> encode("Hello, World!", 3)
    'Khoor, Zruog!'
    """
    return "".join(_shift_char(c, shift) for c in text)


def decode(text: str, shift: int) -> str:
    """Decrypt `text` that was Caesar-encoded with the given `shift`.

    Decoding is just encoding with the shift negated - shifting
    forward by `shift` and then backward by `shift` returns you to
    where you started (that symmetry is what makes Caesar/Vigenère
    ciphers so simple to implement, and also so easy to break).

    >>> decode("Khoor, Zruog!", 3)
    'Hello, World!'
    """
    return encode(text, -shift)
