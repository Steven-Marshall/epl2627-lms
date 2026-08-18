"""The 'punching bag' strategy: fix a minnow, pick whoever plays it each round.

Auto-satisfies no-repick for the first 19 rounds (a team faces 19 distinct
opponents in the first half of a double round-robin). Quality oscillates with the
bag's home/away: when the BAG is away, your pick is at HOME (strong); when the bag
is home, your pick is away (weaker). And it goes soft when the bag faces another
minnow.
"""
from lms.matrix import build_matrix


def bag_route(bag, horizon=12, start=1, cells=None):
    """-> {round: {team, pwin, bag_home, src}} picking the bag's opponent."""
    cells = cells if cells is not None else build_matrix()
    route = {}
    for (team, rnd), c in cells.items():
        if c["opp"] == bag and start <= rnd < start + horizon:
            # c['home'] = is the OPPONENT (our pick) at home?
            route[rnd] = {"team": team, "pwin": c["pwin"],
                          "pick_home": c["home"], "src": c["src"]}
    return route


def repick_ok(route):
    teams = [route[r]["team"] for r in route]
    return len(teams) == len(set(teams))
