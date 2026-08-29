---
name: memory-validation
description: 'Validating this repository''s skill files against the schema: running the validator, the mandatory field set, and the verification workflow before committing. Use when a skill file fails validation, when the pre-commit hook blocks a commit, or when the routing manifest goes stale. For the schema definition itself, use skill-standard.'
version: 1.1.0
category: ai_infrastructure
triggers: [skill file fails validation, pre-commit hook blocked my commit, run the memory validator, required frontmatter fields, the manifest is stale, validate the skills]
dependencies: [pytest-elite]
inputs: [skill files to validate]
outputs: [a validation report, a corrected skill file]
tags: [infra, validation, meta, python]
links: ['[[skill-standard]]', '[[skill-creator]]', '[[pytest-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
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
