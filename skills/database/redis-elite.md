---
title: Redis High-Performance Caching (2026)
date: 2026-03-08
task_ref: all-facets-expansion
confidence_score: 1.0
tags: [database, redis, caching, pub-sub, performance]
links: ["[[skills/database/postgresql-elite]]"]
---

# Redis High-Performance Caching (2026)

## 🎯 Purpose
Guidelines for architecting high-performance caching, rate-limiting, and messaging using Redis.

## 🛠️ The Process / Fact

### 1. Data Structure Strategy
- **Hashes (HSET/HGET):** Use instead of large JSON strings for objects with multiple fields. Allows for field-level updates without full re-serialization.
- **Sorted Sets (ZSET):** Ideal for real-time leaderboards, rate-limiting (sliding window), and task scheduling.
- **Streams (XADD):** Standard for high-throughput messaging and event logging with consumer group support.

### 2. Caching & TTL Strategies
- **TTL Mastery:** Always set a TTL (Time-To-Live) for cached data. Use **Jitter** (adding a small random offset) to prevent "Thundering Herd" cache stampedes where all keys expire at once.
- **Write-Through/Write-Behind:** Decide on the persistence strategy. Write-behind (async DB updates) is fastest but risks data loss on Redis failure.

### 3. Concurrency & Logic
- **Lua Scripting (EVAL):** For atomic multi-key operations (e.g., decrementing balance + logging transaction).
- **Pub/Sub:** Real-time event broadcasting to multiple subscribers.

## ⚠️ Known Quirks or Edge Cases
- **Memory Management:** Monitor `maxmemory` and eviction policies (`allkeys-lru` is common).
- **Blocking Operations:** Avoid `KEYS *` in production; use `SCAN` to prevent blocking the single-threaded Redis core.

## 🔗 Related Memories
- [[skills/database/postgresql-elite]]
