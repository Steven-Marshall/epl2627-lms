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

## 2. The forecast: one champion, crowned by late November

| | After R4 (Pred 02) | **After R5 (Pred 03)** |
|--|--|--|
| Solo winner | ~62% | **~76%** |
| Split | ~38% | ~24% |
| Winner set locks | median R14 | **median R11** (~late Nov) |

Seven from twenty-four, five of them on a single life. This is no longer a pool that can
settle into a shared pot — it's **one champion, most likely decided inside six more
rounds**, and hard-capped at Round 21 by the 20-team budget regardless.

## 3. The board — a two-man race, with a coin lurking

Ranked by EV (expected pot share; fair share = 14.3%), Mr Random modelled as the **true
dice roll**:

| Player | Lives | EV % | Solo |
|--|--|--|--|
| **Josh Wansell** | 2 | **30.7%** | 21.3% |
| **Jimmy D** | 1 | **27.1%** | 25.6% |
| Mr Random | 2 | 15.8% | 15.8% |
| Jp C | 1 | 7.6% | 5.0% |
| Andy W | 1 | 7.1% | 4.5% |
| PK1 | 1 | 6.5% | **0%** |
| Bobby A | 1 | 5.2% | 3.6% |

**Josh Wansell and Jimmy D are 58% of the pot between them** — a two-horse race. And look
how close they are: Josh has **two** lives, Jimmy D has **one**, yet they're nearly level.
Jimmy D's board is simply better — he saved the elite teams the others burned, so he still
has the sharpest picks in front of him. The second life and the better board very nearly
cancel out. That's the whole thesis of this project in one line of a table: **what's left
on your card is worth about as much as a life.**

PK1 is the cautionary tale — **0% solo**. His used-list shadows Josh's on four of five
teams, so greedy-forward he keeps landing on the same picks and can only ever *split* with
a man who has more lives. Even after the clone blocs shattered, one shadow remains.

## 4. The coin got worse — because the model got better 🎲

The reveal still stands: model **Mr Random** greedy and it flatters to a chart-topping
**47.5% EV**; model it as the genuine dice roll and it's **15.8% (3rd)**. But recalibration
quietly *demoted* the coin, and the reason is the sharpest thing we've learned all season:

**Making the weak teams genuinely weak hurts the random bot more than it hurts the
thinkers.** A dice roll walks onto the tail half the time; a thinker steps around it. The
wider and truer the real gap between good and bad teams, the more there is to avoid — and
avoiding it is the entire payoff of thinking. Mr Random thrived against a *blurry* model's
field; against a *sharp* one, blind picking costs more. The coin is still alive on two
lives, and every win it takes is solo — so it remains the most dangerous single entry in
the field. It's just no longer *winning* this on the numbers. Thinking, it turns out, pays
exactly to the extent that the world is legible — and we just made it more legible.

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
time working out who gets to be *alone*. It has crowned a two-man race, rated a one-life
board level with a two-life cushion, and — having finally been made honest — quietly
concluded that the coin it once feared is only the third-best thing in the room. The
octopus grows sharper; the game grows crueller; and somewhere in the field a random number
generator is about to make its pick without a single thought in its head. 🐙
