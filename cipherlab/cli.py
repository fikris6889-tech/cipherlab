"""
cli.py
------

Command-line front door for the whole toolkit. Kept deliberately thin:
all the real logic lives in caesar.py / vigenere.py / cracker.py, and
this module's only job is to parse arguments and call into them. That
separation (business logic vs. CLI plumbing) is a habit worth building
early - it's what makes each piece independently testable, which is
exactly why tests/ never has to touch argparse at all.
"""

from __future__ import annotations

import argparse
import sys

from . import caesar, vigenere
from .cracker import crack_caesar


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cipherlab",
        description="Encode, decode, and crack classical substitution ciphers.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    caesar_enc = subparsers.add_parser("caesar-encode", help="Encode text with a Caesar cipher")
    caesar_enc.add_argument("text", help="Plaintext to encode")
    caesar_enc.add_argument("shift", type=int, help="Shift amount, e.g. 3")

    caesar_dec = subparsers.add_parser("caesar-decode", help="Decode a Caesar-ciphered text")
    caesar_dec.add_argument("text", help="Ciphertext to decode")
    caesar_dec.add_argument("shift", type=int, help="Shift amount used to encode it")

    vig_enc = subparsers.add_parser("vigenere-encode", help="Encode text with a Vigenère cipher")
    vig_enc.add_argument("text", help="Plaintext to encode")
    vig_enc.add_argument("key", help="Keyword, letters only matter")

    vig_dec = subparsers.add_parser("vigenere-decode", help="Decode a Vigenère-ciphered text")
    vig_dec.add_argument("text", help="Ciphertext to decode")
    vig_dec.add_argument("key", help="Keyword used to encode it")

    crack = subparsers.add_parser(
        "crack", help="Automatically crack a Caesar-ciphered text (no key needed!)"
    )
    crack.add_argument("text", help="Ciphertext to crack")
    crack.add_argument(
        "--show-top",
        type=int,
        default=1,
        help="Show this many top candidate decodes, best first (default: 1)",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "caesar-encode":
        print(caesar.encode(args.text, args.shift))
    elif args.command == "caesar-decode":
        print(caesar.decode(args.text, args.shift))
    elif args.command == "vigenere-encode":
        print(vigenere.encode(args.text, args.key))
    elif args.command == "vigenere-decode":
        print(vigenere.decode(args.text, args.key))
    elif args.command == "crack":
        result = crack_caesar(args.text)
        top_n = max(1, args.show_top)
        for rank, (shift, plaintext, score) in enumerate(result.all_candidates[:top_n], start=1):
            marker = "-> " if rank == 1 else "   "
            print(f"{marker}#{rank} shift={shift:>2}  score={score:7.2f}  {plaintext}")
    else:  # pragma: no cover - argparse `required=True` prevents this
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
