---
title: Generative Art Templates
date: 2026-03-08
task_ref: skill-migration
confidence_score: 1.0
tags: [media, art, generative, p5js, templates]
links: ["[[algorithmic-art]]"]
---

# Generative Art Templates

## 🎯 Purpose
Supporting files for creating interactive generative art with p5.js.

## 📁 Files

### `viewer.html`
A self-contained HTML template with Anthropic branding, a sidebar for controls, and a p5.js canvas area. Use this as the base for all interactive sketches.

### `generator_template.js`
A boilerplate JavaScript file demonstrating best practices for p5.js generative art:
- Seeded randomness for reproducibility.
- Parameter organization for easy UI binding.
- Class structure for entity-based systems (particles, agents).
- Performance optimization tips.

## 🛠️ Usage
1. Copy `viewer.html` and `generator_template.js`.
2. Inline the JS into the HTML's `<script>` tag.
3. Implement your specific algorithmic philosophy in the `draw()` and `Particle` sections.
4. Customize the UI controls in the sidebar to match your parameters.
