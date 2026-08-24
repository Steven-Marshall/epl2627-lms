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

    # clone blocs: alive players grouped by identical used-list (WC lesson).
    # A bloc of size k can't separate internally -> none can win outright vs the
    # others while they stay matched. Meaningful once used-lists start diverging.
    from collections import defaultdict
    blocs = defaultdict(list)
    for n, p in st.items():
        if p["alive"] and p["used"]:
            blocs[tuple(sorted(p["used"]))].append(n)
    big = sorted((g for g in blocs.values() if len(g) > 1), key=len, reverse=True)
    if big:
        print("\n  CLONE BLOCS (identical used-lists -> can't separate within a bloc):")
        for g in big:
            print(f"    [{len(g):>2}]  {', '.join(sorted(g))}")

    # who on the roster hasn't picked the latest round
    picked = {r["player"] for r in load_picks() if r["round"] == last}
    missing = [n for n in roster() if n not in picked]
    if missing:
        print(f"\n  Not yet picked R{last}: {', '.join(missing)}")


if __name__ == "__main__":
    main()
