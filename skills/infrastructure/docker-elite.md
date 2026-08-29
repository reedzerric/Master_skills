---
name: docker-elite
description: 'Container images built small and secure: multi-stage BuildKit builds, distroless and scratch base images, Compose watch for development, and the practices that stop images bloating. Use when an image is too large, when hardening a container, or when rebuilds are slow. For deploying it, use gcloud-deployment-elite or github-actions-elite.'
version: 1.1.0
category: core
triggers: [my docker image is too big, multi stage build, distroless base image, docker build is slow, compose watch, run container as non root, docker layer caching]
dependencies: [github-actions-elite]
inputs: [an application to containerize]
outputs: [a multi-stage Dockerfile, a hardened image]
tags: [infrastructure, devops, docker, security, distroless, buildkit]
links: ['[[github-actions-elite]]', '[[gcloud-deployment-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
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
