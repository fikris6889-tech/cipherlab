"""
frequency.py
------------

Letter-frequency analysis: the statistical tool that makes classical
ciphers breakable. In any large chunk of normal English text, letters
don't show up equally often - 'E' shows up roughly 12.7% of the time,
while 'Z' shows up barely 0.07% of the time. A Caesar cipher just
*shifts* this whole frequency fingerprint - it doesn't hide it. So if
you count letter frequencies in the ciphertext and find the shift that
makes that fingerprint line up best with normal English, you've almost
certainly found the key. That's exactly what `cracker.py` does with
the tools defined here.
"""

from __future__ import annotations

from collections import Counter

# Standard relative frequencies (%) of letters in English text,
# widely published (e.g. Cornell University's classic letter-frequency
# tables based on large corpora). Values sum to ~100.
ENGLISH_FREQUENCIES: dict[str, float] = {
    "a": 8.167, "b": 1.492, "c": 2.782, "d": 4.253, "e": 12.702,
    "f": 2.228, "g": 2.015, "h": 6.094, "i": 6.966, "j": 0.153,
    "k": 0.772, "l": 4.025, "m": 2.406, "n": 6.749, "o": 7.507,
    "p": 1.929, "q": 0.095, "r": 5.987, "s": 6.327, "t": 9.056,
    "u": 2.758, "v": 0.978, "w": 2.360, "x": 0.150, "y": 1.974,
    "z": 0.074,
}

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def letter_counts(text: str) -> Counter:
    """Count occurrences of each letter a-z in `text`, case-insensitively.

    Non-alphabetic characters are ignored entirely - we only care
    about letters here.

    >>> letter_counts("Hello!")
    Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})
    """
    return Counter(c for c in text.lower() if c.isalpha())


def chi_squared_score(text: str) -> float:
    """Score how well `text`'s letter distribution matches English.

    Lower is better (closer to real English). This is the classic
    chi-squared goodness-of-fit statistic:

        sum over each letter of: (observed - expected)^2 / expected

    where `expected` is how many times we'd expect that letter to
    appear in a text this long, based on ENGLISH_FREQUENCIES, and
    `observed` is how many times it actually appears.

    We use chi-squared rather than something naive like "count the
    vowels" because it accounts for EVERY letter's frequency at once,
    including how rare letters like 'q', 'x', 'z' should almost never
    appear - a huge tell when a decode attempt is wrong.
    """
    counts = letter_counts(text)
    total_letters = sum(counts.values())
    if total_letters == 0:
        # No letters at all to score - treat as maximally un-English.
        return float("inf")

    score = 0.0
    for letter in ALPHABET:
        observed = counts.get(letter, 0)
        expected = ENGLISH_FREQUENCIES[letter] / 100.0 * total_letters
        if expected == 0:
            continue
        score += (observed - expected) ** 2 / expected

    return score
