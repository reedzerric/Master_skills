---
name: bigquery-elite
description: 'BigQuery cost-first engineering: partitioning and clustering as the primary lever, SQL patterns that avoid full table scans, and governance controls that cap spend before it happens. Use when a query costs too much or runs too long, when designing table layout, or when setting up cost guardrails. For transactional Postgres work, use postgresql-elite.'
version: 1.1.0
category: core
triggers: [my bigquery query is expensive, partition and cluster a table, bigquery scanned too much data, reduce query cost, bigquery slot usage, set a query cost limit]
dependencies: [python-elite]
inputs: [a query or table schema, a cost target]
outputs: [a partitioning and clustering plan, an optimized query, cost guardrails]
tags: [database, bigquery, sql, optimization, cost]
links: ['[[finops-value-elite]]', '[[postgresql-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
---

# BigQuery Data Engineering Mastery (2026)

## 🎯 Purpose
Guidelines for architecting and querying BigQuery with a "Cost-First" approach.

## 🛠️ The Process / Fact

### 1. Partitioning & Clustering (The Golden Rule)
- **Partitioning:** (Coarse Pruning) Divide tables by `DATE`, `TIMESTAMP`, or `INTEGER RANGE`. Aim for 1GB per partition.
- **Clustering:** (Fine Pruning) Sort data within partitions by up to 4 columns. Order of columns matters.
- **Enforcement:** Use `require_partition_filter = TRUE` on large tables.

### 2. SQL Optimization Patterns
- **Ditch `SELECT *`:** Only name columns required (BigQuery is columnar).
- **Early Filter:** Apply `WHERE` clauses BEFORE joins.
- **`QUALIFY` for De-duplication:** Use `ROW_NUMBER() OVER(...) QUALIFY row_num = 1`.
- **`INT64` Joins:** Joining on integers is significantly cheaper and faster than string joins.
- **Avoid Cross-Joins:** Use window functions or `ARRAY`/`STRUCT` instead.

### 3. Cost Control & Governance
- **Dry Run:** Always dry-run queries via the CLI/Console to check expected billing before executing.
- **Materialized Views:** Use for heavy, repetitive aggregations.
- **Capacity Pricing:** Move to Capacity-Based (Slots) with Autoscaling for predictable enterprise workloads.

## ⚠️ Known Quirks or Edge Cases
- **Legacy SQL Sunset:** 2026 is the deadline. Use GoogleSQL (Standard) for all new projects.
- **Storage Billing:** Evaluate Physical vs. Logical storage. Highly compressed data is cheaper on physical billing.

## 🔗 Related Memories
- [[skills/backend/python-elite]]
