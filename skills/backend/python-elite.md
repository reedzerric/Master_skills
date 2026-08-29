---
name: python-elite
description: 'Python standards on the Astral toolchain: uv for environments and dependency resolution, ruff for lint and format, advanced typing for 3.13 and later, and the idiomatic patterns expected of code in this repository. Use when starting a Python project, adding or locking dependencies, or deciding how to type something. For test structure, use pytest-elite.'
version: 1.1.0
category: core
triggers: [start a python project, uv instead of pip, ruff configuration, type hints for python 3.13, generics and protocols, pyproject setup, lock dependencies]
dependencies: [flask-elite]
inputs: [a Python project or module]
outputs: [a pyproject and uv setup, typed idiomatic Python]
tags: [backend, python, astral, uv, ruff, typing]
links: ['[[pytest-elite]]', '[[flask-elite]]', '[[django-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
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
