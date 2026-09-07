# Prediction 01 — how the season plays out (after Round 3)

*A forecast from 20,000 Monte-Carlo simulations of the rest of the season, run from
the current state: everyone's used-team lists, their remaining lives, and the
projected win-probabilities for all 34 remaining rounds. Each simulated player picks
their best available team each week (greedy survival — the field's observed
behaviour); match outcomes are sampled per team, so everyone on the same team shares
the same fate. Archived as-is; we'll re-run it as the field thins.*

---

## 1. The field collapses fast, then freezes

```
Avg still alive:  24 → 18 (R7) → 12 (R10) → 7 (R16) → ~4 (R19) → stalls at ~4 to the end
```

The carnage is almost entirely **rounds 4–19**. The pool goes from 24 to about four in
fifteen weeks — and then **eliminations essentially stop**. Once it's down to a handful
of players on full lives picking bankers, they almost never all fail (and the all-lose
rule protects a unanimous slip). ~4 survivors is a stable attractor that coasts to the
final whistle. **First elimination: median Round 5 — i.e. next week.** The cull starts
now.

## 2. It probably ends in a split

| Outcome | Probability |
|--|--|
| **Solo winner** | **33%** |
| Split (2+ ways) | **67%** |

Solo is the single most likely *exact* result (33%), but *some* kind of split is twice
as likely overall — most often 2–5 ways. A strong echo of the World Cup (85% split
there). The structure pushes toward a shared pot.

## 3. Why — and who can actually win it *outright*

This is the whole story, and it's the World Cup lesson made flesh:

| Player | Lives | In-money | **Solo win** | |
|--|--|--|--|--|
| Bobby A / Josh Wansell / Jp C | 3 | 36% | **0%*** | clone bloc — best survival, 0% solo *in the sim* |
| **Jimmy D** | 3 | 34% | **9.1%** | 3 lives **and** differentiated — best-placed |
| **Malley** | 2 | 25% | **7.0%** | the maverick's edge |
| the 7-strong Arsenal bloc | 2 | 18% ea | **0%* ea** | seven players, 0% solo *in the sim* |
| Smarshy | 1 | **3%** | ~0% | one life — survival, not victory (yet) |

**\*Read that 0% carefully — it's an artifact of the model, not a rule of the game.**
Because a clone bloc shares an identical used-list *and* the sim picks greedily (best
available), its members make the same pick every week and so **never separate** — which
forces their solo chance to exactly zero. In *reality* a clone is free to pick a
different unused team, break the symmetry, and win alone. It's just (a) against
everything this field has done so far, and (b) game-theoretically **dominated** — the
World Cup's *volunteer's dilemma*: the player who breaks away usually just gifts the
solo win to the twin who stayed put. So it's **very unlikely and self-defeating, not
impossible.**

The takeaway holds either way: the blocs with the *highest survival* are the ones with
*least* claim on the whole pot — they're built to split. **Malley's 7% is real,
free-standing solo equity; the seven Arsenal clones would each have to *actively break
formation* to earn any.** Differentiation is the road to winning outright, and Malley's
"difficult mode" travels it for nothing — the same instinct that won him the World Cup
LMS. (The sim is even *harsh* on him: it plays him greedily, so his true solo chance is
higher than 7%.)

## 4. The prediction, in a sentence

**The field halves by October and settles into a stable ~3–4 survivors who most likely
carve up the pot — unless one of the differentiated players (Jimmy D on three lives, or
Malley on his maverick path) is the last one standing when the herd finally hits a bad
week.** Watch for the round a big banker slips (a City or a Chelsea, the way Liverpool
did in Round 2): *that's* the moment the clone blocs get gutted en masse and a lone wolf
inherits the whole thing.

## 5. And Smarshy, honestly 🐟

**A long shot — ~3%, effectively 0% to win outright right now.** On one life, one more
non-win ends it, and he'd need to win essentially every remaining pick *and* be one of
the final four. The dream isn't dead — his used-list is fairly unique, so if he claws
back to two or three lives he inherits Malley-style solo upside. But that's chapters
away. Right now the only forecast that matters is: **win the next one, then the next
one, then breathe.** Survival first; the winning comes later, if it comes.

---

*Model caveats: the sim assumes greedy survival play and the field's current herding
behaviour; it understates the mavericks (who differentiate more than greedy) and
assumes clones never break formation. Projected win-probabilities beyond the next round
or two are model estimates, re-anchored to real odds each week.*
