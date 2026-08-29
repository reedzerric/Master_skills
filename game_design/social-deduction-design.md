---
name: social-deduction-design
description: Design social deduction and murder mystery games against the psychological drives that make them work — theory-of-mind engagement, safe transgression, earned revelation, identity adoption, and shared narrative. Covers narrative-first clue generation (scene fragments over inventory labels), the three-layer story model, and secret distribution for offline play. Use when designing a hidden-role game, when clues feel like a form to fill in rather than a mystery, or when players disengage after elimination.
version: 1.0.0
category: game_design
triggers: [social deduction, murder mystery, hidden role, werewolf, clue design, deduction game, party game, secret distribution, roleplay game]
dependencies: [narrative-event-system]
inputs: [a player count, a scenario premise, a distribution mechanism]
outputs: [a clue generation model, role dossiers, a story layer spec, a distribution flow]
tags: [game_design, social_deduction, narrative, mystery, multiplayer]
links: ["[[narrative-event-system]]", "[[multiplayer-interruption-pattern]]"]
confidence_score: 0.85
date: 2026-08-15
task_ref: skill-consolidation
---

# Social Deduction Design

Design games where the product is the experience of reading another person and
being wrong about it. It does ONE thing: apply the psychology of social deduction
to mechanics and clue generation. It does not cover the networking layer, and it
does not design single-player narrative systems (that is
`[[narrative-event-system]]`).

## Operating Posture

You are designing around a specific neurological fact: deception synchronizes
players' brains more than truth does. The game is not a puzzle with social
decoration — the social inference *is* the product, and every mechanic either
feeds it or competes with it. When a mechanic adds cognitive load that is not
social inference, it is subtracting from the game.

## Hard Rules

1. **Uncertain inference is the product, not a failure state.** Being wrong
   about someone must feel like part of the experience, never like a bug.
   Maximize the moments of uncertain reading.
2. **Never replace social inference with another puzzle type.** Cryptography,
   logic grids, and code-breaking are extraneous cognitive load that crowds out
   the actual game. This is the single most common way the genre fails.
3. **Never strip a player of their character.** Elimination that removes
   identity removes investment. An eliminated player must retain a role.
4. **Every clue must be interpretable through reasoning.** A clue that can only
   be guessed rewards luck over attention and destroys earned revelation.
5. **The roleplay layer is load-bearing, not flavor.** It is the moral
   permission structure that makes lying to friends comfortable. Breaking
   immersion breaks the game.
6. **A host device never displays a secret in the clear.** Secrets route to the
   owning player's own device.

## The Psychological Drives

Design decisions trace back to these. When a mechanic is in question, ask which
drive it serves.

**Theory of mind engagement.** Deception is the most cognitively demanding
social act a person can perform — suppressing truth, constructing a false
narrative, monitoring its consistency, and modeling opponents simultaneously.
*Implication:* maximize moments of uncertain inference; do not reduce them with
mechanics that resolve ambiguity.

**Safe transgression.** Games provide a moral frame where deception is
celebrated rather than corrosive. Players resolve the dissonance by citing the
game context, and that resolution is cathartic. *Implication:* the dossier and
script are the permission structure. Protect immersion.

**Earned revelation.** The "aha" is neurologically distinct from random
discovery — satisfaction requires believing that careful attention *caused* the
solution. *Implication:* attention must beat guessing, measurably.

**Identity adoption.** Even brief roleplay creates experience-taking: players
temporarily shift self-concept toward the character, perceiving themselves as
more cunning or theatrical. It is why betrayal stings. *Implication:* never
strip the character.

**Social bonding through shared narrative.** Sessions produce stories that
outlast them — "remember when you accused Katherine and she was innocent" is the
metagame. Groups return for accumulated emotional history, not the puzzle.
*Implication:* design for memorable failure, not just clean resolution.

## Workflow

### Phase 1 — Diagnose the clue model

The default failure: the generator picks three independent facts — a location, a
time, a weapon — and distributes them as secret cards. The result is logically
solvable and narratively hollow.

What players experience:

> Killer's secrets: `"The Duke's Study"` / `"Midnight"` / `"Belladonna Extract"`
> Innocent's secrets: `"Gambling Ledger"` / `"Opium Pipe"` / `"Stolen Silver Spoon"`

Those are inventory items, not clues. No *why*, no *how*, no discovery.
Assembling them feels like completing a form.

