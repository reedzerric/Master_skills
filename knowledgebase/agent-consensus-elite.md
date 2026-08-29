---
name: agent-consensus-elite
description: 'How a swarm of agents reaches agreement: the Adjudicator pattern (Proposers generate, Refiners tweak, Adjudicator audits and scores), consensus algorithms for spatial and task allocation, distributed auction protocols, and pheromone-style reinforcement of successful branches. Use when multiple agents return conflicting outputs, when candidate answers need scoring and picking between, or when work must be allocated across a swarm. For spawning and orchestrating the swarm itself, use agent-swarms-elite.'
version: 1.1.0
category: ai_infrastructure
triggers: [my agents disagree with each other, how do agents pick a winner, score candidate agent outputs, adjudicator pattern, allocate tasks across agents, swarm coordination, consensus between agents]
dependencies: [agent-swarms-elite]
inputs: [candidate outputs from multiple agents, a task to allocate across a swarm]
outputs: [an adjudication design, a consensus or auction protocol]
tags: [knowledge, agents, consensus, coordination, swarm, adjudicator]
links: ['[[agent-swarms-elite]]', '[[security-agentic-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-kb
---

# Agent Consensus & Coordination (2026)

## 🎯 Purpose
Guidelines for implementing consensus algorithms and coordination mechanisms for decentralized agent swarms.

## 🛠️ The Process / Fact

### 1. The Adjudicator (Validator) Pattern
- **Standard:** Use a specialized "Adjudicator" agent to resolve conflicts and validate swarm outputs.
- **Workflow:** **Proposers** (generate candidates) -> **Refiners** (tweak top candidates) -> **Adjudicator** (final audit and score).
- **Grounding:** Adjudicators score candidates for safety, grounding (RAG accuracy), and constraint satisfaction.

### 2. Consensus Algorithms
- **Average & Max-Min Consensus:** Used for spatial coordination (e.g., formation control) and parallel task allocation. Agents update their state based on their neighbors' states.
- **Graph-of-Agents (GoA):** A graph-based framework to select relevant agents, establish communication links, and aggregate responses efficiently.
- **Distributed Auction Protocols:** Agents bid for tasks based on local cost functions. The winning bid is validated against global constraints by an Adjudicator.

### 3. Biological Coordination Patterns
- **Evaporation & Reinforcement:** MIMIC biological pheromone trails. Apply "evaporation" to low-yield logic branches (reducing weight) and "reinforcement" to successful paths.
- **Flocking Behavior:** For spatial agents, use decentralized "virtual navigators" to maintain formation while avoiding obstacles.

## ⚠️ Known Quirks or Edge Cases
- **Consensus Latency:** High-cardinality swarms (500+ agents) require optimized, graph-based protocols to avoid latency explosion.
- **Hallucinated Handoffs:** Adjudicators are CRITICAL to prevent "drift" as tasks pass through a swarm.

## 🔗 Related Memories
- [[skills/infrastructure/agent-swarms-elite]]
- [[knowledgebase/security-agentic-elite]]
