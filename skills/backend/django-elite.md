---
name: django-elite
description: 'Django standards: uv-based project tooling, PostgreSQL 18 integration, modern middleware and ASGI serving, and the testing setup. Use when starting or maintaining a Django project, wiring the database, or configuring middleware and static serving. For auth hardening, use django-auth-hardening; for schema changes against a live table, use zero-downtime-migrations.'
version: 1.1.0
category: core
triggers: [start a django project, django settings layout, django with postgres, django asgi deployment, django middleware order, django test setup]
dependencies: [python-elite, zero-downtime-migrations]
inputs: [a Django project or requirement]
outputs: [project scaffolding, settings and middleware configuration]
tags: [backend, django, python, elite, patterns]
links: ['[[python-elite]]', '[[postgresql-elite]]', '[[django-auth-hardening]]', '[[zero-downtime-migrations]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
---

# Django Elite Backend Standards (2026)

## 🎯 Purpose
Guidelines for architecting scalable, maintainable, and high-performance Django applications using modern Python tooling and database patterns.

## 🛠️ The Process / Fact

### 1. Project Tooling
- **Package Management:** Use `uv` with `pyproject.toml` for deterministic builds.
- **Linting:** Use `ruff` for ultra-fast linting and formatting.
- **Configuration:** Use `python-dotenv` and `dj-database-url` for dynamic, environment-based settings.

### 2. Database Integration (PostgreSQL 18)
- **Primary Keys:** Transition to **UUIDv7** for time-ordered, distributed-safe identifiers.
- **Zero-Downtime:** Follow the **Expand-Contract** pattern for all migrations.
- **Connection Pooling:** Use `conn_max_age` and `conn_health_checks` in `DATABASES` settings for persistent, healthy connections.

### 3. Modern Middleware & Serving
- **WhiteNoise:** Standard for efficient static file serving in containerized environments.
- **Middleware Order:** Ensure `SecurityMiddleware` and `WhiteNoiseMiddleware` are at the top of the stack.

### 4. Testing & Validation
- **Pytest:** Use `pytest-django` with modular fixtures in `conftest.py`.
- **Isolation:** Use `pytest-mock` to isolate external service integrations (e.g., Shopify, Firebase).

## ⚠️ Known Quirks or Edge Cases
- **BOM Issues:** When creating `.ini` or `.toml` files via automation, ensure no UTF-8 BOM is present to avoid tool parsing errors.
- **Standard Library:** Verify the environment's Python build contains all standard libraries (e.g., `xml.dom.minidom`) required by Django's test runner.

## 🔗 Related Memories
- [[skills/backend/python-elite]]
- [[skills/database/zero-downtime-migrations]]
- [[testing/pytest-elite]]
