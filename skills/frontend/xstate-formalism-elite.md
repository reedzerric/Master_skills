---
title: XState & Actor Model Formalism (2026)
date: 2026-03-08
task_ref: mit-professor-phase-4
confidence_score: 1.0
tags: [frontend, xstate, state-machine, actor-model, formalism]
links: ["[[skills/frontend/js-html-elite]]"]
---

# XState & Actor Model Formalism (2026)

## 🎯 Purpose
Guidelines for managing complex frontend logic using deterministic state machines and the Actor Model (XState v5+).

## 🛠️ The Process / Fact

### 1. The Actor-First Architecture
- **Isolation:** Treat every logical unit (API service, WebSocket, complex UI component) as an **Actor**. Do not put everything in one giant machine.
- **Communication:** Actors communicate via `sendParent` or by referencing the global `system`. Avoid direct state manipulation of child actors.

### 2. Type-Safe State Management
- **The `setup()` Function:** Always use `setup()` to define types, actions, and actors *before* `createMachine()`.
- **Closed to Types:** This ensures the machine is strictly typed at compile time while remaining open for implementation details.

### 3. Model-Based Testing (MBT)
- **`@xstate/test`:** Do not write manual user flows. Define "States" in your machine and let XState automatically generate the paths (tests) to reach them.
- **Verification:** Attach a `meta: { test: (page) => ... }` property to every state to verify the UI correctly reflects the mathematical state.

## ⚠️ Known Quirks or Edge Cases
- **Over-engineering:** Do not use full Statecharts for simple toggles or synchronous inputs. Use `@xstate/store` for simple state that doesn't require transitions or guards.
- **Side Effects:** Keep transition logic pure. Use `fromPromise` or `fromObservable` for side effects (API calls) and invoke them as external actors.

## 🔗 Related Memories
- [[skills/frontend/js-html-elite]]
- [[testing/webapp-testing]]
