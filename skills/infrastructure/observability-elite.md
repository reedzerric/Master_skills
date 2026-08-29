---
name: observability-elite
description: 'Production observability: the PLTG stack, OpenTelemetry instrumentation as the default everywhere, and patterns for correlating traces, logs and metrics without collecting everything. Use when an issue cannot be diagnosed from existing telemetry, when instrumenting a new service, or when telemetry cost is out of control. For incident process, use sre-incident-protocol.'
version: 1.1.0
category: core
triggers: [cannot diagnose this from the logs, instrument a service, opentelemetry setup, correlate traces and logs, telemetry cost is too high, what should i be measuring, distributed tracing]
dependencies: [github-actions-elite]
inputs: [a service to instrument, an undiagnosable issue]
outputs: [instrumentation code, a telemetry pipeline, dashboards and alerts]
tags: [infrastructure, observability, opentelemetry, ebpf, pltg]
links: ['[[sre-incident-protocol]]', '[[chaos-engineering-elite]]', '[[finops-value-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
---

# Enterprise Observability & Monitoring (2026)

## 🎯 Purpose
Guidelines for architecting unified, actionable, and cost-aware observability systems.

## 🛠️ The Process / Fact

### 1. The PLTG Stack (Modern Standard)
- **Prometheus:** Metrics with auto-service discovery.
- **Loki:** Logs with metadata-only indexing for cost efficiency.
- **Tempo:** Distributed tracing using object storage (e.g., S3/GCS).
- **Grafana:** The single pane of glass for all data.

### 2. OpenTelemetry (OTel) Everywhere
- **Standard:** Use OpenTelemetry SDKs for all instrumentation to avoid vendor lock-in.
- **OTel Collectors:** Use as "telemetry routers" to filter, sample, and redact data before it reaches the backend.

### 3. Advanced 2026 Patterns
- **eBPF Telemetry:** Use eBPF for non-invasive, kernel-level visibility (TCP latency, syscalls) without app-code instrumentation.
- **AIOps (MTTR Reduction):** Integrate AI-driven root cause analysis (RCA) to group related incidents and suggest remediation steps.
- **Cost-Aware Telemetry:** Implement adaptive sampling to reduce storage costs by up to 80% while retaining critical signals.

## ⚠️ Known Quirks or Edge Cases
- **Cardinality Explosion:** Avoid using unique User IDs as Prometheus metric labels. Use high-cardinality platforms (like Honeycomb) for that data instead.
- **Semantic Conventions:** Enforce standard naming (e.g., `service.name`, `http.status_code`) across all teams for unified querying.

## 🔗 Related Memories
- [[skills/infrastructure/github-actions-elite]]
- [[knowledgebase/system-design-elite]]
