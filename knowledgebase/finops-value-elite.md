---
name: finops-value-elite
description: 'Cloud cost treated as an architectural requirement: the FOCUS billing standard for multi-cloud normalisation, unit economics such as cost per API call and cost per active user, GPU and vector-database spend control, and policy-as-code guardrails against waste. Use when a cloud bill needs explaining or cutting, or when cost per unit has to be designed in rather than measured after. For query-level SQL cost, use bigquery-elite.'
version: 1.1.0
category: core
triggers: [our cloud bill is too high, cost per active user, reduce gpu spend, unit economics for infrastructure, forecast cloud spend, stop idle dev environments, focus billing standard, spot instances for training]
dependencies: [bigquery-elite]
inputs: [billing or usage data, an architecture to cost]
outputs: [a unit-cost model, waste-reduction guardrails]
tags: [knowledge, finops, cost, cloud, ai, focus]
links: ['[[bigquery-elite]]', '[[observability-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-kb
---

# FinOps & Cloud Value Management (2026)

## 🎯 Purpose
Guidelines for architecting financially efficient cloud systems and aligning engineering spend with business value.

## 🛠️ The Process / Fact

### 1. The FOCUS Standard
- **Standard:** Use the **FinOps Open Cost and Usage Specification (FOCUS)** to normalize billing data across multi-cloud (AWS, GCP, Azure) and SaaS environments.
- **Goal:** Achieve unified, cross-provider reporting for COGS (Cost of Goods Sold) analysis.

### 2. Unit Economics (The North Star)
- **Metrics:** Move beyond "total bill" to **Cost per Unit** (e.g., Cost per API Call, Cost per Active User).
- **Executive Alignment:** Treat cost as a core architectural requirement (NFR). Report FinOps KPIs directly to the CTO.

### 3. AI & Compute Efficiency
- **AI for FinOps:** Use predictive modeling to forecast seasonal spikes and automate commitment planning (RIs/Savings Plans).
- **FinOps for AI:** Strictly manage high-cost GPU instances and vector DB scaling. Use **Spot Instances** for asynchronous AI training to reduce costs by 70%.

### 4. Continuous Waste Reduction
- **Automated Rightsizing:** Use AI Ops tools to continuously rightsize Kubernetes nodes and database instances.
- **Policy-as-Code:** Implement guardrails to auto-stop untagged resources or idle dev environments on weekends.
- **Ephemeral Environments:** Use temporary infrastructure for CI/CD that is auto-destroyed after use.

## ⚠️ Known Quirks or Edge Cases
- **The Idle Tax:** Structurally idle resources are the primary driver of waste. Monitor "Kubernetes Node Efficiency" vs. simple CPU usage.
- **Effective Savings Rate (ESR):** High commitment coverage is only valuable if the reserved resources are actually utilized.

## 🔗 Related Memories
- [[skills/database/bigquery-elite]]
- [[skills/infrastructure/github-actions-elite]]
