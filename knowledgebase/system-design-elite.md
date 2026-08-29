---
name: system-design-elite
description: 'Designing for six-nines availability: PACELC trade-offs between consistency and latency, active-active geo-distribution, cell-based architecture to contain blast radius, CRDTs and Merkle anti-entropy for drift, circuit breakers, and tunable per-request consistency. Use when choosing between consistency and availability, containing the blast radius of a failure, or designing multi-region. For DDD and module boundaries, use architectural-patterns.'
version: 1.1.0
category: core
triggers: [consistency versus availability, multi region architecture, cap theorem, pacelc, contain the blast radius, cell based architecture, read your writes, eventual consistency drift]
dependencies: [observability-elite]
inputs: [availability and consistency requirements]
outputs: [a consistency strategy, a multi-region topology]
tags: [knowledge, architecture, ha, cap, pacelc, distributed]
links: ['[[observability-elite]]', '[[architectural-patterns]]', '[[chaos-engineering-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-kb
---

# High-Availability System Design (2026)

## 🎯 Purpose
Guidelines for architecting "Six 9s" (99.9999%) geo-distributed systems.

## 🛠️ The Process / Fact

### 1. PACELC Trade-off Strategy
- **P (Partition):** Choose **Availability (AP)** for low-stakes interactions (Add to Cart) or **Consistency (CP)** for high-stakes ones (Checkout).
- **E (Else/Normal):** Trade off between **Latency (L)** and **Consistency (C)**.

### 2. High-Availability Patterns
- **Active-Active Geo-Distribution:** Serve traffic from multiple regions simultaneously to eliminate cold starts.
- **Cell-Based Architecture:** Partition the stack into isolated "cells" to contain the blast radius of any failure.
- **Eventual Consistency:** Manage data drift using **CRDTs (Conflict-free Replicated Data Types)** and background **Merkle Tree** anti-entropy repairs.
- **Circuit Breakers & Retries:** Implement standard patterns for handling downstream outages without cascading failures.

### 3. Reliability Standards
- **Read-Your-Writes:** Ensure a user always sees their own updates immediately, even in an AP system.
- **Tunable Consistency:** Allow per-request consistency levels (e.g., `QUORUM` vs. `LOCAL_ONE`).

## ⚠️ Known Quirks or Edge Cases
- **The Coordination Tax:** Avoid complex distributed state unless necessary. Prefer "Modular Monoliths" for teams under 50 engineers.
- **Eventual Consistency Lag:** Always design UI to handle the lag (e.g., optimistic updates).

## 🔗 Related Memories
- [[skills/infrastructure/observability-elite]]
- [[knowledgebase/architectural-patterns]]
