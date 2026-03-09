---
title: Claude Models & Pricing (Feb 2026)
date: 2026-03-08
task_ref: initial-setup
confidence_score: 1.0
tags: [knowledge, ai, pricing, models]
links: ["[[skills/backend/claude-api]]"]
---

# Claude Models & Pricing (Feb 2026)

## 🎯 Purpose
Provide exact model IDs, context windows, and current pricing for Anthropic's Claude API.

## 🛠️ The Process / Fact

| Model             | Model ID            | Context        | Input $/1M | Output $/1M |
| ----------------- | ------------------- | -------------- | ---------- | ----------- |
| Claude Opus 4.6   | `claude-opus-4-6`   | 200K (1M beta) | $5.00      | $25.00      |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 200K (1M beta) | $3.00      | $15.00      |
| Claude Haiku 4.5  | `claude-haiku-4-5`  | 200K           | $1.00      | $5.00       |

### Model Capabilities:
- **Opus 4.6:** Best for complex reasoning, largest context (1M beta). Support for **adaptive thinking** (`thinking: {type: "adaptive"}`). Supports `output_config: {effort: "max"}`.
- **Sonnet 4.6:** High speed-to-intelligence ratio. Supports adaptive thinking.
- **Haiku 4.5:** Fastest and cheapest, ideal for simple high-volume tasks.

## ⚠️ Known Quirks or Edge Cases
- **Exact IDs Required:** Use the exact model strings above (e.g., `claude-opus-4-6`) without date suffixes.
- **Thinking Budget:** Fixed token budgets (`budget_tokens`) are deprecated for 4.6 models in favor of adaptive thinking.

## 🔗 Related Memories
- [[skills/backend/claude-api]]
