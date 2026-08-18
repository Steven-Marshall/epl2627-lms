# EPL 2026/27 — Last Man Standing strategy engine

A strategy model for a Last-Man-Standing pool over the **2026/27 Premier League**.
Sibling to the completed World Cup engine (`../footy`) but a **different game**: no
bracket, draws kill you, three lives, and the scarce resource is good fixtures
rather than surviving teams.

---

## The rules (this pool)

- Each **round** (a full set of 10 fixtures — every team plays once) you pick **one
  team**. It must **win**; a **draw or a loss costs a life**.
- **3 lives** — each non-win costs one; you're out on your **3rd**.
- **No repick**: each team can be used at most **once all season** (20 teams → you
  can never need more than 20 picks, and realistically far fewer).
- **No reset** within a competition. **Field**: ~10–20 friends. **Ties**: the pot is
  **split** among the last players standing.
- *TBC:* the all-lose rule ("all survive" if everyone picks a non-winner), and what
  happens if a player uses all 20 teams (split vs reset). Neither bites early.

## Why the World Cup engine doesn't transfer

| World Cup | EPL LMS |
|--|--|
| Knockout bracket | League — no bracket |
| A loss ends you | **Draw *or* loss costs a life** (3 lives) |
| Bradley-Terry (win/lose) | 3-outcome model (win/draw/lose) |
| Save the champion | No champion — pure survival + differentiation |
| Scarce = surviving teams | Scarce = **premium fixtures** (assignment problem) |

---

## The model

**1. Strength ratings** (`lms/strength.py`) — each team gets a rating on an
"expected league points" scale, blended from **three anchors**, each trusted only
where it carries signal:

- **Title odds** → pins the top ~6 (sharp there, flat below).
- **"Finish bottom" odds** → pins the tail (who's actually weak — the instrument the
  title market can't be).
- **Last season's points** → fills the middle.

Weights are hierarchical: the title market claims contenders, the finish-bottom
market claims relegation risks, last-season points cover everyone else. (Man City's
finish-bottom price is excluded — it's a hedge against a *points deduction*, an
off-pitch risk that doesn't change match results.)

**2. Win probabilities** (`lms/winprob.py`) — a supremacy-Poisson model turns two
ratings + home advantage into P(win / draw / lose).

**3. The matrix** (`lms/matrix.py`) — P(win) for every team in every round.
Projected from ratings, but **any round with real 1X2 odds overrides the
projection** (sharp market prices always beat the model).

---

## Strategy — the three questions each round

For the early weeks this is pure survival maths (harvest/save + disposal). Once the
field thins and shockers land, a crowd/field layer gets added on top.

1. **Top picks you can play** — the best win-prob teams available this round.
2. **Save vs spend** — for each, their *best upcoming game*, i.e. what option value
   you destroy by spending them now. Save a team if it has a clearly better slot
   later (e.g. Arsenal's home game vs Hull); spend it if now is about its peak.
3. **Mid-band disposal** — a "not-quite-minnow" team (ranks ~12–18) whose *good
   window is this round* can be worth using up now, rather than being forced to play
   it later in a hopeless spot.

`python week.py [round]` runs all three at once.

### Two structural truths this game turns on

- **Harvest/save:** every pick spends a team you can't reuse. Score ≈ P(win now) ×
  (1 − how much you'll want them later). Never burn your best team on an ordinary
  week; never get stranded with only away-days-at-the-big-six left.
- **Toxic assets:** the very worst teams (Hull, Ipswich) have *no* good week — Hull's
  best fixture all season is ~35%. You don't time their disposal, you **never play
  them**. Since a deep run needs only ~15 picks, you simply leave the bottom few on
  the shelf.

### Durable lessons carried from the World Cup (properties of the *pot*, not the sport)

Contrarian value decays with crowding (the edge is in the *lane*, not the player);
a split pot makes people play "don't get knocked out" rather than EV, so they herd;
**clone pairs** (identical used-lists) can never separate and so can't win outright.
These bite later here than in the WC (3 lives + split ties soften early herding),
which is why the field layer is deferred.

---

## Tools

| Command | What it does |
|--|--|
| `python week.py [rnd]` | **The weekly driver** — top picks, save-vs-spend, mid-band disposal |
| `python decide.py [rnd]` | Top-K picks + full downstream route & survival for each |
| `python route.py [rnd]` | Full planned route, 1st (plan) + 2nd (backup) each week |
| `python plan.py [rnd]` | Optimal route + harvest-vs-save table + survival curve |
| `python weak.py [N]` | Disposal windows for the bottom-N teams |
| `python bag.py [team]` | "Punching bag" strategy (shadow one minnow) vs the planner |
| `python picks.py` | Standings from logged picks — lives, status, clone pairs |
| `python compare_round.py [rnd]` | Market odds vs model projection for a round |
| `python ingest_outright.py` | Parse pasted title odds into the strength sheet |
| `python build_fixtures.py` | Rebuild & validate `data/fixtures.csv` |

## Weekly workflow

1. Paste the round's **1X2 odds** → saved to `data/rounds/roundNN.txt` (overrides the
   projection for that round).
2. `python week.py N` → make the pick using the three questions above.
3. After the games, log everyone's picks + results in `data/picks.csv` →
   `python picks.py` for standings and clone-pair flags.
4. When the field starts to thin (a few weeks in), build the field/crowding layer
   from the accumulated picks — the real tiebreaker for close calls.

## Data files

- `data/teams.txt` — 20 teams + outright title odds.
- `data/finish_bottom.txt` — wooden-spoon market (sorts the tail).
- `data/last_season.txt` — 2025/26 final points (the table prior).
- `data/fixtures.csv` — all 380 matches, validated.
- `data/rounds/roundNN.txt` — per-round 1X2 odds as they arrive.
- `data/picks.csv`, `data/players.txt` — the mates' picks + roster.

## Status

Engine complete through the solo/decision layer. Field/crowding layer deferred until
real pick data accumulates. Pure stdlib Python; no dependencies.
