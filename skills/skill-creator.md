---
name: skill-creator
description: 'Authoring a new skill for this repository: the creation lifecycle, writing descriptions and triggers that route correctly, and when to split bulk into companion files. Use when adding a skill, splitting an oversized one, or when a skill is not being picked up by routing. For the schema it must satisfy, use skill-standard; for validating it, use memory-validation.'
version: 1.1.0
category: core
triggers: [create a new skill, my skill is not being triggered, split a skill into companion files, write a skill description, add a skill to the manifest]
dependencies: [skill-standard]
inputs: [a capability to capture as a skill]
outputs: [a conforming skill file, a manifest entry]
tags: [meta, skill, creation, evaluation, benchmark]
links: ['[[skill-standard]]', '[[memory-validation]]', '[[writing-for-agents]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
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
