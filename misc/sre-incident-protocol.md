---
name: sre-incident-protocol
description: Guidelines for managing production incidents and maintaining "Six 9s" reliability through automated coordination and systemic learning. Use when working with sre, reliability, slo.
version: 1.0.0
category: core
triggers: [sre, reliability, slo, post-mortem, incident, protocol]
dependencies: [observability-elite]
inputs: [source files, project config]
outputs: [refactored code, review findings]
title: SRE Incident Response & Reliability (2026)
date: 2026-03-08
task_ref: mit-professor-phase-3
confidence_score: 1.0
tags: [misc, sre, reliability, slo, post-mortem, incident]
links: ["[[skills/infrastructure/observability-elite]]"]
---

# SRE Incident Response & Reliability (2026)

## 🎯 Purpose
Guidelines for managing production incidents and maintaining "Six 9s" reliability through automated coordination and systemic learning.

## 🛠️ The Process / Fact

### 1. The Incident Lifecycle
- **Automated Coordination:** Use tools (Rootly/Incident.io) to auto-create Slack channels and page on-call engineers upon detection.
- **Tail-Based SLIs:** Monitor p95/p99 latency. "Slow is the new down"—spikes are SEV-1.
- **SLO-as-Code:** Version reliability targets in Git (OpenSLO) to gate deployments. If the **Error Budget** is exhausted, halt feature releases.

### 2. Blameless Post-Mortems
- **Focus:** Identify systemic failures (workflow, tools), never individual blame.
- **Timeline:** Document actions taken, observed effects, and expectations vs. reality.
- **Action Items:** Must be concrete, assignable, and tracked to completion to reduce the "Repeat Incident Rate."

### 3. Gameday Standards
- **Scheduled Failure:** 4-6 weeks of prep for intentional fault injection.
- **Objectives:** Measurable (e.g., "Replica promotion completes in < 300s").
- **Debrief:** Hold within 48 hours while the timeline is fresh.

## ⚠️ Known Quirks or Edge Cases
- **Telemetry Budgeting:** Avoid "collect everything" defaults to manage costs. Focus on high-value signals.
- **AI Investigation:** Use AI for data retrieval, but human intuition must drive the final root cause analysis.

## 🔗 Related Memories
- [[skills/infrastructure/observability-elite]]
- [[knowledgebase/system-design-elite]]
