"""Field picture for a round: how the pool split, and the correlation risk.

    python field.py [round]
"""
import sys
from collections import Counter

from lms.matrix import build_matrix
from lms.tracking import load_picks


def main():
    rows = load_picks()
    if not rows:
        print("No picks logged.")
        return
    rnd = int(sys.argv[1]) if len(sys.argv) > 1 else max(r["round"] for r in rows)
    picks = [r for r in rows if r["round"] == rnd]
    n = len(picks)
    cells = build_matrix()
    tally = Counter(p["team"] for p in picks)

    print(f"FIELD — Round {rnd}  ({n} picks)\n")
    print(f"  {'team':<16}{'n':>3}{'field%':>8}{'P(win)':>8}   if it fails")
    print("  " + "-" * 52)
    exp_lifeloss = 0.0
    for team, c in sorted(tally.items(), key=lambda kv: -kv[1]):
        pw = cells[(team, rnd)]["pwin"] if (team, rnd) in cells else float("nan")
        exp_lifeloss += c * (1 - pw)
        risk = f"{c} players lose a life" if c >= 3 else ""
        print(f"  {team:<16}{c:>3}{c/n*100:>7.0f}%{pw*100:>7.0f}%   {risk}")

    top_team, top_n = tally.most_common(1)[0]
    print(f"\n  Concentration: {top_n}/{n} ({top_n/n*100:.0f}%) on {top_team}.")
    print(f"  Expected life-losses across the field this round: {exp_lifeloss:.1f}")


if __name__ == "__main__":
    main()
