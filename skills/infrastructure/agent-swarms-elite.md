---
name: agent-swarms-elite
description: 'Orchestrating multiple agents: the architectural patterns (supervisor, hierarchical, network), LangGraph state management, and role definitions that stop agents duplicating each other''s work. Use when one agent is not enough, when parallelising agent work, or when agents keep redoing the same task. For resolving their conflicting outputs, use agent-consensus-elite.'
version: 1.1.0
category: ai_infrastructure
triggers: [orchestrate multiple agents, supervisor agent pattern, langgraph state, agents duplicating work, parallelise agent tasks, multi agent architecture]
dependencies: [agent-handoff-elite]
inputs: [a task too large for a single agent]
outputs: [a swarm topology, role definitions, a graph state schema]
tags: [infrastructure, agents, swarm, langgraph, orchestration]
links: ['[[agent-consensus-elite]]', '[[agent-handoff-elite]]', '[[security-agentic-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
---

# Agent Swarm Orchestration (2026)

## 🎯 Purpose
Guidelines for architecting multi-agent systems (MAS) to solve complex, non-linear tasks with high reliability and low hallucination.

## 🛠️ The Process / Fact

### 1. Architectural Patterns
- **Hierarchical (Supervisor/Worker):** A central "Director" decomposes goals and assigns tasks to specialized workers. Best for sequential, high-precision tasks.
- **Peer-to-Peer (P2P/Swarm):** Agents communicate directly via handoffs. Highly resilient and parallelizable.
- **Blackboard:** Agents contribute independently to a shared state repository (the "Blackboard"). Best for exploratory/scientific research where the solution path is unknown.

### 2. State Management (LangGraph Standard)
- **State Persistence:** Use durable state machines (e.g., Redis-backed) to allow agents to "pause" and "resume" without losing progress.
- **Cycles & Loops:** Design logic with explicit "termination conditions" to prevent infinite agent loops.
- **Parallel Execution:** Execute independent tool calls or sub-agent tasks in parallel to minimize latency.

### 3. Roles & Responsibilities
- **Planner:** Defines the task hierarchy.
- **Executor:** Performs the actual work/tool calls.
- **Critic/Adjudicator:** Validates outputs against constraints and grounding data.

## ⚠️ Known Quirks or Edge Cases
- **Hallucination Propagation:** In hierarchical swarms, if the Supervisor fails to plan, workers will execute incorrect sub-tasks. Use "Critic" agents to validate the plan first.
- **Coordination Overhead:** For tasks under 3 steps, a single agent is faster. Only deploy a Swarm for complex, multi-domain problems.

## 🔗 Related Memories
- [[skills/infrastructure/agent-handoff-elite]]
- [[knowledgebase/agent-consensus-elite]]
