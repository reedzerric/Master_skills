---
name: pytest-elite
description: 'pytest standards: yield fixtures for teardown, explicit fixture injection over autouse, the mocker fixture from pytest-mock patched where an object is used rather than where it is defined, parametrization for edge cases, narrowest scope by default, and xdist for parallelism. Use when writing or fixing Python tests, when a mock does not take effect, or when the suite is slow or flaky. For browser-level testing, use webapp-testing.'
version: 1.1.0
category: core
triggers: [write pytest tests, my mock is not working, patch where it is used, pytest fixture teardown, parametrize a test, my test suite is slow, flaky test, mock an async function]
dependencies: [python-elite]
inputs: [Python code under test]
outputs: [pytest fixtures, mocks patched at the right site, parametrized test cases]
tags: [testing, python, pytest, mocking, fixtures]
links: ['[[python-elite]]', '[[webapp-testing]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch2
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
