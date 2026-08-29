---
name: roguelike-scoring
description: Design a Balatro-style multiplicative scoring engine — a chips-plus-multiplier core, a hand/combo evaluation table, a deterministic modifier resolution order, and escalating score targets. Use when building a roguelike deckbuilder, a dice or card scoring system, or when scores are exploding out of control and the modifier stacking needs a defined order. For tuning the economy and rarity around such a system, use run-economy-balancing.
version: 1.0.0
category: game_design
triggers: [balatro, chips and mult, scoring system, combo scoring, roguelike deckbuilder, dice scoring, yahtzee, score target, joker stacking]
dependencies: []
inputs: [a hand or roll of game pieces, equipped modifiers, the current score target]
outputs: [a scoring table, a resolution order spec, a target curve]
tags: [game_design, roguelike, scoring, mechanics, balance]
links: ["[[run-economy-balancing]]", "[[narrative-event-system]]"]
confidence_score: 0.85
date: 2026-08-15
task_ref: skill-consolidation
---

# Roguelike Scoring

Build the multiplicative scoring core that makes a roguelike deckbuilder feel
explosive rather than arithmetic. It does ONE thing: define how a play converts
into a number. It does not tune the reward curve or rarity tiers (that is
`[[run-economy-balancing]]`), and it does not handle narrative gating.

## Operating Posture

You are a systems designer whose success metric is the moment a player realizes
their build multiplies. The core insight of the genre is that *additive* bonuses
are boring and *multiplicative* ones are addictive — but multiplication without a
defined resolution order produces both unplayable exploits and unreproducible
bugs. Your job is to make the explosion intentional.

## Hard Rules

1. **Two accumulators, never one.** Keep chips (additive base) and multiplier
   (multiplicative) separate until the final step. Collapsing them into a single
   score value destroys the entire design space.
2. **Resolution order is part of the rules, not an implementation detail.**
   Modifiers resolve left-to-right in equip order. Publish this; players will
   optimize around it, and that optimization *is* the metagame.
3. **Every modifier declares which accumulator it touches.** `+chips`,
   `+mult`, or `×mult`. A modifier that ambiguously "boosts scoring" is
   unimplementable and untestable.
4. **`×mult` is the scarce resource.** Additive multiplier bonuses are common;
   multiplicative ones are rare and are what a build is built around.
5. **Cap nothing silently.** If a value needs a ceiling, the ceiling is a
   visible rule with a stated reason, not a clamp buried in the scoring
   function.
6. **Scoring must be deterministic given (hand, modifiers, state).** Any
   randomness resolves *before* scoring begins, never during.

## Workflow

### Phase 1 — Define the play state machine

Establish the loop that produces a scorable hand. The Yahtzee-style shape:

- **INIT** — draw the pieces (e.g. 5 dice). Roll counter = 0.
- **ROLL** — re-roll unlocked pieces; increment counter. Player may toggle locks
  freely and play single-use consumables ("set a die to 6", "gain +1 roll").
  Loops while rolls remain.
- **SCORE** — evaluate the best combo, compute base chips and base mult, then
  trigger equipped modifiers in order. Add the product to the round score.
- **EVAL** — if round score ≥ target, win the round and open the shop. If plays
  remaining = 0 and target unmet, the run ends.

**Completion criterion:** every transition has an explicit trigger, and it is
unambiguous when the player loses agency over the hand.

### Phase 2 — Build the combo table

Base values for each recognized combination. The spread between adjacent tiers
should be roughly 1.5×–2× on chips and grow faster on mult at the top end.

| Hand | Description | Base Chips | Base Mult |
| :--- | :--- | :--- | :--- |
| High Die | Highest single value (fallback) | Die × 5 | 1 |
| Pair | 2 of same value | 10 + (Die × 2) | 2 |
| Two Pair | Two distinct pairs | 20 + (Dice × 2) | 2 |
| Three of a Kind | 3 of same value | 30 + (Die × 3) | 3 |
| Straight | 5 sequential | 40 + (sum) | 4 |
| Full House | 3 + 2 | 40 + (sum) | 4 |
| Four of a Kind | 4 of same value | 60 + (Die × 4) | 7 |
| Five of a Kind | all 5 same | 120 + (Die × 5) | 12 |

Note the deliberate mult jump at Four of a Kind (4 → 7) and Five (7 → 12). Those
discontinuities are where build identity forms.

**Completion criterion:** no two hands have identical (chips, mult) pairs, and
every hand is reachable.

### Phase 3 — Specify modifier resolution

```
final = (base_chips + Σ modifier_chips) × (base_mult + Σ modifier_add_mult) × Π modifier_x_mult
```

Modifiers evaluate strictly left-to-right in equip slot order. A modifier that
reads the current accumulator sees the value *after* all modifiers to its left
have applied.

```python
def score_hand(hand: Hand, modifiers: list[Modifier]) -> int:
    chips, mult = COMBO_TABLE[hand.kind](hand)
    for mod in modifiers:                    # equip order is load-bearing
        chips, mult = mod.apply(chips, mult, hand)
    return int(chips * mult)
```

**Completion criterion:** two identical modifier sets in different slot orders
produce different scores, and the difference is explicable from the rules alone.

### Phase 4 — Set the target curve

Targets escalate faster than linear or the late run trivializes. A workable
shape is geometric with a per-act step:

```
target(depth) = base × growth ** depth
```

with `growth` around 1.6–1.8 for a 8–12 depth run. Validate by simulating a
median build against the curve — the intended failure point should be
depth 6–8 for an average run, not depth 2 and not never.

**Completion criterion:** a simulated median build fails somewhere in the
intended band, and a simulated optimal build clears the full run with margin.

### Phase 5 — Node/path structure

Replace linear stages with a branching risk/reward map:

- **Encounter** — standard target. Safe. Reward: base currency.
- **Elite / Rift** — high target plus a punishing round modifier. Reward: large
  currency plus a guaranteed rare modifier. Risk: a permanent curse if the
  player overspends rolls.
- **Shop** — spend currency on modifiers, consumables, and upgrades.
- **Rest** — recover, or convert the node into a permanent upgrade.

Offer 2–3 choices per depth. A single path is a treadmill.

**Completion criterion:** at every depth the player faces a decision with a
stated tradeoff, not a forced route.

## Known Quirks & Edge Cases

- **Unbounded `×mult` stacking overflows.** Three multiplicative modifiers that
  each grow with a counter will exceed a 64-bit integer within a long run. Use a
  float score with a displayed scientific notation above a threshold, or cap the
  count of `×mult` slots.
- **Best-hand evaluation is not obvious with wildcards.** Once a piece can
  substitute, "best combo" requires searching all substitutions — and the
  highest-chip hand is not always the highest-scoring hand once modifiers apply.
  Evaluate against final score, not against the base table.
- **Order-dependence confuses players who cannot reorder.** If equip order
  matters, the UI must let the player rearrange it. Otherwise the rule is a
  hidden tax rather than a decision.
- **`Straight` and `Full House` sharing a tier is intentional** — it gives two
  different build paths the same power level. Do not "fix" it by differentiating
  them without a reason.
- **Consumables that mutate the hand break replay determinism** unless their
  effect is recorded in the play log. Log the post-consumable hand state, not
  the pre-.

## Related
- [[run-economy-balancing]] — currency, rarity tiers, and reward pacing
- [[narrative-event-system]] — gating content on run state
