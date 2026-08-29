---
name: chaos-engineering-elite
description: 'Proving resilience by breaking things on purpose: forming a steady-state hypothesis, running experiments continuously in a pipeline rather than once a year, and bounding blast radius with explicit abort conditions. Use when you need evidence a system survives failure, when designing a fault-injection experiment, or when a gameday needs abort criteria. For running a real incident, use sre-incident-protocol.'
version: 1.1.0
category: core
triggers: [chaos experiment, fault injection, prove the system survives failure, steady state hypothesis, limit the blast radius, kill a pod on purpose, resilience testing]
dependencies: [observability-elite]
inputs: [a system and its steady-state metrics]
outputs: [an experiment design, abort conditions, resilience findings]
tags: [infrastructure, devops, chaos, resilience, kubernetes, ai]
links: ['[[sre-incident-protocol]]', '[[observability-elite]]', '[[system-design-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
---

# Chaos Engineering & Continuous Resilience (2026)

## 🎯 Purpose
Guidelines for architecting self-healing systems and validating their resilience through continuous fault injection.

## 🛠️ The Process / Fact

### 1. The Steady State Hypothesis
- **Business Focus:** Define "normal" based on business metrics (e.g., checkout success rate) rather than just system metrics (CPU/RAM).
- **Metric:** "99.9% of requests return 2xx within 500ms."

### 2. Continuous Resilience Pipelines
- **Integration:** Chaos is a stage in CI/CD. Use **Chaos Mesh** or **Gremlin** to block deployments if a service fails to self-heal.
- **AI-Driven Discovery:** Use agentic tools (e.g., Krkn-AI) to automatically scan clusters and generate exploratory experiments to find architectural weak points.

### 3. Blast Radius & Abort Conditions
- **Start Small:** Begin with 1% of traffic or a single pod.
- **Automated Abort:** If steady-state metrics deviate beyond a threshold (e.g., error rate > 5%), the experiment must terminate and rollback instantly.

## ⚠️ Known Quirks or Edge Cases
- **Cascading Failures:** Be careful with network partitions; they can trigger retry-storms that crash downstream services. Implement **Circuit Breakers** first.
- **AI Systems:** Chaos test AI models with synthetic "noisy" data to detect drift or graceful failure modes.

## 🔗 Related Memories
- [[skills/infrastructure/observability-elite]]
- [[knowledgebase/system-design-elite]]
