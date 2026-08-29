---
name: claude-api
description: 'Integrating the Claude API and Anthropic SDK: model selection for a workload, detecting which language SDK applies, the surface tiers (Messages, tool runner, managed agents) and the implementation pattern for each. Use when adding Claude to an application, choosing between SDK surfaces, or wiring up streaming and tools. For exact model IDs and pricing, use models; for failure handling, use error-codes.'
version: 1.1.0
category: ai_infrastructure
triggers: [add claude to my app, which anthropic sdk surface, messages api or tool runner, integrate the anthropic sdk, call an llm from my backend, managed agents]
dependencies: [models]
inputs: [an application needing LLM capability, a workload description]
outputs: [SDK integration code, a model and surface choice]
tags: [backend, ai, claude, api, sdk]
links: ['[[models]]', '[[error-codes]]', '[[tool-use-concepts]]', '[[python-deep-dive]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
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
- **Prefill Removed:** Assistant message prefills return a 400 error on Opus 4.6. Use structured outputs (`output_config.format`) or system prompts instead.
- **JSON Parsing:** Opus 4.6 may use different escaping in tool calls; always use `json.loads()` or `JSON.parse()`.
- **128K Output:** Requires streaming to avoid HTTP timeouts.

## 🛡️ Technical Integrity
- **Typed Exceptions:** NEVER use string matching for error handling. Use `Anthropic.RateLimitError`, `Anthropic.BadRequestError`, etc.
- **SDK Types:** Use built-in SDK types (e.g., `Anthropic.MessageParam`, `Anthropic.Tool`) instead of redefining interfaces.
- **Thinking:** `budget_tokens` is DEPRECATED for all 4.6 models; use `thinking: {type: "adaptive"}` exclusively.

## 🔗 Related Memories
- [[knowledgebase/claude/models]]
- [[knowledgebase/claude/python-deep-dive]]
- [[knowledgebase/claude/typescript-deep-dive]]
- [[knowledgebase/claude/tool-use-concepts]]
- [[skills/skill-creator]]
