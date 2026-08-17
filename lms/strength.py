"""Team strength ratings on an 'expected points' scale.

Two signals, blended per team:
  - MARKET  : outright title odds -> implied expected points (forward-looking,
              sharp for the strong teams, flat/uninformative for the tail).
  - TABLE   : last season's final points (informative for the tail, stale for
              teams the market has re-rated, e.g. Spurs).

Blend weight leans on the market where it has signal and on the table where it
doesn't:  w_market = P(champ) / (P(champ) + C).  Strong teams ~all market;
tail teams ~all table; Spurs lands near a 50/50 compromise (the max-disagreement
team) with both raw signals exposed so it can be overridden by eye.

Rating unit is 'expected points this season' — intuitive, and the win-prob model
turns rating differences into goal supremacy.
"""
import math
import os

from lms.ingest import CANON, vig_free

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "data")

# --- market -> expected points map:  epts = A + B * ln P(champ) --------------
# Anchored so the clear favourite (~86 pts) and the flat tail (~40 pts) land right.
MKT_A, MKT_B = 92.3, 7.58
# --- blend constant: smaller C => market wins for more teams -----------------
BLEND_C = 0.02


def _read_outright(path):
    prices = {}
    with open(path, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#") or "|" not in ln:
                continue
            name, val = (x.strip() for x in ln.split("|", 1))
            if val:
                prices[name] = float(val)
    return prices


def _read_points(path):
    pts = {}
    with open(path, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#") or "|" not in ln:
                continue
            parts = [x.strip() for x in ln.split("|")]
            pts[parts[0]] = float(parts[1])
    return pts


def build(data_dir=DATA):
    prices = _read_outright(os.path.join(data_dir, "teams.txt"))
    pchamp = vig_free(prices)
    pts = _read_points(os.path.join(data_dir, "last_season.txt"))

    rows = {}
    for t in CANON:
        p = pchamp[t]
        mkt = MKT_A + MKT_B * math.log(p)          # market-implied expected points
        tbl = pts[t]                                # last-season points (or prior)
        w = p / (p + BLEND_C)                        # weight on the market
        rating = w * mkt + (1 - w) * tbl
        rows[t] = {"pchamp": p, "market_epts": mkt, "table_pts": tbl,
                   "w_market": w, "rating": rating}
    return rows


def ratings(data_dir=DATA):
    return {t: r["rating"] for t, r in build(data_dir).items()}


if __name__ == "__main__":
    rows = build()
    print(f"{'team':<20}{'P(champ)':>9}{'mkt_epts':>10}{'table':>7}"
          f"{'w_mkt':>7}{'RATING':>8}")
    print("-" * 61)
    for t, r in sorted(rows.items(), key=lambda kv: -kv[1]["rating"]):
        print(f"{t:<20}{r['pchamp']*100:>8.1f}%{r['market_epts']:>10.1f}"
              f"{r['table_pts']:>7.0f}{r['w_market']:>7.2f}{r['rating']:>8.1f}")
