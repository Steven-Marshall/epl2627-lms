"""Projected win prob vs real market odds for a round — how did the model do?

    python compare_round.py [round]
"""
import sys

from lms.matchodds import load_round
from lms.matrix import build_matrix
from lms.strength import ratings
from lms.winprob import win_prob


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    rows = load_round(n)
    if rows is None:
        print(f"No odds file for round {n}.")
        return
    R = ratings()

    recs = []
    for m in rows:
        for team, opp, home, pmkt in (
            (m["home"], m["away"], True, m["pH"]),
            (m["away"], m["home"], False, m["pA"]),
        ):
            pproj = win_prob(R[team], R[opp], home=home)
            recs.append((team, ("vs " if home else "@ ") + opp, pproj, pmkt))

    recs.sort(key=lambda x: -x[3])
    print(f"Round {n}: market P(win) vs projection (sorted by market)\n")
    print(f"  {'team':<18}{'fixture':<20}{'market':>8}{'proj':>8}{'delta':>8}")
    print("  " + "-" * 62)
    for team, fx, pproj, pmkt in recs:
        d = (pproj - pmkt) * 100
        flag = "  <-- " + ("proj HIGH" if d > 0 else "proj low") if abs(d) >= 6 else ""
        print(f"  {team:<18}{fx:<20}{pmkt*100:>7.1f}%{pproj*100:>7.1f}%{d:>+7.1f}{flag}")

    # LMS pick view: best survival picks this round from the sharp odds
    print(f"\nRound {n} — best survival picks (market P(win)):")
    picks = sorted(({"team": m["home"], "p": m["pH"], "fx": "vs " + m["away"]}
                    for m in rows), key=lambda r: -r["p"])
    picks += sorted(({"team": m["away"], "p": m["pA"], "fx": "@ " + m["home"]}
                     for m in rows), key=lambda r: -r["p"])
    for r in sorted(picks, key=lambda r: -r["p"])[:6]:
        print(f"  {r['team']:<18}{r['fx']:<20}{r['p']*100:>6.1f}%")


if __name__ == "__main__":
    main()
