---
name: architectural-patterns
description: Guidelines for architecting large-scale enterprise systems using Domain-Driven Design (DDD) and Hexagonal principles. Use when working with knowledge, architecture, ddd.
version: 1.0.0
category: core
triggers: [knowledge, architecture, ddd, hexagonal, micro-frontends, architectural, patterns]
dependencies: [serverless-edge-elite]
inputs: [source files, project config]
outputs: [refactored code, review findings]
title: Modern Architectural Patterns (2026)
date: 2026-03-08
task_ref: all-facets-expansion
confidence_score: 1.0
tags: [knowledge, architecture, ddd, hexagonal, micro-frontends]
links: ["[[skills/infrastructure/serverless-edge-elite]]"]
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
