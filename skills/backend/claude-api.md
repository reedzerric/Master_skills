---
title: Claude API & Anthropic SDK Integration
date: 2026-03-08
task_ref: initial-setup
confidence_score: 1.0
tags: [backend, ai, claude, api, sdk]
links: ["[[knowledgebase/claude-models]]"]
---

# Claude API & Anthropic SDK Integration

## 🎯 Purpose
Guidelines for building LLM-powered applications using the Claude API, Anthropic SDK, and Agent SDK. Covers model selection, thinking parameters, and language-specific patterns.

## 🛠️ The Process / Fact

### 1. Model Selection (CRITICAL)
- **Default Model:** Always use `claude-opus-4-6`.
- **Thinking:** Use `thinking: {type: "adaptive"}` for complex tasks. 
- **Note:** `budget_tokens` is DEPRECATED for 4.6 models.

### 2. Language Detection
Identify the project language via files (e.g., `package.json` for TS, `requirements.txt` for Python) before providing code examples.

### 3. Surface Tiers
- **Single Call:** Use for classification, summarization, extraction.
- **Workflow:** Use Tool Use for multi-step pipelines.
- **Agent SDK:** Use when built-in file/web/terminal access and MCP are required.

### 4. Implementation Patterns
- **Streaming:** Default to streaming for long outputs to prevent timeouts.
- **Compaction:** Enable for long-running conversations (Opus 4.6 only, requires `compact-2026-01-12` header).

## ⚠️ Known Quirks or Edge Cases
- **Prefill Removed:** Assistant message prefills return a 400 error on Opus 4.6. Use structured outputs or system prompts instead.
- **JSON Parsing:** Opus 4.6 may use different escaping in tool calls; always use `json.loads()` or `JSON.parse()`.
- **128K Output:** Requires streaming to avoid HTTP timeouts.

## 🔗 Related Memories
- [[knowledgebase/claude-models]]
- [[skills/skill-creator]]
