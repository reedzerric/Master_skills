---
name: iac-opentofu-elite
description: Guidelines for managing cloud infrastructure deterministically using OpenTofu/Terraform with strict state and drift governance. Use when working with infrastructure, devops, iac.
version: 1.0.0
category: core
triggers: [infrastructure, devops, iac, opentofu, terraform, governance]
dependencies: [github-actions-elite]
inputs: [source files, project config]
outputs: [refactored code, review findings]
title: Infrastructure as Code (IaC) Governance (2026)
date: 2026-03-08
task_ref: mit-professor-critique
confidence_score: 1.0
tags: [infrastructure, devops, iac, opentofu, terraform, governance]
links: ["[[skills/infrastructure/github-actions-elite]]"]
---

# Infrastructure as Code (IaC) Governance (2026)

## 🎯 Purpose
Guidelines for managing cloud infrastructure deterministically using OpenTofu/Terraform with strict state and drift governance.

## 🛠️ The Process / Fact

### 1. State Management & Locking
- **Remote State:** Never store `.tfstate` locally. Always use a secure remote backend (e.g., AWS S3 + DynamoDB for locking, or Terraform Cloud/HCP).
- **State Isolation:** Isolate state files by environment (`dev`, `staging`, `prod`) and by domain (e.g., `network.tfstate`, `database.tfstate`) to reduce the blast radius of a corrupted state.

### 2. The GitOps Pipeline
- **Plan in PR:** A pull request must automatically trigger a `tofu plan`. The output MUST be posted as a comment on the PR for human review.
- **Apply on Merge:** `tofu apply` is ONLY executed automatically when the PR is merged into the default branch. Humans never run `apply` from their laptops.
- **Policy as Code:** Use tools like `checkov` or `OPA` (Open Policy Agent) in the CI pipeline to block any plan that violates security rules (e.g., "S3 buckets must not be public").

### 3. Drift Detection
- **Continuous Reconciliation:** Run a scheduled `tofu plan` every 24 hours to detect "Configuration Drift" (changes made manually in the cloud console).
- **Alerting:** If drift is detected, automatically alert the SRE team. Manual changes must be backported into IaC or immediately reverted.

## ⚠️ Known Quirks or Edge Cases
- **Secret Management:** Never hardcode secrets in `.tf` files. Pass them at runtime via OIDC integrations or fetch them dynamically from a Secret Manager using data blocks.
- **Provider Pinning:** Always pin provider versions using the pessimistic constraint operator (e.g., `~> 5.0`) to avoid breaking changes during automated runs.

## 🔗 Related Memories
- [[skills/infrastructure/github-actions-elite]]
- [[knowledgebase/security-agentic-elite]]
