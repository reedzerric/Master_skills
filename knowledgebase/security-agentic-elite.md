---
name: security-agentic-elite
description: 'Securing autonomous agents against the OWASP Agentic Top 10: the Intent Capsule pattern so a model never calls a tool directly, zero-trust agent identity with just-in-time scoped permissions, runtime SBOMs, semantic validation against context poisoning, and human cryptographic approval gates on high-impact actions. Use when an agent can call tools, move money, or touch production. For data privacy and erasure specifically, use privacy-by-design-elite.'
version: 1.1.0
category: core
triggers: [secure my agent, prompt injection defence, agent calling tools safely, owasp agentic top 10, limit what an agent can do, context poisoning, human approval before an agent acts, scope agent permissions]
dependencies: [agent-swarms-elite]
inputs: [an agent design, its tool and data surface]
outputs: [a threat model, tool-permission scoping, human-in-the-loop gates]
tags: [knowledge, security, ai, agents, owasp, zero-trust]
links: ['[[agent-swarms-elite]]', '[[privacy-by-design-elite]]', '[[agentic-security-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-kb
---

# Agentic AI Security (2026)

## 🎯 Purpose
Guidelines for architecting secure, autonomous AI agents and mitigating the OWASP Agentic Top 10 (ASI).

## 🛠️ The Process / Fact

### 1. The Intent Capsule Pattern
- **Standard:** Never allow an LLM to call a tool directly. Use a deterministic "Intent Parser" to validate the request against a cryptographic "Intent Capsule."
- **Whitelist:** Tool use must be strictly whitelisted and scoped to the task.

### 2. Zero-Trust Tooling
- **Identity:** Treat every agent as a third-party user with its own session-based identity.
- **JIT Permissions:** Provide just-in-time, scoped permissions (e.g., "Read-only access to `/reports` for 5 minutes").

### 3. Supply Chain & Context Verification
- **Runtime SBOMs:** Verify all agent-used tools and libraries in real-time.
- **Context Integrity:** Use semantic validation on all RAG data to prevent context poisoning.
- **mTLS:** All inter-agent communication must be encrypted via mTLS and digitally signed.

### 4. Human-in-the-Loop (HITL)
- **High-Impact Actions:** Financial transfers, data deletion, and privilege escalations REQUIRE human cryptographic approval.
- **Reasoning Logs:** Agents must provide a transparent, step-by-step reasoning log before requesting approval.

## ⚠️ Known Quirks or Edge Cases
- **Prompt Injection:** Traditional firewalls are ineffective against goal hijacking. Use "Intent Hierarchies" to keep agents within their mandated objective.
- **Cascading Failures:** Use circuit breakers on autonomous workflows to prevent small errors from triggering destructive loops.

## 🔗 Related Memories
- [[agent]]
- [[knowledgebase/architectural-patterns]]
