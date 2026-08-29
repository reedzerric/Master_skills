---
name: git-ops-elite
description: 'Source control standards: Conventional Commits in `type(scope): description` form, rebase-first for feature branches and never for main, mandatory pre-commit hooks (ruff, pyright or tsc, secret-scan), and trunk-based branching behind protected environments. Use when writing a commit message, setting up hooks, or deciding between rebase and merge. For PR sizing, stacking and merge queues, use git-velocity-elite.'
version: 1.1.0
category: core
triggers: [write a commit message, conventional commits format, rebase or merge this branch, set up pre-commit hooks, force push safely, stop secrets reaching the repo, git lfs for large files]
dependencies: [github-actions-elite]
inputs: [a change to commit, a repository to configure]
outputs: [a conventional commit message, a pre-commit config, a branching policy]
tags: [misc, git, gitops, workflow, automation]
links: ['[[github-actions-elite]]', '[[git-velocity-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch2
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
