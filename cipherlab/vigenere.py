"""
vigenere.py
-----------

The Vigenère cipher is a Caesar cipher that uses a *different* shift
for each letter, taken from a repeating keyword instead of one fixed
number. It was considered unbreakable for roughly 300 years (it was
called "le chiffre indéchiffrable" - the indecipherable cipher) until
Kasiski and Babbage worked out how to attack it in the 1800s.

Key idea: each letter of the KEY tells you the shift for the
corresponding letter of the plaintext. If the key is "KEY" and the
plaintext is "HELLO":

    H  E  L  L  O
    K  E  Y  K  E     <- key repeats: K,E,Y,K,E
    +  +  +  +  +
    shift H by K(=10), E by E(=4), L by Y(=24), L by K(=10), O by E(=4)

The common beginner bug: advancing the key index on EVERY character,
including spaces and punctuation. That desyncs the key from the
letters as soon as the plaintext has a space in it. The fix (used
below) is to only advance the key index when we actually shift a
letter - non-alphabetic characters are copied through untouched and
do NOT consume a key position.
"""

from __future__ import annotations

from .caesar import _shift_char

ALPHABET_SIZE = 26


def _key_shifts(key: str) -> list[int]:
    """Turn a key string into a list of numeric shifts (A=0, B=1, ...).

    Non-alphabetic characters in the key are dropped entirely - only
    letters can define a shift.
    """
    shifts = [ord(c.lower()) - ord("a") for c in key if c.isalpha()]
    if not shifts:
        raise ValueError("Vigenère key must contain at least one letter")
    return shifts


def _apply(text: str, key: str, direction: int) -> str:
    """Shared implementation for encode/decode.

    `direction` is +1 to encode, -1 to decode.
    """
    shifts = _key_shifts(key)
    result_chars = []
    key_index = 0

    for char in text:
        if char.isalpha():
            shift = shifts[key_index % len(shifts)] * direction
            result_chars.append(_shift_char(char, shift))
            key_index += 1  # only letters advance the key
        else:
            result_chars.append(char)

    return "".join(result_chars)


def encode(text: str, key: str) -> str:
    """Encrypt `text` with a Vigenère cipher using `key`.

    >>> encode("Attack at dawn", "LEMON")
    'Lxfopv ef rnhr'
    """
    return _apply(text, key, direction=1)


def decode(text: str, key: str) -> str:
    """Decrypt `text` that was Vigenère-encoded with `key`.

    >>> decode("Lxfopv ef rnhr", "LEMON")
    'Attack at dawn'
    """
    return _apply(text, key, direction=-1)
