---
title: PDF Processing & Extraction
date: 2026-03-08
task_ref: initial-setup
confidence_score: 1.0
tags: [documents, pdf, extraction, ocr, python]
links: ["[[testing/webapp-testing]]"]
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
