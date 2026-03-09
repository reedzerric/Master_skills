---
title: Python Elite Standards (2026)
date: 2026-03-08
task_ref: tech-expansion
confidence_score: 1.0
tags: [backend, python, astral, uv, ruff, typing]
links: ["[[skills/backend/flask-elite]]"]
---

# Python Elite Standards (2026)

## 🎯 Purpose
Guidelines for writing high-performance, type-safe, and maintainable Python code using the 2026 Astral toolchain (`uv`, `ruff`) and advanced type hinting.

## 🛠️ The Process / Fact

### 1. Tooling (Astral Ecosystem)
- **Project/Package Management:** Use `uv`.
  - `uv init`: Initialize a project.
  - `uv add <package>`: Add dependencies (updates `pyproject.toml` and `uv.lock`).
  - `uv run <script.py>`: Run scripts in an auto-managed virtual environment.
- **Linting & Formatting:** Use `ruff`.
  - `ruff check --fix`: Linting and auto-fixing.
  - `ruff format`: Code formatting (replaces Black).
  - Configure via `[tool.ruff]` in `pyproject.toml`.

### 2. Advanced Typing (Python 3.13+)
- **Type Narrowing:** Use `TypeIs` (PEP 742) for more intuitive narrowing in conditional branches.
- **ReadOnly:** Use `ReadOnly[]` (PEP 705) in `TypedDict` for immutable keys.
- **Defaults:** Use defaults for `TypeVar` (e.g., `class Box[T = int]: ...`).
- **Union Syntax:** Always use the pipe operator `int | str` instead of `Union[int, str]`.
- **Generics:** Use lower-case built-ins (e.g., `list[int]`).

### 3. Idiomatic Patterns
- **Template Strings (t-strings):** In 3.14+, use `t"..."` for safer SQL and HTML generation.
- **Configuration:** Use `dataclasses` or Pydantic models for application settings, never raw dictionaries.
- **Dependency Management:** Always commit `uv.lock` for deterministic builds.

## ⚠️ Known Quirks or Edge Cases
- **Python Versioning:** `uv` can manage Python interpreters. Use `uv python install 3.14` to avoid `pyenv`.
- **Lazy Evaluation:** In 3.14+, annotations are evaluated lazily by default; `from __future__ import annotations` is no longer required.

## 🔗 Related Memories
- [[skills/backend/flask-elite]]
