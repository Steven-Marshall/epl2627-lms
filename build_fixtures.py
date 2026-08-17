"""Build & validate data/fixtures.csv from data/fixtures_raw.txt.

Raw format: '### Matchday N' headers, then 'Home | Away' lines.
Resolves loose names to canonical, then VALIDATES hard before writing:
  - 38 rounds, 10 matches each
  - every team appears exactly once per round (all 20, home+away)
  - each ordered (home, away) pairing occurs exactly once all season
  - each unordered pairing occurs exactly twice (once each way)
  - every team has exactly 19 home and 19 away games
Refuses to write fixtures.csv if any check fails.
"""
import os
import sys
from collections import Counter, defaultdict

from lms.ingest import CANON, resolve_team

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
RAW = os.path.join(DATA, "fixtures_raw.txt")
OUT = os.path.join(DATA, "fixtures.csv")


def parse():
    rounds = defaultdict(list)
    cur = None
    problems = []
    with open(RAW, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            if ln.lower().startswith("### matchday"):
                cur = int(ln.split()[-1])
                continue
            if "|" not in ln:
                problems.append(f"no '|' separator: {ln!r}")
                continue
            h, a = (x.strip() for x in ln.split("|", 1))
            ch, ca = resolve_team(h), resolve_team(a)
            if ch is None:
                problems.append(f"MD{cur}: unresolved home {h!r}")
            if ca is None:
                problems.append(f"MD{cur}: unresolved away {a!r}")
            rounds[cur].append((ch, ca))
    return rounds, problems


def validate(rounds):
    errs = []
    if sorted(rounds) != list(range(1, 39)):
        errs.append(f"rounds present: {sorted(rounds)} (want 1..38)")
    ordered = Counter()
    home_ct, away_ct = Counter(), Counter()
    for r in sorted(rounds):
        games = rounds[r]
        if len(games) != 10:
            errs.append(f"MD{r}: {len(games)} matches (want 10)")
        seen = Counter()
        for h, a in games:
            seen[h] += 1
            seen[a] += 1
            ordered[(h, a)] += 1
            home_ct[h] += 1
            away_ct[a] += 1
        for t in CANON:
            if seen[t] != 1:
                errs.append(f"MD{r}: {t} appears {seen[t]}x (want 1)")
    for pair, n in ordered.items():
        if n != 1:
            errs.append(f"ordered pair {pair} occurs {n}x (want 1)")
    for t in CANON:
        if home_ct[t] != 19:
            errs.append(f"{t}: {home_ct[t]} home games (want 19)")
        if away_ct[t] != 19:
            errs.append(f"{t}: {away_ct[t]} away games (want 19)")
    # unordered pairing exactly twice
    unordered = Counter()
    for (h, a), n in ordered.items():
        unordered[frozenset((h, a))] += n
    for pair, n in unordered.items():
        if n != 2:
            errs.append(f"unordered {set(pair)} occurs {n}x (want 2)")
    return errs


def main():
    rounds, problems = parse()
    errs = problems + validate(rounds)
    if errs:
        print("VALIDATION FAILED — fixtures.csv NOT written:\n")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("round,home,away\n")
        for r in sorted(rounds):
            for h, a in rounds[r]:
                f.write(f"{r},{h},{a}\n")
    print(f"OK — 38 rounds, 380 matches, all checks passed. Wrote {OUT}")


if __name__ == "__main__":
    main()
