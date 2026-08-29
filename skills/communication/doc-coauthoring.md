---
name: doc-coauthoring
description: 'A three-stage workflow for writing a document with someone: gathering context before drafting, refining structure together, then reader-testing the result on someone who was not in the room. Use when co-writing a design doc, proposal, or announcement, or when a draft is technically correct but not landing. For internal status formats, use internal-comms.'
version: 1.1.0
category: utilities
triggers: [help me write this doc, co-author a proposal, my draft is not landing, structure this document, reader test my writing, review my design doc]
dependencies: [internal-comms]
inputs: [a document goal, source material, a target reader]
outputs: [a structured draft, reader-test findings]
tags: [communication, doc, writing, collaboration, structured]
links: ['[[internal-comms]]', '[[internal-comms-deep-dive]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
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
