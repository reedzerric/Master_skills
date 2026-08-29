---
name: xlsx
description: Guidelines for creating, editing, and analyzing `.xlsx`, `.csv`, and `.xlsm` files. Use when tabular data is the primary input or output.
version: 1.0.0
category: utilities
triggers: [documents, excel, xlsx, formulas, pandas]
dependencies: [pdf]
inputs: [input document or dataset]
outputs: [generated file]
title: XLSX Spreadsheet Mastery
date: 2026-03-08
task_ref: initial-setup
confidence_score: 1.0
tags: [documents, excel, xlsx, formulas, pandas]
links: ["[[skills/documents/pdf]]"]
---

# XLSX Spreadsheet Mastery

## 🎯 Purpose
Guidelines for creating, editing, and analyzing `.xlsx`, `.csv`, and `.xlsm` files. Use when tabular data is the primary input or output.

## 🛠️ The Process / Fact

### 1. Library Selection
- **`pandas`**: Best for bulk analysis, data cleaning, and simple exports.
- **`openpyxl`**: Required for complex formatting, cell-level control, and **formulas**.

### 2. CRITICAL: Formulas, Not Hardcodes
- **NEVER** calculate values in Python and hardcode them.
- **ALWAYS** use Excel strings (e.g., `sheet['B10'] = '=SUM(B2:B9)'`) so the sheet stays dynamic.

### 3. Standards
- **Font:** Professional (Arial/Times New Roman).
- **Financial Standards:** Blue text (RGB: 0,0,255) for inputs; Black text (0,0,0) for formulas.
- **Number Formats:** Years as strings; Currency as `$#,##0`.

### 4. Recalculation Loop
- Modified sheets via `openpyxl` do not hold calculated values.
- **MANDATORY:** Run `python scripts/recalc.py <file>` using LibreOffice before final delivery.

## ⚠️ Known Quirks or Edge Cases
- **`data_only=True`:** If `openpyxl` loads a file with this flag and saves it, **all formulas are lost forever**.
- **1-Indexed:** Excel is 1-indexed (Row 1), while DataFrames are 0-indexed.

## 🔗 Related Memories
- [[skills/documents/pdf]]
- [[knowledgebase/documents/document-tooling-deep-dive]]
