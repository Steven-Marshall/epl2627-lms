"""Standings from the logged picks: lives, status, used teams, clone pairs.

    python picks.py
"""
from itertools import combinations

from lms.tracking import load_picks, roster, standings


def main():
    st = standings()
    if not st:
        print("No picks logged yet. Add rows to data/picks.csv "
              "(round,player,team,result).")
        return

    last = max(r["round"] for r in load_picks())
    order = sorted(st.items(), key=lambda kv: (not kv[1]["alive"],
                                               kv[1]["nonwins"], kv[0]))
    print(f"STANDINGS after round {last}\n")
    print(f"  {'player':<14}{'lives':>6}{'status':>10}{'used':>6}  last pick")
    print("  " + "-" * 52)
    for name, p in order:
        status = "ALIVE" if p["alive"] else f"OUT R{p['out_round']}"
        lastpick = p["picks"][-1]
        lp = f"R{lastpick[0]} {lastpick[1] or '?'} {lastpick[2] or ''}".strip()
        print(f"  {name:<14}{p['lives_left']:>6}{status:>10}{len(p['used']):>6}  {lp}")

    # clone pairs: alive players with identical used-team sets (WC lesson)
    alive = [(n, p) for n, p in st.items() if p["alive"]]
    clones = [(a, b) for (a, pa), (b, pb) in combinations(alive, 2)
              if set(pa["used"]) == set(pb["used"]) and pa["used"]]
    if clones:
        print("\n  CLONE PAIRS (identical used-lists -> can't separate; watch these):")
        for a, b in clones:
            print(f"    {a} = {b}")

    # who on the roster hasn't picked the latest round
    picked = {r["player"] for r in load_picks() if r["round"] == last}
    missing = [n for n in roster() if n not in picked]
    if missing:
        print(f"\n  Not yet picked R{last}: {', '.join(missing)}")


if __name__ == "__main__":
    main()
