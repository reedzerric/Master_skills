---
name: pdf
description: Reading, extracting, merging, splitting and creating PDF files, including OCR for scanned pages and table extraction. Use when the user mentions a .pdf, needs data pulled out of one, or wants a PDF produced. For library-level detail, use document-tooling-deep-dive; for spreadsheets, use xlsx.
version: 1.1.0
category: utilities
triggers: [extract text from a pdf, merge pdf files, split a pdf, fill a pdf form, ocr a scanned document, create a pdf report, extract tables from a pdf]
dependencies: [webapp-testing]
inputs: ['a PDF file, or content to render as one']
outputs: [extracted text or tables, a generated PDF]
tags: [documents, pdf, extraction, ocr, python]
links: ['[[document-tooling-deep-dive]]', '[[xlsx]]', '[[docx]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch4
---

# PDF Processing & Extraction

## 🎯 Purpose
Guidelines for reading, extracting, merging, splitting, and creating PDF files. Use when a user mentions `.pdf` or needs data from a PDF.

## 🛠️ The Process / Fact

### 1. Recommended Libraries
- **`pypdf`**: Best for basic operations (merge, split, metadata, rotation).
- **`pdfplumber`**: Superior for text and table extraction with layout preservation.
- **`reportlab`**: Primary library for generating new PDFs from scratch.
- **`pytesseract` + `pdf2image`**: Required for OCR on scanned PDFs.

### 2. Core Snippets
- **Extract Tables (pdfplumber):**
  ```python
  with pdfplumber.open("doc.pdf") as pdf:
      table = pdf.pages[0].extract_table()
  ```
- **Merge PDFs (pypdf):**
  ```python
  writer = PdfWriter()
  for p in ["1.pdf", "2.pdf"]: writer.add_page(PdfReader(p).pages[0])
  ```

## ⚠️ Known Quirks or Edge Cases
- **ReportLab Unicode:** NEVER use Unicode subscript/superscript (e.g., ², ₃). They render as black boxes. Use XML tags instead: `<sub>2</sub>` or `<super>2</super>`.
- **Scanned PDFs:** `pypdf` and `pdfplumber` will return empty strings for scanned images; must use OCR.

## 🔗 Related Memories
- [[skills/documents/xlsx]]
- [[knowledgebase/documents/document-tooling-deep-dive]]
