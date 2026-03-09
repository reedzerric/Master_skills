---
title: CSS Elite Architecture (2026)
date: 2026-03-08
task_ref: tech-expansion
confidence_score: 1.0
tags: [frontend, css, layout, subgrid, layers, container-queries]
links: ["[[skills/media/frontend-design]]"]
---

# CSS Elite Architecture (2026)

## 🎯 Purpose
Guidelines for architecting scalable, component-first CSS using native 2026 features. Use for all modern web interfaces.

## 🛠️ The Process / Fact

### 1. Cascade Layers (`@layer`)
- **Strategy:** Declare layer order at the top of your CSS to end "specificity wars."
- **Standard Order:** `reset, base, components, utilities`.
- **Implementation:**
  ```css
  @layer components {
    .card { background: white; }
  }
  @layer utilities {
    .bg-blue { background: blue; } /* Overrides .card regardless of specificity */
  }
  ```

### 2. Container Queries (Component Portability)
- **Goal:** Style components based on their parent's size, not the viewport.
- **Implementation:**
  ```css
  .parent { container-type: inline-size; }
  @container (min-width: 400px) {
    .child { display: grid; }
  }
  ```
- **Units:** Use `cqi` (container query inline-size) for internal component spacing.

### 3. Grid & Subgrid (Deep Alignment)
- **Subgrid:** Allows nested elements to align to a grandparent's grid tracks.
- **Best Practice:** Use `grid-template-rows: subgrid` to align headers/footers across sibling cards with varying content.

### 4. Advanced Selectors & Logic
- **`:has()`:** Use for "parent selection" (e.g., style a card differently if it contains a specific icon).
- **Native Nesting:** Use native CSS nesting (no Sass required for basic nesting).

## ⚠️ Known Quirks or Edge Cases
- **Container Context:** A component can only query its *nearest* container ancestor.
- **Variable Fonts:** Use a single `.woff2` and control via `font-variation-settings`.

## 🔗 Related Memories
- [[skills/media/frontend-design]]
