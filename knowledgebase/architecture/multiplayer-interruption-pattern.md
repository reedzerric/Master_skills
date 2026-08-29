---
name: multiplayer-interruption-pattern
description: In turn-based games where players need to interact out-of-turn (e.g., playing 'Disruption' or 'Reaction' cards), the standard 'Current Player' state logic is insufficient. Use when working with architecture, multiplayer, frontend.
version: 1.0.0
category: core
triggers: [architecture, multiplayer, frontend, state-management, interruption, pattern]
dependencies: []
inputs: [source files, project config]
outputs: [refactored code, review findings]
title: Multiplayer Interruption-Response Pattern
date: 2026-03-08
confidence_score: 0.95
tags: [architecture, multiplayer, frontend, state-management]
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
