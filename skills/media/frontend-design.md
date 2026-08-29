---
name: frontend-design
description: 'Design judgement for interfaces that do not look machine-generated: the philosophy of restraint, hierarchy and intentional spacing, and the implementation rules that follow from it. Use when a UI looks generic or AI-generated, when choosing a spacing and type scale, or when a design needs a point of view. For CSS mechanics, use css-elite.'
version: 1.1.0
category: design_media
triggers: [my ui looks generic, make this look designed, ai slop design, spacing and type scale, visual hierarchy, why does this look off, design a landing page]
dependencies: [web-artifacts-builder, theme-factory]
inputs: [an interface or a design brief]
outputs: [design direction, spacing and type decisions]
tags: [media, frontend, design, css, react, animation]
links: ['[[css-elite]]', '[[themes]]', '[[brand-guidelines]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
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
