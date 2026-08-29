---
name: git-velocity-elite
description: 'Shipping faster through trunk-based development: branches that live under 24 hours, feature flags decoupling deployment from release, stacked PRs of 50 to 100 lines managed with Graphite or ghstack, squash-merge for linear history, and merge queues to keep the trunk green. Use when a PR is too big to review, when changes sit in review for days, or when long-lived branches are causing merge pain. For commit format and hooks, use git-ops-elite.'
version: 1.1.0
category: core
triggers: [my pr is too big to review, stacked pull requests, graphite or ghstack, trunk based development, feature flags for incomplete work, prs sit in review too long, merge queue, long lived branch merge pain]
dependencies: [git-ops-elite]
inputs: [a large change to split, a team's current branching habits]
outputs: [a PR stack plan, a trunk-based branching policy]
tags: [misc, git, velocity, trunk-based, stacked-prs, graphite]
links: ['[[git-ops-elite]]', '[[github-actions-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch2
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
