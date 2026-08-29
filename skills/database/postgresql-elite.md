---
name: postgresql-elite
description: Guidelines for architecting high-concurrency, performant relational databases using PostgreSQL 18+ features. Use when working with database, postgresql, indexing.
version: 1.0.0
category: core
triggers: [database, postgresql, indexing, jsonb, performance]
dependencies: [rust-elite]
inputs: [source files, project config]
outputs: [refactored code, review findings]
title: PostgreSQL Elite Storage & Indexing (2026)
date: 2026-03-08
task_ref: all-facets-expansion
confidence_score: 1.0
tags: [database, postgresql, indexing, jsonb, performance]
links: ["[[skills/backend/rust-elite]]"]
---

# PostgreSQL Elite Storage & Indexing (2026)

## 🎯 Purpose
Guidelines for architecting high-concurrency, performant relational databases using PostgreSQL 18+ features.

## 🛠️ The Process / Fact

### 1. Modern Architecture (PG 18)
- **Asynchronous I/O (AIO):** Leverage PG18's AIO subsystem for concurrent read requests, reducing I/O bottlenecks.
- **UUIDv7:** Standardize on `uuidv7()` for primary keys. It is time-ordered, leading to superior B-tree locality and fewer page splits compared to random UUIDv4.

### 2. Advanced JSONB Performance
- **GIN (`jsonb_path_ops`):** For containment queries (`@>`), use `jsonb_path_ops` over default `jsonb_ops`. It is typically **30-50% smaller** and faster.
- **Virtual Generated Columns:** Use virtual columns to extract specific keys from JSONB on-the-fly for fast B-tree lookups without disk bloat.
- **JSON_TABLE:** Project JSONB data into a relational table format for complex extraction logic.

### 3. Smart Indexing
- **Avoid "The GIN Trap":** Do not GIN index every JSONB column. Use **Partial Indexes** to only index rows frequently queried.
- **Index Skip Scan:** Utilize composite indexes `(tenant_id, status)` even if the first column is not in the `WHERE` clause.

## ⚠️ Known Quirks or Edge Cases
- **Normalization Rule:** If a key is joined or filtered in 90% of queries, **promote it to a typed column**. JSONB is for cold or polymorphic data.
- **GIN Bloat:** GIN indexes are expensive to update; avoid on write-heavy tables without partial filtering.

## 🔗 Related Memories
- [[skills/backend/rust-elite]]
- [[skills/database/bigquery-elite]]
