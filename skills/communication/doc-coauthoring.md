---
name: doc-coauthoring
description: Guidelines for collaborative document creation (PRDs, technical specs, decision docs). Use when working with communication, doc, writing.
version: 1.0.0
category: utilities
triggers: [communication, doc, writing, collaboration, structured, coauthoring]
dependencies: [internal-comms]
inputs: [input document or dataset]
outputs: [generated file]
title: Doc Co-Authoring Workflow
date: 2026-03-08
task_ref: initial-setup
confidence_score: 1.0
tags: [communication, doc, writing, collaboration, structured]
links: ["[[skills/communication/internal-comms]]"]
---

# Doc Co-Authoring Workflow

## 🎯 Purpose
Guidelines for collaborative document creation (PRDs, technical specs, decision docs).

## 🛠️ The Process / Fact

### 1. Stage 1: Context Gathering
- **Identify:** Document type, audience, impact, template.
- **Clarify:** 5-10 specific questions to ensure knowledge alignment.

### 2. Stage 2: Refinement & Structure
- **Brainstorm:** Generate 5-20 options per section.
- **Draft:** Create the doc section-by-section using surgical edits (`str_replace`).

### 3. Stage 3: Reader Testing
- **Goal:** Catch blind spots.
- **Fresh Claude:** Use a sub-agent to "read" the doc with no context and predict questions or identify ambiguity.

## ⚠️ Known Quirks or Edge Cases
- **Context Bleed:** The original conversation holds too much "implied" knowledge. Use Reader Testing to ensure the doc stands alone.

## 🔗 Related Memories
- [[skills/communication/internal-comms]]
