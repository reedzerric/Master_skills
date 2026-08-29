---
name: postgresql-elite
description: 'PostgreSQL 18 practice: the async I/O architecture and UUIDv7 keys, JSONB performance patterns, and index selection driven by the query shapes actually run. Use when a query is slow, when choosing a primary key type, when deciding between JSONB and real columns, or when picking an index. For schema changes against a live table, use zero-downtime-migrations.'
version: 1.1.0
category: core
triggers: [my postgres query is slow, which index should i add, uuid or bigint primary key, jsonb or separate columns, gin index, postgres 18 features, reading explain analyze]
dependencies: [rust-elite]
inputs: [a schema, a slow query or EXPLAIN output]
outputs: [an index plan, a schema design, a rewritten query]
tags: [database, postgresql, indexing, jsonb, performance]
links: ['[[zero-downtime-migrations]]', '[[redis-elite]]', '[[rust-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
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
