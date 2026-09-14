# Prediction 02 — after the bloodbath (after Round 4)

*The season simulation re-run from Round 5, on the wreckage of Round 4: 19 players left,
**14 of them on a single life**. Same method as [Prediction 01](prediction-01.md) —
greedy survival, per-team correlated outcomes, 3-lives attrition — plus one experiment
explained in Part 3.*

---

## 1. The forecast flipped: it's a solo-winner's game now

| | After R3 (Pred 01) | **After R4 (Pred 02)** |
|--|--|--|
| **Solo winner** | 33% | **~62%** |
| Split | 67% | ~38% |
| Winner set locks | median R18 | **median R14** (~mid-December) |

Round 4 didn't just thin the field, it changed the game's *nature*. With 14 of 19
survivors on their last life, the pool can no longer settle into a comfortable 3–4-way
split — it collapses. The most likely outcome is no longer a shared pot; it's **one
champion, crowned around mid-December.** (The 20-team budget still caps everything at
~round 20, but attrition now gets there first.)

## 2. The new board — the differentiated survivors run away with it

Ranked by EV (expected pot share; fair share = 5.3%):

| Player | Lives | EV % | Solo |
|--|--|--|--|
| **Jimmy D** | 2 | **23.6%** | 18.7% |
| **Jp C** | 2 | **19.0%** | 14.9% |
| Bobby A / Josh Wansell | 2 | 8.7% ea | **0%** (clone pair) |
| **Malley** | 1 | 7.4% | 6.6% |
| Mr Random | 2 | 7.3% | 7.3% |
| the 5-man clone bloc | 1 | **0.5% ea** | 0% |

Two lives *and* a used-list nobody shares — that's the whole story. Jimmy D and Jp C are
clear favourites. Malley, on his last life, still out-EVs the two-life clones — the
maverick's resilience again. And the five-man clone bloc is dead weight: **0.5% EV each,
under a tenth of fair share** — playing beautifully not to lose and hopelessly to win.

## 3. The experiment — does a coin beat the room? 🎲

Here's the reveal: **"Mr Random" is not a person.** The pool added a *control* this
season. The platform auto-allocates a random team to anyone who doesn't pick, so they
gave that empty seat its own entry — the house's dice roll — to see whether mindlessness
beats the mob. Four rounds in, it's alive on two lives while five humans are out.

So we tested it properly: model Mr Random's future picks as **genuinely random** (uniform
over unused teams), not greedy, and re-run.

| Mr Random plays… | EV % | In-money | Solo | Rank |
|--|--|--|--|--|
| greedy (the flattering sim) | 23.8% | 32.6% | 19.0% | **1st** |
| **true dice roll** (reality) | **7.3%** | 7.3% | 7.3% | **6th** |

**Random is not magic.** Play it for real and its survival craters — it picks a weak team
half the time — dropping it from 1st to 6th. But look at what survives the drop:

- **The coin still buries the herd.** At 7.3% EV it sits *above* fair share (5.3%) and
  **~15× the five herding humans** (0.5% each). A dice roll is worth fifteen careful
  thinkers who reasoned their way into the same blob.
- **Every win is solo.** For the dice, **in-money = solo = EV = 7.3%** — it is so
  perfectly uncorrelated that whenever it wins, it wins *alone*. It never shares a pot
  because it never shares a used-list. The coin achieves the model's single most-prized
  property — concentrated, solo winnings — by having no strategy whatsoever.
- It loses cleanly only to the genuine contrarians (Jimmy D, Jp C).

**The verdict:** *thinking only pays if it makes you different.* The players who reasoned
their way onto the same safe banker finished **far below a coin** — because the coin, at
least, was never part of the crowd. Correlation is the enemy of a shared pot, and
rationality that ignores it is worse than useless.

## 4. Footnote 🐟

The model is now crowning the players who ignored what it recommended each week, and
rating a dice roll above fifteen humans. Smarshy, its author, went out in Round 4 on the
safest pick on the board. That's the whole game in one bittersweet line: the octopus's
job was to keep you *alive*, and it did — right up to the week it couldn't. But *winning*
this thing was always going to belong to whoever was brave enough, or mindless enough, to
be alone.

---

*Caveats as Prediction 01: a greedy-survival model for the human field, projected
win-probabilities beyond the next round or two are estimates. The random-bot result uses
true uniform-random picks over each player's unused teams.*
