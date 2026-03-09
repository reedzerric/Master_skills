---
title: High-Availability System Design (2026)
date: 2026-03-08
task_ref: all-facets-expansion
confidence_score: 1.0
tags: [knowledge, architecture, ha, cap, pacelc, distributed]
links: ["[[skills/infrastructure/observability-elite]]"]
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
