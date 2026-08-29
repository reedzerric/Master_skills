---
name: architectural-patterns
description: Domain-Driven Design bounded contexts and ubiquitous language, Hexagonal ports-and-adapters for keeping business logic framework-free, and micro-frontend federation split by business domain. Use when deciding where a service or module boundary goes, isolating a domain core from its framework, or splitting a frontend by domain rather than technical layer. For availability and consistency trade-offs, use system-design-elite.
version: 1.1.0
category: core
triggers: [where should the service boundary go, bounded context, ports and adapters, hexagonal architecture, isolate business logic from the framework, split the frontend by domain, micro frontend federation]
dependencies: [serverless-edge-elite]
inputs: [a system or module to structure]
outputs: [bounded-context boundaries, a ports-and-adapters layout]
tags: [knowledge, architecture, ddd, hexagonal, micro-frontends]
links: ['[[serverless-edge-elite]]', '[[system-design-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-kb
---

# Modern Architectural Patterns (2026)

## 🎯 Purpose
Guidelines for architecting large-scale enterprise systems using Domain-Driven Design (DDD) and Hexagonal principles.

## 🛠️ The Process / Fact

### 1. Domain-Driven Design (DDD)
- **Bounded Contexts:** Each micro-service or micro-frontend must be defined by a single Bounded Context (e.g., "Checkout," "Inventory").
- **Ubiquitous Language:** The code and API contracts must use the same business terminology defined by domain experts.

### 2. Hexagonal Architecture (Ports & Adapters)
- **Domain Core:** Isolate business logic in a pure JS/TS/Python core without framework dependencies.
- **Ports (Interfaces):** The core defines what it needs (e.g., `UserRepository`).
- **Adapters (Implementations):** 
  - **Driving:** UI (React/Vue).
  - **Driven:** Infrastructure (FetchAPI, LocalStorage).

### 3. Micro-Frontend (MFE) Federation
- **Native Federation:** Use browser-native standards (ES Modules, Import Maps) for dynamic loading without heavy build tools.
- **Domain Ownership:** MFEs are split by business domain, not technical layer.

## ⚠️ Known Quirks or Edge Cases
- **MFE Tax:** Do not start with Micro-Frontends. Start with a "Modular Monolith" and split only when team scale demands it (50+ engineers).
- **EventStorming:** Use EventStorming workshops to identify "natural seams" before splitting services.

## 🔗 Related Memories
- [[skills/infrastructure/serverless-edge-elite]]
