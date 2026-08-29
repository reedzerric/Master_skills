---
name: rust-elite
description: 'Rust systems practice: async patterns on Tokio for 1.75 and later, the error-handling trio of thiserror, anyhow and Result, and the concurrency rules that keep the borrow checker on your side. Use when writing async Rust, designing error types across a library and binary boundary, or sharing state between tasks. For Python instead, use python-elite.'
version: 1.1.0
category: core
triggers: [async rust with tokio, thiserror or anyhow, rust error type design, share state between tasks, arc and mutex in rust, fighting the borrow checker, spawn a tokio task]
dependencies: [python-elite]
inputs: [a Rust crate or async workload]
outputs: [async Rust code, an error type hierarchy]
tags: [backend, rust, async, tokio, error-handling]
links: ['[[python-elite]]', '[[postgresql-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
---

# Rust Systems Mastery (2026)

## 🎯 Purpose
Guidelines for writing efficient, safe, and idiomatic Rust code with a focus on modern async patterns.

## 🛠️ The Process / Fact

### 1. Modern Async Patterns (Rust 1.75+)
- **Native Async Traits:** No longer use `#[async_trait]`. Define async methods directly in traits.
- **Send Bounds:** For multi-threaded executors (e.g., Tokio), ensure futures are `Send` using trait variants or RTN (Return Type Notation).

### 2. The Error Handling "Trio"
| Tool | Context | Use Case |
| :--- | :--- | :--- |
| **`thiserror`** | **Internal Modules** | Strong enum types for library-style error matching. |
| **`anyhow`** | **Applications (Binaries)** | Opaque error reporting with easy context (`.context("...")`). |
| **`miette`** | **CLI Tools** | User-facing errors with color and helpful snippets. |

### 3. Concurrency & Safety
- **Tokio 1.x:** The industry standard executor.
- **`tokio::select!`:** The primary tool for managing concurrent branches and ensuring cooperative cancellation.
- **Avoid Blocking:** NEVER block the runtime with CPU-heavy tasks. Use `tokio::task::spawn_blocking`.
- **Tracing:** Use the `tracing` crate instead of simple `log` for async spans and request lifecycle tracking.

## ⚠️ Known Quirks or Edge Cases
- **Async Drop:** Rust lacks native `AsyncDrop`. Use explicit `shutdown()` methods for cleanup tasks.
- **Seeded Randomness:** In production, use `rand` with specific RNG seeds for reproducible logic in simulations or tests.

## 🔗 Related Memories
- [[skills/backend/python-elite]]
