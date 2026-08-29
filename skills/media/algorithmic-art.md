---
name: algorithmic-art
description: 'Interactive, seeded generative art with p5.js: flow fields, particle systems, noise-driven composition, and seeds that make a piece reproducible. Use when the user asks for code-based art, a generative sketch, or a flow field. For static poster and print composition, use canvas-design.'
version: 1.1.0
category: design_media
triggers: [generative art sketch, p5js flow field, code based art, particle system art, seeded random art, noise based visuals]
dependencies: [theme-factory]
inputs: [an aesthetic brief, a palette, a seed]
outputs: [a p5.js sketch, rendered frames]
tags: [media, art, generative, p5js, javascript]
links: ['[[theme-factory]]', '[[canvas-design]]', '[[themes]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch4
---

# Algorithmic & Generative Art (p5.js)

## 🎯 Purpose
Guidelines for creating interactive, seeded generative art using p5.js. Use when users request "code-based art," "flow fields," or "generative sketches."

## 🛠️ The Process / Fact

### 1. The Two-Step Workflow
1.  **Algorithmic Philosophy (.md):** Create a manifesto (4-6 paragraphs) defining the computational worldview (e.g., "Organic Turbulence," "Quantum Harmonics").
2.  **Interactive Expression (.html):** Express the philosophy in a self-contained p5.js artifact.

### 2. Implementation Standards
- **Seeded Randomness:** Every sketch MUST use a seed for reproducibility.
- **Interactive UI:** Use the `templates/viewer.html` structure. Include sliders for parameters (scale, speed, density) and seed navigation (Prev/Next/Random).
- **Standalone:** All code (p5.js CDN, CSS, JS) must be inline in one HTML file.

## ⚠️ Known Quirks or Edge Cases
- **Undertriggering:** Claude may default to static shapes. Ensure the "Philosophy" phase pushes for emergent behavior (Perlin noise, flow fields).
- **Performance:** For high particle counts, optimize the `draw()` loop or use `noLoop()` for static generative pieces.

## 🔗 Related Memories
- [[skills/media/theme-factory]]
- [[knowledgebase/media/templates/README]]
