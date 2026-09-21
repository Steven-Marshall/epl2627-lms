# Prediction 03 — seven left, a sharper model, a two-man race (after Round 5)

*Re-run from Round 6 on a field of seven. Two things are new since
[Prediction 02](prediction-02.md): the strength model has been **recalibrated** to
the in-season markets, and **Round 6's real Betfair odds** are folded in. Same method
otherwise — greedy survival for the human field, per-team correlated outcomes, 3-lives
attrition, plus the random-bot control from Part 4.*

---

## 1. The model got honest — and it changed the tail

Five rounds of results let us re-anchor the strength table on the **current** markets
(title odds + "to be relegated" odds) instead of the pre-season ones. The market has
watched the same football we have, so this is a re-rate by the crowd of bookmakers, not
a thumb on the scale. The big moves:

| Team | was | now | why |
|--|--|--|--|
| **Man City** | 78.9 | **83.9** ▲ | title shortened to 2.67 — near co-favourite |
| **Chelsea** | 74.3 | **61.4** ▼ | drifted 7.1 → 28.5 to win it |
| **Fulham / Palace** | ~50 / ~47 | **37 / 34** ▼ | both now priced to be relegated |
| **Tottenham** | 50.5 | **44.3** ▼ | slid into the relegation market (9.0) |
| **Hull** | 25.0 | **24.6** — | *unchanged* |

That last row is the interesting one. Hull have beaten Man Utd and held Chelsea, and it
would be tempting to rate them up. But the market — same evidence — still prices Hull at
**1.7 to be relegated**. The bookmakers are calling Hull's results **overperformance that
regresses**, not a good team emerging. So the model holds the line and keeps Hull near the
bottom. Hull keeps causing *upsets*; an upset by a weak side isn't evidence the side is
strong — it's evidence this game is cruel. The recalibration's real work was in the
**middle**: Chelsea, Spurs, Fulham and Palace were all rated too high, and they're exactly
the teams the seven survivors must pick from now the elite is used up. A truer model is a
**harsher** one.

## 2. The forecast: one champion, but *when* is a wide spread

| | After R4 (Pred 02) | **After R5 (Pred 03)** |
|--|--|--|
| Solo winner | ~62% | **~90%** |
| Split | ~38% | ~10% |
| Winner crowned | median R14 | **median R10–11** (~early November) |

Seven from twenty-four, five on a single life — and it resolves to **one champion about
nine times in ten.** It's also front-loaded: roughly **a third are decided by Round 9**
(late October), the **median crowning is Round 10–11** (early November), and only about
**8%** grind to the Round-21 budget cap (~New Year) and split.

That pace turns on the pool's exact deadlock rule, now confirmed: **a non-win costs a life
as normal — even in a round where nobody wins — right up until the moment *every* remaining
player is on their last life.** Only then, with no champion possible if they all fell at
once, is a no-win round voided so the survivors play on. So the protection is a narrow
endgame tie-breaker, not a general shield: the field collapses fast, and the one-life
players are genuinely fragile — a one-lifer on ~55% picks is only **~12–30%** to last four
more rounds. The 20-team budget is the hard stop: the game **cannot** run past Round 21.

## 3. The board — Josh out front, the extra life is king

Ranked by EV (expected pot share; fair share = 14.3%), Mr Random modelled as the **true
dice roll**:

| Player | Lives | EV % | Solo |
|--|--|--|--|
| **Josh Wansell** | 2 | **47.3%** | 42.5% |
| **Jimmy D** | 1 | **22.0%** | 21.3% |
| Mr Random | 2 | 18.0% | 18.0% |
| Andy W | 1 | 5.9% | 4.5% |
| PK1 | 1 | 3.9% | **0%** |
| Jp C | 1 | 1.7% | 1.2% |
| Bobby A | 1 | 1.3% | 1.0% |

