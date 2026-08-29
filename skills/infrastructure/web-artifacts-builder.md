---
name: web-artifacts-builder
description: 'Building self-contained web artifacts with React and shadcn/ui: initialising the project and bundling everything into a single HTML file that makes no external requests. Use when producing a standalone interactive page, dashboard, or visualization that has to run from one file. For visual design judgement, use frontend-design.'
version: 1.1.0
category: ai_infrastructure
triggers: [build a single html artifact, standalone interactive page, bundle react into one file, shadcn artifact, self contained dashboard, page with no external dependencies]
dependencies: [frontend-design, skill-creator]
inputs: [an artifact requirement]
outputs: [a single self-contained HTML file]
tags: [infrastructure, frontend, react, shadcn, tailwind, vite]
links: ['[[frontend-design]]', '[[js-html-elite]]', '[[css-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
---

# Web Artifacts Builder (React & shadcn/ui)

## 🎯 Purpose
Guidelines for building complex, multi-component React artifacts using `shadcn/ui`, `Tailwind CSS`, and `Vite`.

## 🛠️ The Process / Fact

### 1. Initialization
- **Script:** `bash scripts/init-artifact.sh <name>`.
- **Stack:** React 18, TypeScript, Vite, Tailwind CSS 3.4.1.
- **Components:** 40+ shadcn/ui components are pre-installed via the script.

### 2. Bundling (Single HTML)
- **Script:** `bash scripts/bundle-artifact.sh`.
- **Result:** Generates a self-contained `bundle.html` using Parcel and `html-inline`.
- **Requirement:** Must have an `index.html` in the root.

## ⚠️ Known Quirks or Edge Cases
- **"AI Slop" Prevention:** Avoid centered layouts, purple gradients, and generic `Inter` fonts.
- **Node Version:** Script auto-detects Node 18+ and pins Vite version accordingly.

## 🔗 Related Memories
- [[skills/media/frontend-design]]
- [[skills/skill-creator]]
