---
name: docx
description: Guidelines for creating, editing, and manipulating Word documents (`.docx`). Use when a "report," "memo," or "letter" is requested.
version: 1.0.0
category: utilities
triggers: [documents, word, docx, xml, javascript]
dependencies: [pdf, xlsx]
inputs: [input document or dataset]
outputs: [generated file]
title: DOCX Document Creation & XML Editing
date: 2026-03-08
task_ref: initial-setup
confidence_score: 1.0
tags: [documents, word, docx, xml, javascript]
links: ["[[skills/documents/pdf]]", "[[skills/documents/xlsx]]"]
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
