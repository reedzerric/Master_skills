---
name: frontend-design
description: Guidelines for creating distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Use when working with media, frontend, design.
version: 1.0.0
category: design_media
triggers: [media, frontend, design, css, react, animation]
dependencies: [web-artifacts-builder, theme-factory]
inputs: [brief, brand tokens]
outputs: [design artifact, style spec]
title: Frontend Design & Aesthetics
date: 2026-03-08
task_ref: initial-setup
confidence_score: 1.0
tags: [media, frontend, design, css, react, animation]
links: ["[[skills/infrastructure/web-artifacts-builder]]", "[[skills/media/theme-factory]]"]
---

# Frontend Design & Aesthetics

## 🎯 Purpose
Guidelines for creating distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics.

## 🛠️ The Process / Fact

### 1. Design Philosophy
- **Anti-Generic:** AVOID `Inter`, `Roboto`, purple gradients, and centered layouts.
- **Bold Aesthetics:** Choose an extreme (e.g., Brutalist, Retro-Futuristic, Organic, Minimalist).
- **Typography:** Choose distinctive fonts that elevate the design. Pair display fonts with refined body fonts.

### 2. Implementation Guidelines
- **Motion:** Use staggered reveals and high-impact micro-interactions. Prefer CSS-only or `Motion` library.
- **Backgrounds:** Use textures (noise, grain, gradients, meshes) instead of solid colors.
- **Composition:** Use asymmetry, diagonal flow, and grid-breaking elements.

## ⚠️ Known Quirks or Edge Cases
- **Context:** Match implementation complexity to the vision. Maximalist designs require elaborate code; minimalist designs require extreme precision in spacing.

## 🔗 Related Memories
- [[skills/infrastructure/web-artifacts-builder]]
- [[skills/media/theme-factory]]
