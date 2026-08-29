---
name: pytest-elite
description: Guidelines for writing modular, fast, and high-coverage Python tests using `pytest` and modern dependency injection. Use when working with testing, python, pytest.
version: 1.0.0
category: core
triggers: [testing, python, pytest, mocking, fixtures]
dependencies: [python-elite]
inputs: [source files, project config]
outputs: [refactored code, review findings]
title: Pytest Elite Testing Standards (2026)
date: 2026-03-08
task_ref: all-facets-expansion
confidence_score: 1.0
tags: [testing, python, pytest, mocking, fixtures]
links: ["[[skills/backend/python-elite]]"]
---

# Pytest Elite Testing Standards (2026)

## 🎯 Purpose
Guidelines for writing modular, fast, and high-coverage Python tests using `pytest` and modern dependency injection.

## 🛠️ The Process / Fact

### 1. Modern Fixtures (Dependency Injection)
- **Prefer `yield`:** Always use `yield` for teardown. Code before `yield` is setup; code after is cleanup.
- **Explicit Requests:** Avoid `autouse=True`. Explicitly pass fixtures as arguments to make test dependencies clear.
- **Composition:** Inject simpler fixtures into complex ones (e.g., `db_connection` into `populated_db`).

### 2. Mocking with `pytest-mock`
- **Standard:** Use the `mocker` fixture instead of `unittest.mock`. It handles teardown automatically.
- **Patching Strategy:** Patch where the object is **used**, not defined (e.g., `mocker.patch("app.module.os.path.exists")`).
- **Async Mocks:** Use `AsyncMock` for mocking `awaitable` functions in 3.10+.

### 3. Advanced Patterns
- **Parametrization:** Use `@pytest.mark.parametrize` to run logic against multiple datasets to handle edge cases efficiently.
- **Scope Control:** Use the narrowest scope (`function`) by default. Use `session` ONLY for expensive resources (DB/Browser).
- **Parallelism:** Run tests in parallel using `pytest-xdist` to reduce CI time.

## ⚠️ Known Quirks or Edge Cases
- **Mock Leakage:** Standard `patch` can leak if not stopped. The `mocker` fixture prevents this.
- **Flaky Session Fixtures:** Be careful with `session` scoped fixtures; data changes in one test can pollute others.

## 🔗 Related Memories
- [[skills/backend/python-elite]]
- [[testing/webapp-testing]]
