---
title: GitOps Elite Workflow (2026)
date: 2026-03-08
task_ref: all-facets-expansion
confidence_score: 1.0
tags: [misc, git, gitops, workflow, automation]
links: ["[[skills/infrastructure/github-actions-elite]]"]
---

# GitOps Elite Workflow (2026)

## 🎯 Purpose
Guidelines for efficient, automated, and secure source control management.

## 🛠️ The Process / Fact

### 1. Semantic Commits (Conventional Commits)
- **Standard:** Use the `type(scope): description` format.
- **Types:** `feat` (new feature), `fix` (bug fix), `docs` (documentation), `style` (formatting), `refactor` (logic change, no feature), `test` (tests), `chore` (maintenance).
- **Example:** `feat(auth): add OIDC provider support`.

### 2. Rebase-First Workflow
- **Strategy:** Prefer `git rebase` over `git merge` for feature branches to keep a clean, linear history.
- **Rules:** Never rebase `main` or `production`. Only rebase local/feature branches.

### 3. Pre-Commit Hooks
- **Standard:** Use `pre-commit` framework.
- **MANDATORY Hooks:** `ruff`, `pyright` (or `tsc`), `secret-scan` (prevent credential leaks).

### 4. Branching Strategy
- **Trunk-Based Development:** Prefer short-lived feature branches (<2 days).
- **GitHub Environments:** Use protected branches and environment-specific reviewers for production deployments.

## ⚠️ Known Quirks or Edge Cases
- **Force-Push:** Only use `git push --force-with-lease` after rebasing feature branches.
- **Large Files:** Use `Git LFS` for assets >50MB to prevent repository bloat.

## 🔗 Related Memories
- [[skills/infrastructure/github-actions-elite]]
