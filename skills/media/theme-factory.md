---
name: theme-factory
description: 'Generating and applying a coherent theme: the usage loop from brand tokens through to applied styles, and the theme set available out of the box. Use when deriving a palette and type system from brand inputs, or when applying one theme consistently across documents and slides. For a ready-made palette catalogue instead, use themes.'
version: 1.1.0
category: design_media
triggers: [generate a theme from brand colours, apply a consistent theme, derive a palette, theme my slides, style tokens from a brand]
dependencies: [pdf]
inputs: [brand tokens or a source palette]
outputs: [a theme definition, applied styles]
tags: [media, design, theme, colors, fonts]
links: ['[[themes]]', '[[brand-guidelines]]', '[[pptx]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
---

# Theme Factory & Styling

## 🎯 Purpose
Guidelines for applying professional styling to artifacts (slides, docs, reports) using curated themes.

## 🛠️ The Process / Fact

### 1. Usage Loop
- **Selection:** Use the `theme-showcase.pdf` to allow visual theme selection.
- **Application:** Apply the chosen theme's colors (hex codes) and font pairings consistently across the entire artifact.
- **Custom Themes:** If no preset theme works, generate a new one based on user-provided brand colors/aesthetic.

### 2. Available Themes
- **Ocean Depths:** Calm maritime theme.
- **Sunset Boulevard:** Warm vibrant sunset.
- **Modern Minimalist:** Clean grayscale.
- **Tech Innovation:** Bold, modern tech aesthetic.

## ⚠️ Known Quirks or Edge Cases
- **Contrast:** Ensure proper contrast when applying dark themes (`Midnight Galaxy`) to reports intended for printing.
- **Consistency:** Maintain the identity across different file types (e.g., matching a PPTX to a PDF).

## 🔗 Related Memories
- [[skills/documents/pdf]]
- [[knowledgebase/media/themes]]
