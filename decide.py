"""Weekly decision helper: this round's top candidates + their downstream effect.

For each of the top-K picks by win probability this round, force it, then solve
the optimal continuation — so you can see how spending that team NOW reshapes the
rest of your route (and what future slot you give up).

    python decide.py [round=1] [horizon=12] [K=3]
"""
import math
import sys

from lms.ingest import CANON
from lms.matrix import build_matrix
from lms.planner import _optimal, plan, survival_curve


def plan_forcing(first, horizon, start, cells):
    """Play `first` at `start`, then optimal continuation. -> (route, total_log)."""
    c0 = cells[(first, start)]
    rest_teams = [t for t in CANON if t != first]
    rest, rest_total = _optimal(cells, rest_teams, list(range(start + 1, start + horizon)))
    route = {start: {"team": first, "pwin": c0["pwin"], "opp": c0["opp"],
                     "home": c0["home"], "src": c0["src"]}}
    route.update(rest)
    return route, math.log(c0["pwin"]) + rest_total


def fx(c):
    return ("vs " if c["home"] else "@ ") + c["opp"]


def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    horizon = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    K = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    cells = build_matrix()

    base, _ = plan(horizon=horizon, start=start, cells=cells)
    natural = {base[r]["team"]: r for r in base}     # where the free plan uses each team

    this = sorted(((t, c) for (t, r), c in cells.items() if r == start),
                  key=lambda x: -x[1]["pwin"])[:K]

    print(f"ROUND {start} — top {K} picks and their knock-on effect "
          f"(horizon {horizon})\n")
    ranked = []
    for team, c in this:
        route, total = plan_forcing(team, horizon, start, cells)
        curve = {r: a for r, _, _, a in survival_curve(route)}
        ranked.append((team, c, route, total, curve))

    best_total = max(r[3] for r in ranked)
    for team, c, route, total, curve in ranked:
        src = "odds" if c["src"] == "odds" else "proj"
        nat = natural.get(team)
        gap = total - best_total
        tag = "  <-- best continuation" if abs(gap) < 1e-9 else f"  ({gap:+.3f})"
        print(f"> {team}  {fx(c)}  {c['pwin']*100:.0f}%  [{src}]{tag}")
        nxt = [r for r in sorted(route) if r > start][:5]
        trail = "  ".join(f"R{r}:{route[r]['team']}({route[r]['pwin']*100:.0f})"
                          for r in nxt)
        print(f"    then: {trail}")
        print(f"    survival: " + " ".join(
            f"R{k} {curve[k]*100:.0f}%" for k in (start+3, start+5, start+7, start+9)
            if k in curve))
        if nat is not None and nat != start:
            saved = base[nat]
            print(f"    (spending {team} now forgoes its plan slot: "
                  f"R{nat} {fx(saved)} {saved['pwin']*100:.0f}%)")
        print()


if __name__ == "__main__":
    main()
