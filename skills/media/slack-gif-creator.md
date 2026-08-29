---
name: slack-gif-creator
description: 'Producing animated GIFs for Slack with Python PIL: the size and dimension limits Slack enforces, frame construction, and the optimization needed to stay under them. Use when making a Slack emoji or reaction GIF, or when a GIF is rejected for being too large. For static image composition, use canvas-design.'
version: 1.1.0
category: design_media
triggers: [make a slack gif, animated emoji for slack, gif is too large for slack, slack emoji size limit, build an animation with pil]
dependencies: [canvas-design]
inputs: [a concept or source frames]
outputs: [an optimized GIF within Slack's limits]
tags: [media, animation, gif, slack, python]
links: ['[[canvas-design]]', '[[algorithmic-art]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
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
