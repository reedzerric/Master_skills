---
name: github-actions-elite
description: Guidelines for architecting high-performance, zero-secret CI/CD pipelines. Use when working with infrastructure, devops, ci.
version: 1.0.0
category: core
triggers: [infrastructure, devops, ci, cd, github-actions, security, github, actions]
dependencies: [docker-elite]
inputs: [source files, project config]
outputs: [refactored code, review findings]
title: GitHub Actions Elite CI/CD (2026)
date: 2026-03-08
task_ref: all-facets-expansion
confidence_score: 1.0
tags: [infrastructure, devops, ci, cd, github-actions, security]
links: ["[[skills/infrastructure/docker-elite]]"]
---

# GitHub Actions Elite CI/CD (2026)

## 🎯 Purpose
Guidelines for architecting high-performance, zero-secret CI/CD pipelines.

## 🛠️ The Process / Fact

### 1. OIDC Zero-Secret Deployment
- **Standard:** Use OpenID Connect (OIDC) for all cloud providers (AWS, GCP, Azure).
- **Security:** Never store long-lived secrets (e.g., `AWS_SECRET_KEY`).
- **Permissions:** Explicitly set `id-token: write` and `contents: read` at the job level.

### 2. Performance-First Caching
- **Native Setup Actions:** Always use the built-in cache features (e.g., `actions/setup-node`, `actions/setup-python`).
- **Docker Layer Caching:** Use `type=gha` with `docker/build-push-action`. This uses GitHub's fast internal cache backend.
- **Cache Keys:** Include the runner OS and lockfile hash: `v1-${{ runner.os }}-${{ hashFiles('uv.lock') }}`.

### 3. Matrix & Monorepo Scaling
- **Dynamic Matrices:** Use a previous job to generate a JSON list of targets (sharding) for monorepos.
- **Fail-Fast:** Set `fail-fast: true` for PRs to save costs; `fail-fast: false` on `main` to ensure full reports.
- **Concurrency Groups:** Use `concurrency` with `cancel-in-progress: true` to auto-kill outdated PR runs.

## ⚠️ Known Quirks or Edge Cases
- **10GB Limit:** GitHub has a per-repo cache limit. Monitor usage to avoid eviction of critical layers.
- **SHA Pinning:** For high-security environments, pin third-party actions to their **full commit SHA**, not just the version tag.

## 🔗 Related Memories
- [[skills/infrastructure/docker-elite]]
