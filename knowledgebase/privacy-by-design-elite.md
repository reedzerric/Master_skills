---
name: privacy-by-design-elite
description: Cryptographic shredding through envelope encryption so right-to-erasure works in immutable systems, edge redaction with typed placeholders so raw PII never leaves the device, DPIA 2.0 under the EU AI Act, and differential privacy for aggregated training. Use when user data must be provably deleted from backups, when PII must be masked before transmission, or when an AI system needs a compliance assessment. For agent-specific threats, use security-agentic-elite.
version: 1.1.0
category: core
triggers: [right to be forgotten, delete user data from backups, gdpr erasure request, redact pii before sending, eu ai act compliance, differential privacy, cryptographic shredding, dpia assessment]
dependencies: [security-agentic-elite]
inputs: [a system handling PII, an erasure or compliance requirement]
outputs: [a key-hierarchy design, a redaction and compliance plan]
tags: [knowledge, privacy, gdpr, cryptography, security, edge-ai]
links: ['[[security-agentic-elite]]', '[[postgresql-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-kb
---

# Privacy by Design & GDPR (2026)

## 🎯 Purpose
Guidelines for architecting systems that meet the rigorous 2026 standards for data privacy, cryptographic erasure, and EU AI Act compliance.

## 🛠️ The Process / Fact

### 1. Cryptographic Shredding
- **Right to Erasure:** Use **Envelope Encryption** to fulfill the "Right to Forgotten" in immutable systems.
- **Pattern:** Each user has a unique **User-Level Key (ULK)**. Encrypt user PII with a DEK, then wrap the DEK with the ULK.
- **The Shred:** Destroy the ULK to make all associated user data mathematically unrecoverable across all backups/logs instantly.

### 2. Edge-Based Redaction (Local-First)
- **Redaction-at-Origin:** Redact or mask PII on the client device *before* transmission. Raw PII never leaves the user boundary.
- **Typed Placeholders:** Replace sensitive data with tokens (e.g., `[EMAIL_1]`) so downstream AI maintains context without seeing raw values.

### 3. Compliance & Federated Learning
- **DPIA 2.0:** Assessments must include AI Risk (provenance, explainability) per the EU AI Act (Aug 2026).
- **Differential Privacy:** Use Local Differential Privacy (LDP) to add noise to data on edge devices before aggregation for AI training.
- **Homomorphic Encryption:** For high-risk training, use homomorphic techniques to train models on encrypted data without decryption.

## ⚠️ Known Quirks or Edge Cases
- **Key Rotation:** ULKs must be strictly audited. If a master key is lost, you effectively "shred" your entire user base.
- **Explainability:** The EU AI Act requires model decisions to be explainable; redact the inputs but log the reasoning path.

## 🔗 Related Memories
- [[skills/frontend/local-first-ai-elite]]
- [[knowledgebase/security-agentic-elite]]
