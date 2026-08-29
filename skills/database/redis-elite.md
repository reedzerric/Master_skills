---
name: redis-elite
description: 'Redis for caching and coordination: picking the data structure that matches the access pattern, TTL strategies with jitter so keys do not expire together, and concurrency patterns for locks and atomic updates. Use when cache misses spike simultaneously, when choosing between a hash, sorted set or stream, or when implementing a distributed lock. For durable storage, use postgresql-elite.'
version: 1.1.0
category: core
triggers: [cache stampede, redis ttl strategy, which redis data structure, distributed lock in redis, sorted set leaderboard, redis stream or list, thundering herd]
dependencies: [postgresql-elite]
inputs: [an access pattern, a caching or coordination requirement]
outputs: [a data-structure choice, a TTL and eviction policy, a lock implementation]
tags: [database, redis, caching, pub-sub, performance]
links: ['[[postgresql-elite]]', '[[observability-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
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
