---
name: pptx
description: 'Creating and editing PowerPoint decks: slide layouts, master styling, charts and speaker notes. Use when a deck, slides or a presentation is requested, or when an existing .pptx must be edited. For the palette and typography, use theme-factory; for library-level detail, use document-tooling-deep-dive.'
version: 1.1.0
category: utilities
triggers: [build a slide deck, create a powerpoint, edit a pptx file, presentation from an outline, slide layout and master, add speaker notes]
dependencies: [theme-factory, docx]
inputs: [content or an outline, a theme]
outputs: [a .pptx deck]
tags: [documents, powerpoint, pptx, presentation, design]
links: ['[[theme-factory]]', '[[docx]]', '[[document-tooling-deep-dive]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch4
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
