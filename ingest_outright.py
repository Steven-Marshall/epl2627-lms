"""Ingest pasted outright title odds.

Usage:
    1. Paste the block (however it comes off the page) into data/outright_raw.txt
    2. python ingest_outright.py

Parses the block, writes prices into data/teams.txt, and prints the vig-free
championship probabilities + a strength ranking. Flags anything it couldn't match
so a messy paste never fails silently.
"""
import os

from lms.ingest import CANON, parse_block, vig_free

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
RAW = os.path.join(DATA, "outright_raw.txt")
SHEET = os.path.join(DATA, "teams.txt")


def write_sheet(prices):
    lines = ["# EPL 2026/27 teams — human-edited sheet.",
             "# Columns: name | outright_odds (decimal, to win the league)",
             "#",
             "# name                 | outright"]
    for t in CANON:
        o = prices.get(t)
        lines.append(f"{t:<22}| {o if o is not None else ''}")
    with open(SHEET, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    if not os.path.exists(RAW):
        print(f"Paste the odds block into {RAW} first.")
        return
    with open(RAW, encoding="utf-8") as f:
        text = f.read()

    prices, unmatched = parse_block(text)
    probs = vig_free(prices)

    print(f"Parsed {len(prices)}/20 teams.")
    missing = [t for t in CANON if t not in prices]
    if missing:
        print("  MISSING (no price found):", ", ".join(missing))
    if unmatched:
        print("  UNMATCHED lines:")
        for ln in unmatched:
            print("    ", ln)

    over = sum(1.0 / o for o in prices.values())
    print(f"\n  Book overround: {(over - 1) * 100:+.1f}%  (sum of 1/odds = {over:.3f})")
    print(f"\n  {'team':<20}{'odds':>8}{'P(champ)':>11}")
    print("  " + "-" * 39)
    for t, p in sorted(probs.items(), key=lambda kv: -kv[1]):
        print(f"  {t:<20}{prices[t]:>8.2f}{p * 100:>10.1f}%")

    write_sheet(prices)
    print(f"\n  Wrote {SHEET}")


if __name__ == "__main__":
    main()
