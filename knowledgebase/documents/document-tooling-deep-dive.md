---
name: document-tooling-deep-dive
description: 'Library-level reference for programmatic document work: PDF extraction and generation, XLSX formulas and formatting, DOCX through Node and raw OOXML, and PPTX layout with its QA checks. Use when choosing a library or debugging document-generation code. For an end-to-end task workflow, use the pdf, xlsx, docx or pptx skill instead.'
version: 1.1.0
category: utilities
triggers: [which library for pdf extraction, generate an excel file from python, edit a docx programmatically, build a powerpoint from code, openpyxl formatting, extract text from a pdf, write ooxml directly]
dependencies: [pdf, xlsx, docx, pptx]
inputs: [a document generation or extraction task]
outputs: [a library choice, working document-manipulation code]
tags: [documents, python, automation, pdf, excel, word, powerpoint]
links: ['[[pdf]]', '[[xlsx]]', '[[docx]]', '[[pptx]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-kb
---

# Document Tooling & Automation Deep Dive

## 📑 PDF Processing (Python)

### 1. Basic Operations (`pypdf`)
- **Merge/Split:** Use `PdfWriter` and `PdfReader`.
- **Metadata:** `reader.metadata` for title, author, etc.
- **Rotation:** `page.rotate(90)`.

### 2. Extraction (`pdfplumber`)
- **Text:** `page.extract_text()` (preserves layout better than pypdf).
- **Tables:** `page.extract_tables()` -> returns list of lists (convert to Pandas DataFrame).

### 3. Creation (`reportlab`)
- **Canvas:** Precise coordinate-based drawing (`c.drawString(x, y, text)`).
- **Platypus:** High-level layout (Paragraphs, Spacers, Tables).
- **CRITICAL:** Use `<sub>` and `<super>` tags for chemical formulas/math; never use Unicode subscripts/superscripts.

---

## 📊 Excel / XLSX (Python & Standards)

### 1. The "Elite" Standard
- **Blue Text:** Hardcoded inputs (RGB: 0,0,255).
- **Black Text:** Formulas and calculations (RGB: 0,0,0).
- **Formula-First:** Never hardcode a value that can be a formula. Use `sheet['B10'] = '=SUM(B2:B9)'`.
- **Zero Errors:** Recalculate and verify with `scripts/recalc.py` to ensure no `#REF!`, `#DIV/0!`, etc.

### 2. Tooling
- **Pandas:** Best for data analysis and bulk CSV/XLSX export.
- **Openpyxl:** Best for formulas, formatting (Font, Fill, Alignment), and preserving existing templates.
- **Recalc:** Always run `python scripts/recalc.py output.xlsx` after saving with openpyxl.

---

## 📝 Word / DOCX (Node & XML)

### 1. New Documents (`docx-js`)
- Use the Node.js `docx` library for creating professional documents from scratch.
- **Key Rules:** Set page size explicitly (US Letter is 12240x15840 DXA), use `HeadingLevel` for TOC compatibility, and never use `\n` (use separate Paragraphs).

### 2. Editing Existing Docs (Unpack/Pack)
- **Step 1:** `python scripts/office/unpack.py doc.docx unpacked/`
- **Step 2:** Edit XML in `unpacked/word/document.xml`. Use smart quote entities (`&#x2019;` for apostrophes).
- **Step 3:** `python scripts/office/pack.py unpacked/ output.docx --original doc.docx`

---

## 📊 PowerPoint / PPTX (Design & QA)

### 1. Design Philosophy
- **"Sandwich" Structure:** Dark backgrounds for Title/Conclusion, light for content.
- **Visual-First:** Every slide needs an image, icon, chart, or shape. No text-only slides.
- **Typography:** Slide titles 36-44pt, Body 14-16pt.

### 2. Visual QA
- Convert to images: `soffice --convert-to pdf` -> `pdftoppm -jpeg`.
- Inspect for overlaps, text overflow, and alignment issues using a subagent.
