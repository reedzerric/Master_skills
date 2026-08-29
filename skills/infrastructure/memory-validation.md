---
name: memory-validation
description: Automated validation of the "Master Skills" memory system to ensure every memory file adheres to elite metadata standards (YAML headers, confidence scores). Use when working with infra, validation, meta.
version: 1.0.0
category: ai_infrastructure
triggers: [infra, validation, meta, python, memory]
dependencies: [pytest-elite]
inputs: [corpus or prompt, model config]
outputs: [pipeline code, evaluation results]
title: Memory Integrity Validation
date: 2026-03-08
task_ref: framework-practice
confidence_score: 1.0
tags: [infra, validation, meta, python]
links: ["[[CORE_MEMORY_PROTOCOL]]", "[[testing/pytest-elite]]"]
---

# Memory Integrity Validation

## 🎯 Purpose
Automated validation of the "Master Skills" memory system to ensure every memory file adheres to elite metadata standards (YAML headers, confidence scores).

## 🛠️ The Process / Fact

### 1. Usage (Python Logic)
Use the `MemoryValidator` class to scan and verify markdown files:
```python
from memory_validator.validator import MemoryValidator
from pathlib import Path

validator = MemoryValidator()
results = validator.scan_directory(Path("./skills"))
# results = {"path/to/skill.md": True, ...}
```

### 2. Mandatory Fields
Every memory file MUST include:
- `title`: Descriptive name.
- `confidence_score`: Float (0.0 to 1.0).
- `date`: Capture date.

### 3. Verification Workflow
1. Write tests in `tests/test_validator.py`.
2. Run `pytest` to ensure logic matches expectations.
3. Integrate into CI/CD to block "non-elite" memory commits.

## ⚠️ Known Quirks or Edge Cases
- **Regex Extraction:** The validator uses a strict regex for the YAML block. Ensure `---` delimiters are on their own lines at the very top of the file.

## 🔗 Related Memories
- [[CORE_MEMORY_PROTOCOL]]
- [[testing/pytest-elite]]
