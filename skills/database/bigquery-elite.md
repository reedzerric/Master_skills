---
name: bigquery-elite
description: Guidelines for architecting and querying BigQuery with a "Cost-First" approach. Use when working with database, bigquery, sql.
version: 1.0.0
category: core
triggers: [database, bigquery, sql, optimization, cost]
dependencies: [python-elite]
inputs: [source files, project config]
outputs: [refactored code, review findings]
title: BigQuery Data Engineering Mastery (2026)
date: 2026-03-08
task_ref: tech-expansion
confidence_score: 1.0
tags: [database, bigquery, sql, optimization, cost]
links: ["[[skills/backend/python-elite]]"]
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
