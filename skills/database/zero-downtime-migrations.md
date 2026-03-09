---
title: Zero-Downtime Database Schema Migrations (2026)
date: 2026-03-08
task_ref: mit-professor-phase-2
confidence_score: 1.0
tags: [database, postgresql, migrations, expand-contract, ha]
links: ["[[skills/database/postgresql-elite]]"]
---

# Zero-Downtime Database Schema Migrations (2026)

## 🎯 Purpose
Guidelines for executing database schema changes in high-availability systems without locking tables or dropping traffic.

## 🛠️ The Process / Fact

### 1. The Expand-Contract Pattern
Never perform a breaking change in one step. Use this 5-phase workflow:
1.  **Expand:** Add the new column/table/index (must be nullable or have a default).
2.  **Migrate (App):** Deploy code that writes to BOTH old and new locations but reads from the old.
3.  **Backfill:** Run background batch jobs to copy existing data from old to new.
4.  **Switch (App):** Deploy code that reads and writes ONLY to the new location.
5.  **Contract:** Drop the old column/table/triggers.

### 2. PostgreSQL Safety Standards
- **Concurrent Indexes:** ALWAYS use `CREATE INDEX CONCURRENTLY`. Never block writes for an index build.
- **Safe Constraints:** Add constraints as `NOT VALID` first (short lock), then run `VALIDATE CONSTRAINT` later (sequential scan, no write block).
- **Lock Timeouts:** Always set a `lock_timeout` (e.g., 2s) for migration sessions to prevent queuing behind slow queries and causing a cascading outage.

### 3. Renaming & Type Changes
- **Renaming:** Add new column -> Sync via Trigger -> Backfill -> Switch -> Drop old.
- **Type Change (e.g., INT to BIGINT):** Use the Expand-Contract pattern. Type changes usually require a full table rewrite; avoid direct `ALTER`.

## ⚠️ Known Quirks or Edge Cases
- **Replication Lag:** High-write backfills can saturate replication streams. Batch your backfills (e.g., 1000 rows at a time with a sleep).
- **Triggers:** Ensure your sync triggers handle `NULL` values and updates correctly to prevent data drift during the "Migrate" phase.

## 🔗 Related Memories
- [[skills/database/postgresql-elite]]
- [[knowledgebase/system-design-elite]]
