"""
cracker.py
----------

Automatically break a Caesar cipher WITHOUT knowing the shift, using
nothing but letter-frequency statistics.

The approach ("brute force + scoring", a pattern that shows up
everywhere in programming, not just cryptography):

1. There are only 26 possible shifts. Just try all of them.
2. For each candidate decode, score how "English-like" the result is
   using the chi-squared statistic from frequency.py.
3. Return the candidate with the LOWEST score (best fit to English).

This is deliberately simple - no machine learning, no dictionaries,
just statistics - and it is genuinely how early 20th-century
cryptanalysts thought about the problem before computers could just
try every dictionary word.

Note this only cracks CAESAR ciphers. Cracking Vigenère requires first
figuring out the key LENGTH (classically via the Kasiski examination
or the index of coincidence) and then treating each of the N key
positions as its own independent Caesar cipher - a great "Day 2"
extension exercise for readers who finish this project early.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import caesar
from .frequency import chi_squared_score

TOTAL_SHIFTS = 26


@dataclass(frozen=True)
class CrackResult:
    """The best guess produced by `crack_caesar`, plus the full ranking."""

    shift: int
    plaintext: str
    score: float
    all_candidates: tuple[tuple[int, str, float], ...]


def crack_caesar(ciphertext: str) -> CrackResult:
    """Find the most likely Caesar shift used to encode `ciphertext`.

    Returns a CrackResult with the winning shift/plaintext/score, and
    `all_candidates` (a tuple of (shift, plaintext, score) for every
    shift 0-25, sorted best-score-first) so callers/tests can inspect
    the runner-ups too.

    Note: this needs a reasonably long ciphertext to work reliably.
    Frequency analysis is a statistical technique, and a message with
    only a handful of letters doesn't carry enough signal - see
    tests/test_cracker.py::test_short_ciphertext_can_fool_the_cracker
    for a worked example of exactly that failure mode.

    >>> crack_caesar(caesar.encode(
    ...     "Statistics rewards patience: the more letters you feed it, "
    ...     "the more reliably the true shift rises to the top", 11
    ... )).shift
    11
    """
    if not ciphertext:
        raise ValueError("Cannot crack an empty ciphertext")

    candidates = []
    for shift in range(TOTAL_SHIFTS):
        plaintext = caesar.decode(ciphertext, shift)
        score = chi_squared_score(plaintext)
        candidates.append((shift, plaintext, score))

    candidates.sort(key=lambda item: item[2])
    best_shift, best_plaintext, best_score = candidates[0]

    return CrackResult(
        shift=best_shift,
        plaintext=best_plaintext,
        score=best_score,
        all_candidates=tuple(candidates),
    )
