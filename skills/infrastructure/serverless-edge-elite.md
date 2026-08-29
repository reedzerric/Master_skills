---
name: serverless-edge-elite
description: 'Serverless and edge compute: choosing between edge and regional runtimes per workload, cold-start mitigation, and event-driven architecture patterns. Use when cold starts hurt latency, when deciding what belongs at the edge, or when designing an event-driven flow. For always-on containers, use docker-elite.'
version: 1.1.0
category: core
triggers: [cold start latency, edge or regional runtime, serverless function timeout, event driven architecture, what belongs at the edge, lambda or workers]
dependencies: [github-actions-elite]
inputs: [a workload and its latency requirements]
outputs: [a runtime placement decision, an event-driven design]
tags: [infrastructure, serverless, edge, wasm, latency, event-driven]
links: ['[[architectural-patterns]]', '[[docker-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
---

# Serverless & Edge Computing Mastery (2026)

## 🎯 Purpose
Guidelines for architecting latency-optimized, event-driven systems using a hybrid Serverless/Edge strategy.

## 🛠️ The Process / Fact

### 1. The Hybrid Runtime Strategy
- **Edge (V8 Isolates / Wasm):** Use for lightweight logic (Auth, SEO, Personalization). 0–5ms cold starts. TTFB focus.
- **Serverless (FaaS):** Use for heavy compute and DB queries. Full runtime support (Python, Node, Rust).

### 2. Cold Start Mitigation
- **Lazy Loading:** Only import dependencies inside the handler for conditional logic.
- **Global State Reuse:** Initialize DB connections and SDK clients OUTSIDE the handler.
- **Wasm 2.0:** Use WebAssembly for high-performance, portable logic across providers (Vercel, Cloudflare, Deno).

### 3. Event-Driven Architecture (EDA)
- **Choreography > Orchestration:** Prefer decentralized services reacting to events to avoid central bottlenecks.
- **Task Isolation:** Break workflows into small, single-responsibility functions for better scaling and retries.

## ⚠️ Known Quirks or Edge Cases
- **CPU Limits:** Edge functions have strict CPU time limits (e.g., 30–50ms). Heavy logic belongs in FaaS.
- **Observability:** Distributed tracing is mandatory for debugging across ephemeral boundaries.

## 🔗 Related Memories
- [[skills/infrastructure/github-actions-elite]]
- [[knowledgebase/architectural-patterns]]
