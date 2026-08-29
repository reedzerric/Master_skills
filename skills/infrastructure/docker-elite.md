---
name: docker-elite
description: Guidelines for building high-performance, ultra-secure containerized applications. Use when working with infrastructure, devops, docker.
version: 1.0.0
category: core
triggers: [infrastructure, devops, docker, security, distroless, buildkit]
dependencies: [github-actions-elite]
inputs: [source files, project config]
outputs: [refactored code, review findings]
title: Docker Elite & Container Security (2026)
date: 2026-03-08
task_ref: all-facets-expansion
confidence_score: 1.0
tags: [infrastructure, devops, docker, security, distroless, buildkit]
links: ["[[skills/infrastructure/github-actions-elite]]"]
---

# Docker Elite & Container Security (2026)

## 🎯 Purpose
Guidelines for building high-performance, ultra-secure containerized applications.

## 🛠️ The Process / Fact

### 1. Multi-Stage BuildKit
- **Cache Mounts:** Use `--mount=type=cache` to persist package manager caches (npm, pip, cargo) across builds.
- **Parallelism:** BuildKit executes independent stages in parallel; structure Dockerfiles to build frontend and backend assets concurrently.

### 2. The Security Tier: Distroless & Scratch
- **Production Standard:** Use `gcr.io/distroless/` for runtime images (Node, Python, Java). It contains NO shell or package manager, reducing attack surface by 90%+.
- **Static Binaries:** Use `FROM scratch` for statically compiled Rust or Go binaries (0MB base image).
- **Non-Root:** NEVER run containers as `root`. Use the `nonroot` user provided in Distroless images.

### 3. Modern Development (Compose Watch)
- **Standard:** Use `develop: watch` in `docker-compose.yml` to sync code without full rebuilds.
- **Docker Init:** Use `docker init` to generate standardized scaffolding for new projects.

### 4. Best Practices
- **Secrets:** Use top-level `secrets` in Compose to mount sensitive data to `/run/secrets/`, avoiding environment variable leakage.
- **Version Pinning:** Pin base images to specific versions (e.g., `python:3.13-slim`), not `latest`.

## ⚠️ Known Quirks or Edge Cases
- **Distroless Debugging:** Since there is no shell, use `docker debug` (CLI tool) or `kubectl debug` for troubleshooting.
- **Context:** Large `node_modules` or `.git` folders slow down builds; use `.dockerignore`.

## 🔗 Related Memories
- [[skills/infrastructure/github-actions-elite]]