**Root cause:** the engine generates the *answer* and fragments it, instead of
generating a *story* and letting the answer be discoverable inside it.

**Completion criterion:** you can state whether the current generator is
answer-first or story-first.

### Phase 2 — Adopt narrative-first generation

Every clue is a **scene fragment** — a moment in time, an overheard
conversation, an object in context — never a label. Assembled, the killer's
fragments should read like a confession written in invisible ink across several
testimonies.

Label form: `"Belladonna Extract"`

Scene-fragment form: *"You saw Lady Ashcombe leave the conservatory at a quarter
past eleven, wiping her hands on a handkerchief she then did not put back in her
pocket."*

The second one implicates, exonerates, or misleads depending on what else is
known. The first is a noun.

**Completion criterion:** no distributed clue is a bare noun phrase.

### Phase 3 — Build the three story layers

```
Layer 1 — THE SURFACE        (what everyone sees)
  The Duke was found dead. The estate is locked. Someone in this room did it.

Layer 2 — THE TANGLE         (what suspects claim publicly)
  Conflicting alibis. Suspicious observations. Every story has holes.
  Innocents tell truths that accidentally implicate others.

Layer 3 — THE TRUTH          (what actually happened)
  A single coherent sequence of events. Every fragment in Layer 2 is a true
  observation of some part of it, seen from the wrong angle.
```

The design constraint that makes it work: **innocents must generate suspicion by
telling the truth.** A game where only the killer lies is a game of spotting the
liar. A game where honest testimony implicates the innocent is a game of
inference.

**Completion criterion:** at least one innocent's truthful fragment points at a
different innocent.

### Phase 4 — Design elimination that preserves identity

Dead players in classic hidden-role games disengage because they were stripped of
their character and given nothing to invest in. Options that preserve identity:

- The eliminated become a distinct role with its own goal (ghost, coroner,
  historian) rather than a spectator
- Their information enters the game in a constrained form they choose how to spend
- The game is short enough that elimination is brief — but this is the weakest
  option, because it treats the symptom

**Completion criterion:** no game state exists in which a player has no role.

### Phase 5 — Distribute secrets without a shared screen

For offline play, the host device must never render a secret in the clear.
Sequential QR handoff works:

```
              ┌────────────────────────┐
              │   Host (shared app)    │
              │  Tracks round & state  │
              └───────────┬────────────┘
                          │ setup QRs
                          ▼
┌──────────┐        ┌──────────┐        ┌──────────┐
│ Player A ├───────>│ Player B ├───────>│ Player C │
│(Dossier) │        │(Dossier) │        │(Dossier) │
└──────────┘        └──────────┘        └──────────┘
```

1. Host selects player count and scenario.
2. Host displays a sequence of QR codes — "Player 1 scan", "Player 2 scan".
3. Each code resolves to that player's dossier on *their own* device: role,
   background, public alibi, secrets, and acting tips.

Encode either as a lookup (`/d/<dossier_id>`, resolved server-side) or as a
fully offline payload (`/reveal?data=<base64>`). The offline form matters — a
party game that requires connectivity fails at the venue.

**Completion criterion:** a full setup completes with the host screen never
showing a secret, and works with the network off.

## Known Quirks & Edge Cases

- **Cryptography puzzles kill the genre.** This is the documented failure of
  Hunt A Killer — pivoting to code-breaking replaced social inference with
  extraneous load. If a mechanic makes players stop watching each other's faces,
  cut it.
- **Base64 dossiers in a URL leak via history and screenshots.** Acceptable for
  a party game among friends; not acceptable if the same code ships anywhere
  competitive.
- **The killer's clue set must be solvable but not trivially so.** Test by
  giving a fresh reader only the killer's fragments — if they name the killer in
  under a minute, the fragments are too explicit.
- **Acting tips are not optional.** Players who do not know how to perform their
  character default to silence, and silence reads as guilt regardless of role,
  poisoning the inference.
- **QR handoff order leaks information.** If the host always generates the
  killer's code in a fixed position, observant players will notice. Randomize.
- **Odd player counts break symmetric role distributions.** Decide the behavior
  at every supported count before shipping, not at the table.

## Related
- [[narrative-event-system]] — the schema patterns for authoring scenario content
- [[multiplayer-interruption-pattern]] — handling players dropping mid-session
