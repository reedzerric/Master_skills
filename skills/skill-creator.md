---
name: skill-creator
description: A meta-skill for building, testing, and iteratively improving other skills. Use when working with meta, skill, creation.
version: 1.0.0
category: core
triggers: [meta, skill, creation, evaluation, benchmark, creator]
dependencies: [skill-standard]
inputs: [source files, project config]
outputs: [refactored code, review findings]
title: Skill Creator Framework
date: 2026-03-08
task_ref: initial-setup
confidence_score: 1.0
tags: [meta, skill, creation, evaluation, benchmark]
links: ["[[CORE_MEMORY_PROTOCOL]]"]
---

# Skill Creator Framework

## 🎯 Purpose
A meta-skill for building, testing, and iteratively improving other skills.

## 🛠️ The Process / Fact

### 1. Creation Lifecycle
- **Intent Capture:** Identify the problem, triggers, and expected output format.
- **Interview:** Ask about edge cases and dependencies.
- **Drafting:** Write `SKILL.md` with progressive disclosure.
- **Evaluation Loop:** Run test prompts, review with a human, and iterate.

### 2. Output & Trigger Optimization
- **Trigger Test:** Use `scripts/run_loop.py` to optimize skill descriptions for better triggering accuracy.
- **Human Review:** Use the `eval-viewer` to present test results for qualitative review.

### 3. Progressive Disclosure Rules
- **Metadata:** Name + description (always in context).
- **Body:** Core instructions (<500 lines).
- **Bundled Resources:** Scripts, references, and assets (loaded only when needed).

## ⚠️ Known Quirks or Edge Cases
- **Undertriggering:** Claude may avoid skills for tasks it thinks it can do alone. Make skill descriptions slightly "pushy" to ensure they fire.
- **Stale Evals:** Bad eval queries lead to poor skill descriptions. Use tricky negative test cases.

## 🔗 Related Memories
- [[CORE_MEMORY_PROTOCOL]]
- [[skills/backend/claude-api]]
