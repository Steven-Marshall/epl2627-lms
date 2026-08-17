"""Recommended survival plan + harvest-vs-save analysis for the current round.

    python plan.py [start_round] [horizon]
"""
import sys

from lms.matrix import build_matrix
from lms.planner import plan, route_value, survival_curve


def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    horizon = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    cells = build_matrix()

    plan_by_round, total = plan(horizon=horizon, start=start, cells=cells)

    print(f"OPTIMAL ROUTE from round {start} (horizon {horizon}, "
          f"maximise product of win probs)\n")
    print(f"  {'rnd':>3}  {'team':<18}{'fixture':<20}{'P(win)':>7}  src")
    print("  " + "-" * 55)
    for rnd in sorted(plan_by_round):
        p = plan_by_round[rnd]
        fx = ("vs " if p["home"] else "@ ") + p["opp"]
        print(f"  {rnd:>3}  {p['team']:<18}{fx:<20}{p['pwin']*100:>6.1f}%  {p['src']}")

    print("\nHARVEST vs SAVE — route value of each alternative FIRST pick "
          f"(round {start}):\n")
    cands = sorted(
        ((t, *route_value(t, horizon=horizon, start=start, cells=cells))
         for t in {plan_by_round[start]["team"]} | _top_now(cells, start)),
        key=lambda r: -r[1])
    best = cands[0][1]
    print(f"  {'first pick':<18}{'P(win) now':>11}{'route value':>13}{'vs best':>9}")
    print("  " + "-" * 51)
    for t, val, p0 in cands:
        mark = "  <- pick" if abs(val - best) < 1e-9 else ""
        print(f"  {t:<18}{p0*100:>10.1f}%{val:>13.3f}{(val-best):>+9.3f}{mark}")

    print("\nSURVIVAL (3 lives, out on 3rd non-win) along the optimal route:\n")
    print(f"  {'rnd':>3}  {'team':<18}{'P(win)':>7}{'P(alive)':>10}")
    print("  " + "-" * 41)
    for rnd, team, pw, alive in survival_curve(plan_by_round):
        print(f"  {rnd:>3}  {team:<18}{pw*100:>6.1f}%{alive*100:>9.1f}%")


def _top_now(cells, start, k=5):
    """The k highest-win-prob teams available this round (candidate first picks)."""
    this = [(t, c["pwin"]) for (t, r), c in cells.items() if r == start]
    return {t for t, _ in sorted(this, key=lambda x: -x[1])[:k]}


if __name__ == "__main__":
    main()
