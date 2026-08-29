---
name: docx
description: Creating, editing and manipulating Word documents, including direct OOXML editing when the Python library cannot reach a feature. Use when a report, memo, letter or contract is requested in Word format, or when an existing .docx must be modified in place. For PDFs, use pdf; for library-level detail, use document-tooling-deep-dive.
version: 1.1.0
category: utilities
triggers: [create a word document, edit a docx file, generate a report in word, track changes in a docx, edit ooxml directly, write a memo or letter]
dependencies: [pdf, xlsx]
inputs: ['content to render, or an existing .docx']
outputs: [a .docx file]
tags: [documents, word, docx, xml, javascript]
links: ['[[document-tooling-deep-dive]]', '[[pdf]]', '[[xlsx]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch4
---

# DOCX Document Creation & XML Editing

## 🎯 Purpose
Guidelines for creating, editing, and manipulating Word documents (`.docx`). Use when a "report," "memo," or "letter" is requested.

## 🛠️ The Process / Fact

### 1. Creation (JS `docx` library)
- **Library:** `npm install -g docx`.
- **Page Size:** Default is A4; ALWAYS set to US Letter (Width: 12240, Height: 15840 DXA) for North American projects.
- **Lists:** NEVER use Unicode bullets (e.g., •). Use `LevelFormat.BULLET` in numbering config.
- **Tables:** Must set both `columnWidths` on the table AND `width` on each cell using `WidthType.DXA`.

### 2. Editing (XML Unpack/Pack)
- **Unpack:** `python scripts/office/unpack.py doc.docx unpacked/`.
- **XML Editing:** Edit `word/document.xml`.
- **Tracked Changes:** Replace entire `<w:r>` blocks with `<w:ins>`/`<w:del>` siblings. Preserve `<w:rPr>` for formatting.
- **Pack:** `python scripts/office/pack.py unpacked/ output.docx --original original.docx`.

## ⚠️ Known Quirks or Edge Cases
- **Google Docs Compatibility:** Always use `WidthType.DXA` for tables; `PERCENTAGE` breaks in Google Docs.
- **Auto-repair:** The packing script fixes invalid `durableId` and missing `xml:space="preserve"`.

## 🔗 Related Memories
- [[skills/documents/pdf]]
- [[knowledgebase/documents/document-tooling-deep-dive]]
- [[skills/documents/xlsx]]
