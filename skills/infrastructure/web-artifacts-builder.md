---
title: Web Artifacts Builder (React & shadcn/ui)
date: 2026-03-08
task_ref: initial-setup
confidence_score: 1.0
tags: [infrastructure, frontend, react, shadcn, tailwind, vite]
links: ["[[skills/media/frontend-design]]", "[[skills/skill-creator]]"]
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
