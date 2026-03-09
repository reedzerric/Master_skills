---
title: Git Velocity & Trunk-Based Development (2026)
date: 2026-03-08
task_ref: velocity-expansion
confidence_score: 1.0
tags: [misc, git, velocity, trunk-based, stacked-prs, graphite]
links: ["[[misc/git-ops-elite]]"]
---

# Git Velocity & Trunk-Based Development (2026)

## 🎯 Purpose
Guidelines for maximizing engineering velocity and minimizing integration pain using 2026 version control standards.

## 🛠️ The Process / Fact

### 1. Trunk-Based Development (The Gold Standard)
- **Standard:** All developers merge small, frequent updates directly to the `main` trunk.
- **Branch Lifespan:** Branches MUST NOT live longer than 24 hours.
- **Feature Flags:** Use toggles to merge incomplete features without exposing them to users. This decouples **deployment** from **release**.

### 2. Stacked Pull Requests (Stacked PRs)
- **Concept:** Break large features into a "stack" of dependent, 50-100 line PRs.
- **Workflow:** 
  - PR A (Foundation) -> PR B (Logic) -> PR C (UI).
  - Reviewers approve small chunks quickly while you continue working on the next layer.
- **Tooling:** Use **Graphite** or `ghstack` to manage the stack and automate rebasing.

### 3. Squash-and-Merge Linear History
- **Strategy:** Use "Squash and Merge" for all PRs to keep the trunk history linear and readable.
- **Merge Queues:** Use an automated merge queue (e.g., GitHub Merge Queue) to coordinate landings and prevent "broken trunk" scenarios.

## ⚠️ Known Quirks or Edge Cases
- **GitFlow is Legacy:** Avoid `develop` or long-lived `release` branches. They create "inventory tax" and slow down the CI/CD pipeline.
- **Small PR Discipline:** Aim for PRs < 200 lines. Smaller PRs have 40% faster cycle times and catch more bugs.

## 🔗 Related Memories
- [[misc/git-ops-elite]]
- [[skills/infrastructure/github-actions-elite]]
