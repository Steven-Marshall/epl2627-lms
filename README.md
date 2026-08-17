# EPL 2026/27 — Last Man Standing strategy engine

A strategy model for a Last-Man-Standing pool over the **2026/27 Premier League**.
Sibling project to the completed World Cup engine (`../footy`), but a **different
game** needing a **different model** — no bracket, draws kill you, and the scarce
resource is good fixtures rather than surviving teams.

## The rules (this pool)

- Each **round** (a full set of 10 fixtures — every team plays exactly once) you
  pick **one team**.
- Your pick must **win**. A **draw or a loss costs a life**.
- You have **3 lives** — each non-win costs one; you're out on your **3rd** non-win.
- **No repick**: you can use each team at most **once for the whole competition**
  (20 teams → a hard ceiling of ~20 rounds of picks).
- **No reset** within a competition (a new comp is just started separately).
- **Field**: ~10–20 friends.
- **Ties**: the pot is **split** among the last players standing (no rollover).
- **Deals**: players may agree to split, but nothing is forced.
- **All-lose rule**: TBC — provisionally "if everyone still in picks a non-winner,
  all survive". Rarely bites early given 3 lives.

## Why the World Cup engine doesn't transfer

| World Cup engine | EPL LMS |
|--|--|
| Knockout **bracket** (reach-probability DP) | **League** — no bracket at all |
| Win = advance; a loss ends you | **Draw *or* loss costs a life** (3-outcome) |
| **Bradley-Terry** (win/lose) fitted to odds | Need **P(win / draw / lose)** — draws matter |
| Save the champion for the final | **No champion to save** — pure survival |
| Scarce resource = surviving teams | Scarce resource = **premium fixtures** |
| Sudden death | **3 lives** — a slow burn, weaker herding |

## Model architecture (build order)

1. **Strength model** → a `P(win)` matrix over `[team × round]`.
   - **Near-term**: taken directly from live **1X2 match odds** (sharp, vig removed).
   - **Future rounds**: projected from **outright title odds** → a team-strength
     ranking + measured home advantage, rolled forward over the fixture list.
2. **Solo planner** → the survival-optimal assignment of *which team in which round*
   (each team used once), respecting the 3-lives structure. Assignment optimisation
   (Hungarian on log-win-prob) + a lives-aware refinement. Outputs a recommended
   plan and a projected survival curve.
3. **Field / game layer** → opponent model, crowding/contrarian value, split-pot EV
   vs pure survival. This is the strategic commentary shared with the group.

## Durable lessons carried over (see `../footy` memory + RETROSPECTIVE)

Properties of the *pot*, not the sport — still apply: contrarian value decays with
crowding (edge is in the lane, not the player); split-pot changes what game people
play (survival vs EV); behavioural priors belong on the *outcome a player wants*.
Herding pressure is **weaker** here than the WC (3 lives, split ties, draws) but the
structure is the same.

## Data

- `data/teams.txt` — human-edited sheet: the 20 teams + outright title odds → strength.
- `data/fixtures.csv` — `round,home,away` for all 380 matches (validated on load).
- `data/rounds/` — per-round 1X2 match odds as they arrive.

## Status

Scaffold. Awaiting first data: outright title odds + validated fixture list.
