---
name: agent-handoff-elite
description: 'Passing work between agents without losing intent: the protocol stack, Structured State Objects that carry task state, and the practices that preserve why a decision was made rather than only what was decided. Use when one agent must continue another''s work, when context is about to run out, or when briefing a subagent. For compacting a human conversation into a document, use handoff.'
version: 1.1.0
category: ai_infrastructure
triggers: [pass work to another agent, agent is losing context, structured state object, brief a subagent, continue another agents work, preserve intent across sessions]
dependencies: [agent-swarms-elite]
inputs: [an in-flight task and its state]
outputs: [a structured handoff object, a continuation brief]
tags: [infrastructure, agents, protocol, handoff, a2a, state-transfer]
links: ['[[agent-swarms-elite]]', '[[handoff]]', '[[agent-consensus-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
---

# Agent Handoff Protocols (2026)

## 🎯 Purpose
Guidelines for implementing reliable, state-aware handoffs between specialized agents to prevent intent drift and context explosion.

## 🛠️ The Process / Fact

### 1. The 2026 Protocol Stack
- **A2A (Agent-to-Agent):** Standard for horizontal coordination and capability discovery. Uses "Agent Cards" (JSON) to negotiate tasks.
- **MCP (Model Context Protocol):** Standard for connecting agents to tools/data. Ensures the receiving agent has the same "plumbing."
- **ACP (Agent Collaboration Protocol):** Governance layer for enterprise security and PII protection during transfers.

### 2. Structured State Objects (SSO)
- **Intent Object:** Do NOT pass raw chat history. Pass a validated JSON "Intent Object" (Goal, Constraints, "Done" Criteria).
- **Checkpoints:** Handoffs must be idempotent. If a transfer fails, the receiver resumes from the last tool-call checkpoint.
- **Selective Context:** Only transfer "evidence references" and key reasoning steps to keep the receiver's context window focused.

### 3. Intent Preservation Best Practices
- **Negative Constraints:** Explicitly list what an agent MUST NOT do (e.g., "Do not exceed $100 budget").
- **HITL Clarification:** If the "Intent Router" flags ambiguity, trigger a human-in-the-loop (HITL) step rather than passing a vague task.

## ⚠️ Known Quirks or Edge Cases
- **Context Bloat:** Passing too much data (raw logs) confuses the receiver. Pass the "Summary of Progress" instead.
- **Infinite Handoff Loops:** Two agents passing a task back and forth without resolution. Use a "Circuit Breaker" based on handoff counts.

## 🔗 Related Memories
- [[skills/infrastructure/agent-swarms-elite]]
- [[knowledgebase/security-agentic-elite]]
