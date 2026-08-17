"""Solo survival planner.

Under no-repick, picking a team spends it: its value now must beat the option
value of holding it for a softer future round. We solve that as an assignment
problem — choose distinct teams for the next `horizon` rounds to maximise the
product of win probabilities (== sum of log win-prob) — via the Hungarian
algorithm. The team assigned to the current round is the recommended pick; the
'harvest vs save' table shows the route value of each alternative first pick.

The 3-lives structure is scored separately as a survival curve over the plan.
"""
import math

from lms.ingest import CANON
from lms.matrix import build_matrix

NEG_INF_COST = 50.0  # cost for an impossible/zero-prob cell (-log guard)


def _cost(pwin):
    return -math.log(pwin) if pwin > 1e-9 else NEG_INF_COST


def _hungarian(cost):
    """Square cost-minimising assignment. Returns assign[row] = col."""
    n = len(cost)
    INF = float("inf")
    u = [0.0] * (n + 1)
    v = [0.0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = INF
            j1 = -1
            for j in range(1, n + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    assign = [0] * n
    for j in range(1, n + 1):
        if p[j] > 0:
            assign[p[j] - 1] = j - 1
    return assign


def _optimal(cells, teams, rounds):
    """Max-log-prob assignment of `teams` to `rounds` (each team <= once).

    Returns (plan_by_round, total_log_prob). Pads to a square matrix so leftover
    teams sit idle at zero cost.
    """
    n = len(teams)
    h = len(rounds)
    cost = [[0.0] * n for _ in range(n)]  # dummy rows (>=h) cost 0 everywhere
    for ri, rnd in enumerate(rounds):
        for ci, t in enumerate(teams):
            cost[ri][ci] = _cost(cells[(t, rnd)]["pwin"])
    assign = _hungarian(cost)
    plan, total = {}, 0.0
    for ri, rnd in enumerate(rounds):
        t = teams[assign[ri]]
        c = cells[(t, rnd)]
        plan[rnd] = {"team": t, "pwin": c["pwin"], "opp": c["opp"],
                     "home": c["home"], "src": c["src"]}
        total += math.log(c["pwin"]) if c["pwin"] > 1e-9 else -NEG_INF_COST
    return plan, total


def plan(horizon=12, used=None, start=1, cells=None):
    used = set(used or [])
    cells = cells if cells is not None else build_matrix()
    teams = [t for t in CANON if t not in used]
    rounds = list(range(start, start + horizon))
    return _optimal(cells, teams, rounds)


def route_value(first_pick, horizon=12, used=None, start=1, cells=None):
    """Total log-prob of forcing `first_pick` this round, then playing optimally."""
    used = set(used or [])
    cells = cells if cells is not None else build_matrix()
    p0 = cells[(first_pick, start)]["pwin"]
    rest_teams = [t for t in CANON if t not in used and t != first_pick]
    rest_rounds = list(range(start + 1, start + horizon))
    _, rest_total = _optimal(cells, rest_teams, rest_rounds)
    return math.log(p0) + rest_total, p0


def survival_curve(plan_by_round, lives=3):
    """P(still alive) after each round given the plan and `lives` (out on the
    `lives`-th non-win). Convolves per-round non-win probabilities."""
    dist = {0: 1.0}  # non-wins so far -> prob
    curve = []
    for rnd in sorted(plan_by_round):
        q = 1.0 - plan_by_round[rnd]["pwin"]
        nd = {}
        for k, pr in dist.items():
            nd[k] = nd.get(k, 0.0) + pr * (1 - q)      # win
            nd[k + 1] = nd.get(k + 1, 0.0) + pr * q     # non-win
        dist = nd
        alive = sum(pr for k, pr in dist.items() if k < lives)
        curve.append((rnd, plan_by_round[rnd]["team"], plan_by_round[rnd]["pwin"], alive))
    return curve
