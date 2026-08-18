"""Toxic-asset disposal: when do the weakest teams get their least-bad games?

Under no-repick, a deep run forces you to field weak teams eventually. Their value
is highest at their best fixture (usually home to a fellow minnow) — so you'd want
to spend them THERE, not be cornered into an away trip at a big side later. This
lists each bottom-N team's best 'disposal windows' and its worst forced spots, so
you can earmark when to use them up.

    python weak.py [N=5] [last_round=19]
"""
import sys

from lms.matrix import build_matrix
from lms.strength import ratings


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    last = int(sys.argv[2]) if len(sys.argv) > 2 else 19
    cells = build_matrix()
    R = ratings()
    bottom = sorted(R, key=R.get)[:N]  # weakest first

    def label(p):
        if p >= 0.45:
            return "coinflip - DUMP HERE"
        if p >= 0.35:
            return "playable"
        return "sacrifice"

    for team in bottom:
        games = sorted(((rnd, cells[(team, rnd)]) for rnd in range(1, last + 1)),
                       key=lambda x: -x[1]["pwin"])
        best = games[:4]
        worst = games[-2:]
        spread = best[0][1]["pwin"] - worst[-1][1]["pwin"]
        print(f"\n{team}  (rating {R[team]:.0f})   best-vs-worst swing: "
              f"{spread*100:.0f} pts")
        print(f"  best windows (rounds 1-{last}):")
        for rnd, c in best:
            fx = ("vs " if c["home"] else "@ ") + c["opp"]
            src = "odds" if c["src"] == "odds" else ""
            print(f"    R{rnd:<3}{fx:<20}{c['pwin']*100:>5.0f}%   "
                  f"{label(c['pwin'])} {src}")
        print(f"  worst forced spots:")
        for rnd, c in worst:
            fx = ("vs " if c["home"] else "@ ") + c["opp"]
            print(f"    R{rnd:<3}{fx:<20}{c['pwin']*100:>5.0f}%")


if __name__ == "__main__":
    main()
