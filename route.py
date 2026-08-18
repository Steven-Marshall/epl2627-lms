"""Full planned route with a 1st and 2nd pick each round.

1st = the optimal-route assignment (save-aware). 2nd = the best legal fallback
that week — highest win-prob team still available, having spent the earlier 1st
picks. (The 2nd may be a team the plan saves for a later round; treat it as
"if not the plan pick, this.")

    python route.py [start=1] [horizon=12]
"""
import sys

from lms.matrix import build_matrix
from lms.planner import plan


def fx(cell):
    return ("vs " if cell["home"] else "@ ") + cell["opp"]


def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    horizon = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    cells = build_matrix()
    route, _ = plan(horizon=horizon, start=start, cells=cells)

    print(f"PLANNED ROUTE from round {start} — 1st (plan) & 2nd (best available alt)\n")
    print(f"  {'rnd':>3}  {'1st pick':<18}{'fixture':<18}{'P':>6}   "
          f"{'2nd pick':<18}{'fixture':<18}{'P':>6}")
    print("  " + "-" * 90)
    spent = set()  # teams used by the plan's 1st picks in earlier rounds
    for rnd in sorted(route):
        first = route[rnd]
        # 2nd = best team playing this round you still hold (not the 1st, not spent)
        alts = [(t, c) for (t, r), c in cells.items()
                if r == rnd and t != first["team"] and t not in spent]
        alts.sort(key=lambda x: -x[1]["pwin"])
        second = alts[0] if alts else None
        f_fx, f_p = fx(first), first["pwin"]
        if second:
            s_t, s_c = second
            # mark: the alt is STRONGER than the plan pick -> plan is saving it
            mark = " *" if s_c["pwin"] > f_p else ""
            s_line = f"{s_t:<18}{fx(s_c):<18}{s_c['pwin']*100:>5.0f}%{mark}"
        else:
            s_line = "-"
        print(f"  {rnd:>3}  {first['team']:<18}{f_fx:<18}{f_p*100:>5.0f}%   {s_line}")
        spent.add(first["team"])
    print("\n  * the alternative outrates the plan pick — the plan is deliberately "
          "saving that team for a better round.")


if __name__ == "__main__":
    main()
