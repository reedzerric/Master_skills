---
name: github-actions-elite
description: 'CI/CD on GitHub Actions: OIDC for zero-secret cloud deployment, caching that actually hits, and matrix and monorepo scaling patterns. Use when a workflow is slow, when removing long-lived cloud credentials from repository secrets, or when scaling CI across a monorepo. For the git workflow around it, use git-ops-elite.'
version: 1.1.0
category: core
triggers: [my ci is slow, oidc instead of stored secrets, github actions cache miss, matrix build, monorepo ci, deploy from actions without keys, workflow permissions]
dependencies: [docker-elite]
inputs: [a repository and its build and deploy needs]
outputs: [a workflow file, an OIDC trust configuration]
tags: [infrastructure, devops, ci, cd, github-actions, security]
links: ['[[git-ops-elite]]', '[[docker-elite]]', '[[iac-opentofu-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
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
