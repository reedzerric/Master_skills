---
name: sre-incident-protocol
description: 'Running production incidents and the reliability discipline around them: automated paging and channel creation, tail-based SLIs on p95 and p99 latency, SLO-as-code with error budgets that gate releases, blameless post-mortems focused on systemic causes, and scheduled gamedays. Use when an incident is live, when writing a post-mortem, or when setting SLOs and error budgets. For deliberately injecting failure, use chaos-engineering-elite.'
version: 1.1.0
category: core
triggers: [we have a production incident, write a post mortem, set an slo, error budget exhausted, p99 latency spike, page the on call engineer, run a gameday, build an incident timeline]
dependencies: [observability-elite]
inputs: [an active incident and its telemetry, reliability targets]
outputs: [an incident timeline, a blameless post-mortem, SLO definitions as code]
tags: [misc, sre, reliability, slo, post-mortem, incident]
links: ['[[observability-elite]]', '[[system-design-elite]]', '[[chaos-engineering-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch2
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
