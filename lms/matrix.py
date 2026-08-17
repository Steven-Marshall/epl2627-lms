"""The P(win) matrix: for every (team, round), the projected probability that
team wins its fixture that round. Projected from strength ratings; a round's
cells get overwritten by real 1X2 odds once those are supplied.
"""
import csv
import os

from lms.strength import ratings
from lms.winprob import win_prob

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "data")


def load_fixtures(data_dir=DATA):
    """-> {round: [(home, away), ...]}."""
    rounds = {}
    with open(os.path.join(data_dir, "fixtures.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rounds.setdefault(int(row["round"]), []).append((row["home"], row["away"]))
    return rounds


def build_matrix(data_dir=DATA, R=None):
    """-> {(team, round): {'opp', 'home', 'pwin'}} for all projected rounds."""
    R = R or ratings(data_dir)
    fixtures = load_fixtures(data_dir)
    cells = {}
    for rnd, games in fixtures.items():
        for home, away in games:
            cells[(home, rnd)] = {"opp": away, "home": True,
                                  "pwin": win_prob(R[home], R[away], home=True)}
            cells[(away, rnd)] = {"opp": home, "home": False,
                                  "pwin": win_prob(R[away], R[home], home=False)}
    return cells


def round_table(rnd, data_dir=DATA):
    """Every team's win chance in a given round, best first."""
    cells = build_matrix(data_dir)
    rows = []
    for (team, r), c in cells.items():
        if r == rnd:
            venue = "vs" if c["home"] else "@"
            rows.append((team, venue, c["opp"], c["pwin"]))
    return sorted(rows, key=lambda x: -x[3])


if __name__ == "__main__":
    import sys
    rnd = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"Round {rnd} — projected win probabilities (best picks first)\n")
    print(f"  {'team':<20}{'fixture':<20}{'P(win)':>8}")
    print("  " + "-" * 46)
    for team, venue, opp, p in round_table(rnd):
        print(f"  {team:<20}{venue + ' ' + opp:<20}{p*100:>7.1f}%")
