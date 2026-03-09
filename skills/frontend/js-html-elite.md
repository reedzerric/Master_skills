---
title: JS & HTML Elite Engineering (2026)
date: 2026-03-08
task_ref: tech-expansion
confidence_score: 1.0
tags: [frontend, javascript, html, temporal, accessibility, components]
links: ["[[skills/frontend/css-elite]]"]
---

# JS & HTML Elite Engineering (2026)

## 🎯 Purpose
Guidelines for building modern, high-performance web applications using the 2026 native web platform features.

## 🛠️ The Process / Fact

### 1. The Temporal API (ES2025+)
- **Ditch `Date`:** The `Date` object is legacy. Use `Temporal`.
- **Zoned Time:** `Temporal.ZonedDateTime` handles DST and time zones automatically.
- **Example:**
  ```javascript
  const today = Temporal.Now.plainDateISO();
  const nextWeek = today.add({ days: 7 });
  ```

### 2. Modern Resource Management
- **`using` (Explicit Resource Management):** Native browser feature for auto-cleanup of file handles or sockets.
  ```javascript
  {
    using handle = openFile("data.json");
    // Handle is auto-closed when block ends
  }
  ```

### 3. Declarative Shadow DOM (DSD)
- **Standard:** Use DSD for Server-Side Rendered (SSR) Web Components.
- **Implementation:**
  ```html
  <custom-element>
    <template shadowrootmode="open">
      <style>...</style>
      <slot></slot>
    </template>
  </custom-element>
  ```

### 4. Accessibility (A11y) Standards (WCAG 2.2+)
- **Focus Management:** Visible focus indicators must NEVER be obscured by sticky elements.
- **Target Size:** Interactive elements must have a minimum size (24x24px, preferably 44x44px).
- **ARIA:** Use native HTML elements first. Only use ARIA (`aria-label`, `role="dialog"`) when native semantics are insufficient.

## ⚠️ Known Quirks or Edge Cases
- **Temporal Nano-Precision:** `Temporal` provides nanosecond precision, which may be excessive for some UI tasks; use `PlainDate` for common user dates.
- **Focus Order:** Always manage the tab order logically, especially in dynamic applications or single-page apps.

## 🔗 Related Memories
- [[skills/frontend/css-elite]]
- [[skills/media/frontend-design]]
