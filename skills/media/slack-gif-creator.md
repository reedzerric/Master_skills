---
title: Slack GIF Creator (Animated GIFs)
date: 2026-03-08
task_ref: initial-setup
confidence_score: 1.0
tags: [media, animation, gif, slack, python]
links: ["[[skills/media/canvas-design]]"]
---

# Slack GIF Creator (Animated GIFs)

## 🎯 Purpose
Guidelines for creating animated GIFs optimized for Slack (emojis or messages).

## 🛠️ The Process / Fact

### 1. Requirements
- **Dimensions:** Emoji (128x128), Message (480x480).
- **FPS:** 10-30 (lower is smaller file size).
- **Duration:** Under 3 seconds for emojis.

### 2. Implementation (Python PIL)
- **GIFBuilder:** Use the `core.gif_builder` utility.
- **Drawing:** Use `ImageDraw` primitives with **thick lines** (width=2+).
- **Easing:** Use `core.easing` for smooth motion (bounce_out, elastic_out, etc.).

### 3. Optimization
- Reduce colors (48-128).
- Remove duplicates with `remove_duplicates=True`.
- Use `optimize_for_emoji=True` for automated Slack-readiness.

## ⚠️ Known Quirks or Edge Cases
- **Emoji Fonts:** UNRELIABLE. Draw shapes from scratch using PIL.
- **Thin Lines:** Width=1 looks amateurish. Always use width=2+.

## 🔗 Related Memories
- [[skills/media/canvas-design]]
- [[skills/media/algorithmic-art]]
