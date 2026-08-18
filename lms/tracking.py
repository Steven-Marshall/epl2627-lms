"""Track the mates' picks: used-team lists, lives, alive/out status.

Reads data/picks.csv (round,player,team,result). Result is W/D/L (blank until
played). Non-win = draw or loss = -1 life; out on the 3rd. Produces per-player
state — the foundation for the field/crowding layer (clone pairs, available
pools, who's forced onto what).
"""
import csv
import os

from lms.ingest import CANON, resolve_team

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "data")
LIVES = 3


def load_picks(data_dir=DATA):
    path = os.path.join(data_dir, "picks.csv")
    rows = []
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(x for x in f if not x.lstrip().startswith("#")):
            if not r.get("player") or not r.get("round"):
                continue
            rows.append({"round": int(r["round"]), "player": r["player"].strip(),
                         "team": resolve_team((r.get("team") or "").strip()),
                         "result": (r.get("result") or "").strip().upper()})
    return sorted(rows, key=lambda x: (x["round"], x["player"]))


def roster(data_dir=DATA):
    path = os.path.join(data_dir, "players.txt")
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if ln and not ln.startswith("#"):
                out.append(ln)
    return out


def standings(data_dir=DATA):
    rows = load_picks(data_dir)
    players = {}
    for r in rows:
        p = players.setdefault(r["player"], {
            "picks": [], "used": [], "nonwins": 0, "out_round": None})
        p["picks"].append((r["round"], r["team"], r["result"]))
        if r["team"]:
            p["used"].append(r["team"])
        if r["result"] in ("D", "L"):
            p["nonwins"] += 1
            if p["nonwins"] >= LIVES and p["out_round"] is None:
                p["out_round"] = r["round"]
    for name, p in players.items():
        p["lives_left"] = max(0, LIVES - p["nonwins"])
        p["alive"] = p["nonwins"] < LIVES
        p["available"] = [t for t in CANON if t not in p["used"]]
    return players
