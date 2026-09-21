# CipherLab

A tiny, zero-dependency Python toolkit for classical substitution ciphers:

- **Caesar cipher** - encode/decode with a fixed shift
- **Vigenère cipher** - encode/decode with a repeating keyword
- **Automatic Caesar cracker** - breaks a Caesar cipher with *no key given*, using letter-frequency (chi-squared) statistics

Pure Python 3 standard library. No `pip install` needed - just clone and run.

## Requirements

Python 3.9+ (uses `from __future__ import annotations` and modern type hints).

## Project layout

```
cipherlab/
    __init__.py
    caesar.py      # Caesar cipher encode/decode
    vigenere.py    # Vigenère cipher encode/decode
    frequency.py   # English letter-frequency table + chi-squared scoring
    cracker.py     # Brute-force Caesar cracker built on frequency.py
    cli.py         # argparse command-line interface
tests/
    test_caesar.py
    test_vigenere.py
    test_frequency.py
    test_cracker.py
```

## Usage

Run everything as a module from the project root (so Python resolves the
`cipherlab` package correctly):

```bash
# Caesar cipher
python3 -m cipherlab.cli caesar-encode "Meet me at midnight" 7
python3 -m cipherlab.cli caesar-decode "Tlla tl ha tpkupnoa" 7

# Vigenère cipher
python3 -m cipherlab.cli vigenere-encode "Attack at dawn" LEMON
python3 -m cipherlab.cli vigenere-decode "Lxfopv ef rnhr" LEMON

# Crack a Caesar cipher with NO key - frequency analysis figures it out
python3 -m cipherlab.cli crack "Wkh vhfuhw phhwlqj lv dw plgqljkw" --show-top 3
```

## Running the tests

```bash
python3 -m unittest discover -s tests -v
```

26 tests, all passing, covering: round-trip correctness, case preservation,
punctuation/space handling, key normalization edge cases, the chi-squared
scorer, and the cracker (including its honestly-documented limitation on
very short ciphertexts - see `tests/test_cracker.py`).

Doctest examples embedded in the module docstrings can be run with:

```bash
python3 -c "import doctest; from cipherlab import caesar, vigenere, cracker; [print(m.__name__, doctest.testmod(m)) for m in (caesar, vigenere, cracker)]"
```

## How the automatic cracker works

1. There are only 26 possible Caesar shifts - brute force all of them.
2. For each candidate decode, score it with a chi-squared statistic that
   compares its letter frequencies against known English letter frequencies.
3. Return the lowest-scoring (most English-like) candidate.

This only works on **Caesar** ciphers directly. Cracking Vigenère needs an
extra first step - figuring out the key length (classically via the
Kasiski examination or the index of coincidence) - and is left as a great
follow-up exercise once you're comfortable with this codebase.

## GitHub repo

Code is written, tested, and committed **locally** in this repo
(`daily-teaching-series`). Push to GitHub is pending Frank's manual
`git push` from his machine, since this automation's network egress
blocks github.com. Once pushed, this project will be live at:
<https://github.com/fikris6889-tech/daily-teaching-series>
