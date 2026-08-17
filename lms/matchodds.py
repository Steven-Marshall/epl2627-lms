"""Real 1X2 match odds per round -> vig-free win probabilities.

A round file (data/rounds/roundNN.txt) holds lines:
    home | away | H | D | A       (decimal prices)
Each match is normalised (1/odds summed to 1) to strip the vig. These are the
SHARP truth for that round and override the projected matrix cells.
"""
import os

from lms.ingest import parse_price, resolve_team

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "data")


def round_path(n, data_dir=DATA):
    return os.path.join(data_dir, "rounds", f"round{n:02d}.txt")


def load_round(n, data_dir=DATA):
    """-> list of {home, away, pH, pD, pA} vig-free, or None if no file."""
    path = round_path(n, data_dir)
    if not os.path.exists(path):
        return None
    out = []
    with open(path, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#") or "|" not in ln:
                continue
            parts = [x.strip() for x in ln.split("|")]
            home, away = resolve_team(parts[0]), resolve_team(parts[1])
            h, d, a = (parse_price(parts[2]), parse_price(parts[3]), parse_price(parts[4]))
            inv = [1.0 / h, 1.0 / d, 1.0 / a]
            s = sum(inv)
            out.append({"home": home, "away": away,
                        "pH": inv[0] / s, "pD": inv[1] / s, "pA": inv[2] / s})
    return out


def round_overrides(n, data_dir=DATA):
    """-> {(team, round): {'opp','home','pwin'}} from real odds, or {} if none."""
    rows = load_round(n, data_dir)
    if rows is None:
        return {}
    cells = {}
    for m in rows:
        cells[(m["home"], n)] = {"opp": m["away"], "home": True, "pwin": m["pH"]}
        cells[(m["away"], n)] = {"opp": m["home"], "home": False, "pwin": m["pA"]}
    return cells


def available_rounds(data_dir=DATA):
    d = os.path.join(data_dir, "rounds")
    if not os.path.isdir(d):
        return []
    ns = []
    for fn in os.listdir(d):
        if fn.startswith("round") and fn.endswith(".txt"):
            try:
                ns.append(int(fn[5:7]))
            except ValueError:
                pass
    return sorted(ns)
