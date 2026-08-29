---
name: iac-opentofu-elite
description: 'Infrastructure-as-code governance with OpenTofu: remote state and locking, the GitOps pipeline from plan to apply, and drift detection between declared and actual infrastructure. Use when state is locked or corrupted, when infrastructure has drifted from code, or when setting up plan-and-apply review. For the CI that runs it, use github-actions-elite.'
version: 1.1.0
category: core
triggers: [terraform state is locked, opentofu drift, infrastructure changed outside of code, plan and apply pipeline, remote state backend, import an existing resource]
dependencies: [github-actions-elite]
inputs: [infrastructure definitions and current cloud state]
outputs: [state configuration, a GitOps pipeline, a drift report]
tags: [infrastructure, devops, iac, opentofu, terraform, governance]
links: ['[[github-actions-elite]]', '[[observability-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
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