Under the real rule, the **extra life is the master variable.** A no-win round now kills a
one-life player, so the cushion Josh and the coin are carrying is worth far more than it
looked — **Josh Wansell is a runaway favourite at 47%, nearly half the pot on his own.**

But board quality still speaks, and this is the subtle bit: **Jimmy D holds second (22%) on
a single life** — his leftover card is so much sharper than anyone else's (the elite teams
saved, a banker still in hand) that his one life outranks the coin's two. So the pecking
order is precise: *two lives and a decent board* (Josh) ≫ *one life and an elite board*
(Jimmy D) ≈ *two lives and no plan at all* (the coin) ≫ everyone else. The three remaining
one-lifers with ordinary boards — Andy W, Jp C, Bobby A — are close to dead weight now,
each under a tenth of the pot.

PK1 is the last shadow — **0% solo**. His used-list mirrors Josh's on four of five teams, so
greedy-forward he keeps landing on Josh's picks and can only ever *split* with a man who has
more lives. Even after the clone blocs shattered, one clone-of-one remains.

## 4. The coin, honestly measured 🎲

The reveal holds and it's still the sharpest thing in the model: pretend **Mr Random** picks
like everyone else (greedy) and it tops the chart at a flattering **52% EV**; model it as the
genuine dice roll it actually is and it's **18% — third.** That gap, 52% down to 18%, *is*
the value of thinking, laid out in a single line: everything the coin "earns" in the naive
sim is really being earned by the strategy it doesn't have.

And yet third is remarkable. On two lives, picking blind, it still sits **above fair share
(14.3%)** and ahead of five thinking humans. Two things carry it: the **extra life**, which
the corrected rule just made precious, and the one structural gift a random picker can't help
having — **it never shares a used-list, so every win it takes is solo** (its in-money, solo
and EV are the same 18%). It will never split a pot because it was never in a crowd. The coin
doesn't win this on the numbers — Josh's cushion and Jimmy D's board both beat it — but it
remains the most dangerous *single* entry in the field, precisely because it cannot be
correlated with anyone. Thinking pays; but so, a little, does having no plan that anyone can
copy.

## 5. The state of the seven — the week ahead

From here we advise each surviving player the same way: **their single best available team
given the current Betfair odds**, respecting no-repick. We don't publish the individual
picks — this note is public and the field can read it — but the *shape* of Round 6 is worth
seeing, because it's where "coinflip territory" starts to bite:

- **The week offers exactly one banker** and then a steep drop to a cluster of coin-flips.
- **Not everyone can reach the banker.** The players who *saved* their strongest pick still
  have a comfortable week; the ones who spent it early are down to roughly a 50/50 — and
  some of them are on their last life.
- **Correlation is still the danger.** Several of the seven are funnelling toward the same
  fallback team, and it's one the recalibration just marked *down*. If it slips, it takes
  more than one player with it — the clone-bloc gutting in miniature, all over again.
- **From Round 7 the squeeze is general.** Once the last bankers are spent, the recalibrated
  middle is all that remains, and it tops out around a 45% pick. Most weeks, for most of the
  seven, will be a coin toss from here.
- **And the coin plays on.** Mr Random picks at random from whatever it hasn't used — so it
  might land on the very banker the thinkers are fighting over, or on a relegation-bound dog,
  with equal nonchalance. That indifference is the whole experiment: it never agonises, and
  it's still standing.

## 6. Footnote 🐟

Seven players, and the model that spent five rounds keeping people *alive* now spends its
time working out who gets to be *alone*. It has installed Josh Wansell as a clear favourite,
priced an extra life above all the clever board-management in the world, ranked Jimmy D's
lone-but-loaded card level with a coin holding two lives, and — having finally been made
honest about both the teams and the rules — concluded that the dice it once feared is the
third-best thing in the room and still the hardest to catch. The octopus grows sharper; the
game grows crueller; and somewhere in the field a random number generator is about to make
its pick without a single thought in its head. 🐙
