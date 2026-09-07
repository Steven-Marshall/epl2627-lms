"""Monte-Carlo the rest of the season from the current state.

Each alive player picks their best available team each round (greedy survival —
the field's observed behaviour), respecting no-repick. Match outcomes are sampled
PER TEAM per round, so everyone on the same team shares the same fate (the
correlation that makes herds dangerous). A non-win costs a life; out on the 3rd.
Last player standing wins; if the season (round 38) runs out or the last players
fall together, they split.

All-lose rule (provisional): if NO alive player's pick wins in a round, nobody
loses a life.

    python sim_season.py [n_sims] [start_round]
"""
import random
import sys
from collections import Counter, defaultdict

from lms.ingest import CANON
from lms.matrix import build_matrix
from lms.tracking import load_picks

LIVES = 3


def initial_state(start_round):
    """Used-teams + lives per player from rounds before start_round."""
    rows = [r for r in load_picks() if r["round"] < start_round]
    st = {}
    for r in rows:
        p = st.setdefault(r["player"], {"used": set(), "nonwins": 0})
        if r["team"]:
            p["used"].add(r["team"])
        if r["result"] in ("D", "L"):
            p["nonwins"] += 1
    return {n: {"used": set(p["used"]), "lives": LIVES - p["nonwins"]}
            for n, p in st.items() if LIVES - p["nonwins"] > 0}


def main():
    n_sims = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    cells = build_matrix()

    # per round: teams sorted by win prob desc (for fast best-available)
    ranked = {r: sorted(CANON, key=lambda t: -cells[(t, r)]["pwin"])
              for r in range(start, 39)}
    pwin = {(t, r): cells[(t, r)]["pwin"] for t in CANON for r in range(start, 39)}

    base = initial_state(start)
    solo = Counter()
    money = Counter()
    split_sizes = Counter()
    alive_after = defaultdict(float)   # round -> avg alive
    first_elim = []

    for _ in range(n_sims):
        players = {n: {"used": set(s["used"]), "lives": s["lives"]}
                   for n, s in base.items()}
        alive = set(players)
        last = set(alive)
        elim_seen = None
        for rnd in range(start, 39):
            if len(alive) <= 1:
                break
            picks = {}
            for n in alive:
                u = players[n]["used"]
                for t in ranked[rnd]:
                    if t not in u:
                        picks[n] = t
                        break
                else:
                    picks[n] = None
            teams = {t for t in picks.values() if t}
            won = {t: random.random() < pwin[(t, rnd)] for t in teams}
            any_win = any(picks[n] and won[picks[n]] for n in alive)
            dead = set()
            for n in alive:
                t = picks[n]
                if t:
                    players[n]["used"].add(t)
                survived = bool(t) and won[t]
                if not survived and any_win:
                    players[n]["lives"] -= 1
                    if players[n]["lives"] <= 0:
                        dead.add(n)
            if dead and elim_seen is None:
                elim_seen = rnd
            alive -= dead
            if alive:
                last = set(alive)
            alive_after[rnd] += len(alive)
        winners = alive if alive else last
        split_sizes[len(winners)] += 1
        if elim_seen:
            first_elim.append(elim_seen)
        for n in winners:
            money[n] += 1
            if len(winners) == 1:
                solo[n] += 1

    print(f"REST-OF-SEASON SIMULATION  ({n_sims:,} runs from round {start}, "
          f"{len(base)} alive)\n")

    print("HOW IT ENDS:")
    for k in sorted(split_sizes):
        print(f"  {k:>2} joint winner(s): {split_sizes[k]/n_sims*100:5.1f}%")
    solo_total = split_sizes.get(1, 0) / n_sims * 100
    print(f"  -> solo winner {solo_total:.1f}%,  split {100-solo_total:.1f}%")
    if first_elim:
        fe = sorted(first_elim)
        print(f"\n  First elimination: median round {fe[len(fe)//2]}, "
              f"earliest {fe[0]} (in {len(first_elim)/n_sims*100:.0f}% of runs someone goes)")

    print("\nFIELD SIZE (avg still alive after round):")
    for r in range(start, 39, 3):
        print(f"  R{r:<2} {alive_after[r]/n_sims:5.1f}")

    print("\nBEST-PLACED PLAYERS  (P in the money / P solo win):")
    ranked_players = sorted(base, key=lambda n: -money[n])
    print(f"  {'player':<16}{'lives':>6}{'in-money':>10}{'solo win':>10}")
    for n in ranked_players:
        print(f"  {n:<16}{base[n]['lives']:>6}{money[n]/n_sims*100:>9.1f}%"
              f"{solo[n]/n_sims*100:>9.1f}%")


if __name__ == "__main__":
    main()
