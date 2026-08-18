"""The weekly decision framework, in one place. Three questions each round:

  [1] TOP PICKS  - the best teams you can actually play this round.
  [2] SAVE COST  - for each, their best UPCOMING game, i.e. what you give up by
                   spending them now (save vs spend).
  [3] MID-BAND   - any 'not-quite-minnow' team (ranks 12-18) whose good window is
                   THIS round, worth using up now rather than being forced later.

This is the right lens for the early weeks (survival + harvest/save + disposal).
Once the field thins and shockers land, layer in crowd/field analysis on top.

    python week.py [round=1] [K=3] [future_to=19]
"""
import sys

from lms.matrix import build_matrix
from lms.strength import ratings


def fx(c):
    return ("vs " if c["home"] else "@ ") + c["opp"]


def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    future_to = int(sys.argv[3]) if len(sys.argv) > 3 else 19
    cells = build_matrix()
    R = ratings()
    rank = {t: i + 1 for i, t in enumerate(sorted(R, key=R.get, reverse=True))}

    this = sorted(((t, c) for (t, r), c in cells.items() if r == start),
                  key=lambda x: -x[1]["pwin"])
    top = this[:K]

    print(f"================  WEEKLY ANALYSIS - ROUND {start}  ================\n")

    print(f"[1] TOP {K} PICKS YOU CAN PLAY (best survival this round)")
    for t, c in top:
        src = "odds" if c["src"] == "odds" else "proj"
        print(f"    {t:<16}{fx(c):<20}{c['pwin']*100:>5.0f}%  [{src}]  (rank {rank[t]})")

    print(f"\n[2] SAVE vs SPEND - each pick's best UPCOMING game "
          f"(what you'd give up now)")
    for t, c in top:
        fut = sorted(((r, cells[(t, r)]) for r in range(start + 1, future_to + 1)),
                     key=lambda x: -x[1]["pwin"])
        if not fut:
            continue
        br, bc = fut[0]
        gap = bc["pwin"] - c["pwin"]
        if gap > 0.03:
            verdict = f"SAVE - better spot R{br} {fx(bc)} {bc['pwin']*100:.0f}% (+{gap*100:.0f})"
        else:
            verdict = f"SPEND - now (~{c['pwin']*100:.0f}%) is about their peak"
        print(f"    {t:<16} now {c['pwin']*100:>3.0f}%   ->  {verdict}")

    print(f"\n[3] MID-BAND DISPOSAL (ranks 12-18) - good window THIS round?")
    mid = [t for t in R if 12 <= rank[t] <= 18]
    flagged = []
    for t in sorted(mid, key=lambda x: rank[x]):
        now = cells[(t, start)]
        season = max(cells[(t, r)]["pwin"] for r in range(start, future_to + 1))
        near_peak = now["pwin"] >= 0.9 * season
        if now["pwin"] >= 0.48 and near_peak:
            flagged.append((t, now, season))
    if flagged:
        for t, now, season in flagged:
            print(f"    {t:<16}{fx(now):<20}{now['pwin']*100:>5.0f}%  "
                  f"(season best {season*100:.0f}%) -> worth using up now")
    else:
        print("    none compelling - mid-band teams are in weak spots this week; "
              "their windows come later.")
    print()


if __name__ == "__main__":
    main()
