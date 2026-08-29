---
name: security-agentic-elite
description: Guidelines for architecting secure, autonomous AI agents and mitigating the OWASP Agentic Top 10 (ASI). Use when working with knowledge, security, ai.
version: 1.0.0
category: core
triggers: [knowledge, security, ai, agents, owasp, zero-trust, agentic]
dependencies: [agent-swarms-elite]
inputs: [source files, project config]
outputs: [refactored code, review findings]
title: Agentic AI Security (2026)
date: 2026-03-08
task_ref: all-facets-expansion
confidence_score: 1.0
tags: [knowledge, security, ai, agents, owasp, zero-trust]
links: ["[[agent]]"]
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
