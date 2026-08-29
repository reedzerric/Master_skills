---
name: pptx
description: Guidelines for creating and editing `.pptx` presentation decks. Use when a "deck," "slides," or "presentation" is requested.
version: 1.0.0
category: utilities
triggers: [documents, powerpoint, pptx, presentation, design]
dependencies: [theme-factory, docx]
inputs: [input document or dataset]
outputs: [generated file]
title: PPTX Presentation Creation & Editing
date: 2026-03-08
task_ref: initial-setup
confidence_score: 1.0
tags: [documents, powerpoint, pptx, presentation, design]
links: ["[[skills/media/theme-factory]]", "[[skills/documents/docx]]"]
---

# PPTX Presentation Creation & Editing

## 🎯 Purpose
Guidelines for creating and editing `.pptx` presentation decks. Use when a "deck," "slides," or "presentation" is requested.

## 🛠️ The Process / Fact

### 1. Creation Lifecycle
- **Extraction:** `python -m markitdown presentation.pptx`.
- **Thumbnails:** `python scripts/thumbnail.py presentation.pptx`.
- **Generation:** Use `pptxgenjs` for from-scratch creation or `openpyxl`/XML for editing templates.

### 2. Design Standards
- **Color Palettes:** Midnight Executive, Forest & Moss, Coral Energy.
- **Hierarchy:** One dominant color (60-70%), supporting tones (20%), and sharp accents (10%).
- **Layout:** One visual element (image/icon/shape) per slide. NO text-only slides.

### 3. QA Protocol (MANDATORY)
- **Content:** `grep -iE "xxxx|lorem|ipsum" output.pptx` to find leftovers.
- **Visuals:** Convert to images (`pdftoppm`) and use subagents to check for overlaps, alignment, and low contrast.

## ⚠️ Known Quirks or Edge Cases
- **Accent Lines:** NEVER use accent lines under titles; they are a hallmark of AI-generated slides. Use whitespace instead.
- **Margin:** Maintain at least 0.5" margin from slide edges.

## 🔗 Related Memories
- [[skills/media/theme-factory]]
- [[skills/documents/docx]]
- [[knowledgebase/documents/document-tooling-deep-dive]]
