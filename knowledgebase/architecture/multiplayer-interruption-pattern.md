---
name: multiplayer-interruption-pattern
description: State design for turn-based games where players act out of turn, such as reaction or disruption cards, which a plain 'current player' state machine cannot express. Use when an out-of-turn action must interrupt the active turn, or when a reaction window has to resolve before normal play resumes. For the actor-model formalism underneath, use xstate-formalism-elite.
version: 1.1.0
category: core
triggers: [player acts out of turn, reaction card, interrupt the current turn, out of turn interaction, turn based state machine, disruption card timing]
dependencies: []
inputs: [a turn-based game's state model]
outputs: [an interruption-aware state design]
tags: [architecture, multiplayer, frontend, state-management]
links: ['[[xstate-formalism-elite]]']
confidence_score: 0.95
date: '2026-08-29'
task_ref: routing-repair-kb
---

# Multiplayer Interruption-Response Pattern

## Context
In turn-based games where players need to interact out-of-turn (e.g., playing 'Disruption' or 'Reaction' cards), the standard 'Current Player' state logic is insufficient.

## Implementation Standard

### 1. The INTERRUPTED State
Introduce an INTERRUPTED state to the global game status. When a card is played out of turn:
- The game enters INTERRUPTED.
- Most standard actions (rolling, ending turn, advancing level) are locked.
- The TargetingState becomes the primary driver of the UI.

### 2. Targeting Resolution
Every resolution of a targeting action MUST reset the status back to PLAYING or the previous active state.

### 3. Global Interaction Hub
Instead of only showing the current player's resources, implement a 'Global Hub' or 'Player Hub' that renders interaction points (e.g., PlayerHand) for all participants simultaneously. This allows non-active players to initiate actions at any time.

[[knowledgebase/architectural-patterns]]
