"""Team strength ratings on an 'expected points' scale.

THREE market/table anchors, each trusted only where it carries signal:
  - TITLE   : outright title odds -> implied expected points. Sharp for the top
              ~6, flat/useless below (everyone ~0.1% to win).
  - BOTTOM  : 'to finish bottom' (wooden-spoon) odds -> implied points. Sharp for
              the tail (who's worst), the instrument the title market can't be.
  - TABLE   : last season's final points. Fills the middle; a prior for the tail.

Hierarchical weighting: the title market claims a team first (w_title high for
contenders), whatever's left is split between the bottom market (w high for
relegation-risk teams) and the table. So Arsenal ~all title, Hull ~all bottom,
a becalmed mid-table side ~all table. Each extreme market only bites where it
actually knows something.

Rating unit is 'expected points this season'; the win-prob model turns rating
differences into goal supremacy.
"""
import math
import os

from lms.ingest import CANON, vig_free

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "data")

# TITLE odds -> expected points:  epts = A + B * ln P(champ)
# Anchored so the clear favourite (~86 pts) and the flat tail (~40 pts) land right.
MKT_A, MKT_B = 92.3, 7.58
# BOTTOM odds -> expected points:  bpts = A + B * ln P(finish bottom)
# Anchored: wooden-spoon favourite (~evens -> ~22 pts), a ~4% shot (~45 pts).
BOT_A, BOT_B = 16.0, -9.2
# weighting constants: smaller => that market claims more teams
C_TITLE = 0.02
C_BOTTOM = 0.05


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


def _read_relegation(path):
    """'to finish bottom' odds -> vig-free P(finish bottom), normalised to sum 1."""
    prices = {}
    with open(path, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#") or "|" not in ln:
                continue
            name, val = (x.strip() for x in ln.split("|", 1))
            if val:
                prices[name] = float(val)
    raw = {t: 1.0 / o for t, o in prices.items()}
    s = sum(raw.values())
    return {t: v / s for t, v in raw.items()}


def build(data_dir=DATA):
    prices = _read_outright(os.path.join(data_dir, "teams.txt"))
    pchamp = vig_free(prices)
    pts = _read_points(os.path.join(data_dir, "last_season.txt"))
    pbottom = _read_relegation(os.path.join(data_dir, "finish_bottom.txt"))

    rows = {}
    for t in CANON:
        pc, pb, tbl = pchamp[t], pbottom[t], pts[t]
        title_epts = MKT_A + MKT_B * math.log(pc)
        bot_epts = BOT_A + BOT_B * math.log(pb)
        # hierarchical weights: title claims first, remainder split bottom/table
        w_title = pc / (pc + C_TITLE)
        rem = 1 - w_title
        w_bottom = rem * (pb / (pb + C_BOTTOM))
        w_table = rem * (C_BOTTOM / (pb + C_BOTTOM))
        rating = w_title * title_epts + w_bottom * bot_epts + w_table * tbl
        rows[t] = {"pchamp": pc, "pbottom": pb, "title_epts": title_epts,
                   "bottom_epts": bot_epts, "table_pts": tbl, "w_title": w_title,
                   "w_bottom": w_bottom, "w_table": w_table, "rating": rating}
    return rows


def ratings(data_dir=DATA):
    return {t: r["rating"] for t, r in build(data_dir).items()}


if __name__ == "__main__":
    rows = build()
    print(f"{'team':<20}{'Pchmp':>6}{'Pbot':>6}{'title':>6}{'bot':>6}{'tbl':>5}"
          f"  {'wT':>4}{'wB':>4}{'wTb':>5}{'RATING':>8}")
    print("-" * 76)
    for t, r in sorted(rows.items(), key=lambda kv: -kv[1]["rating"]):
        print(f"{t:<20}{r['pchamp']*100:>5.1f}{r['pbottom']*100:>6.1f}"
              f"{r['title_epts']:>6.0f}{r['bottom_epts']:>6.0f}{r['table_pts']:>5.0f}  "
              f"{r['w_title']:>4.2f}{r['w_bottom']:>4.2f}{r['w_table']:>5.2f}"
              f"{r['rating']:>8.1f}")
