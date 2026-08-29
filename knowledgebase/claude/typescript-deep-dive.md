---
name: typescript-deep-dive
description: npm install @anthropic-ai/sdk. Use when working with ai, claude, api.
version: 1.0.0
category: ai_infrastructure
triggers: [ai, claude, api, typescript, sdk, deep, dive]
dependencies: [claude-api, tool-use-concepts]
inputs: [corpus or prompt, model config]
outputs: [pipeline code, evaluation results]
title: Claude API TypeScript Deep Dive
date: 2026-03-08
task_ref: skill-migration
confidence_score: 1.0
tags: [ai, claude, api, typescript, sdk]
links: ["[[skills/backend/claude-api]]", "[[knowledgebase/claude/tool-use-concepts]]"]
---

# Claude API TypeScript Deep Dive

## Installation & Initialization
```bash
npm install @anthropic-ai/sdk
```
```typescript
import Anthropic from "@anthropic-ai/sdk";
const client = new Anthropic();
```

## Core Patterns

### Basic Message
```typescript
const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello!" }],
});
```

### Prompt Caching
```typescript
const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  cache_control: { type: "ephemeral" },
  system: "Large context...",
  messages: [{ role: "user", content: "Summarize" }],
});
```

### Adaptive Thinking (Opus 4.6)
```typescript
const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 16000,
  thinking: { type: "adaptive" },
  output_config: { effort: "high" },
  messages: [{ role: "user", content: "Solve..." }],
});
```

## Tool Use & Agents

### Tool Runner (Recommended)
Use `betaZodTool` for type-safe tools and automatic looping.
```typescript
import { betaZodTool } from "@anthropic-ai/sdk/helpers/beta/zod";
import { z } from "zod";

const getWeather = betaZodTool({
  name: "get_weather",
  description: "Get current weather",
  inputSchema: z.object({ location: z.string() }),
  run: async ({ location }) => `72°F in ${location}`,
});

const finalMessage = await client.beta.messages.toolRunner({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  tools: [getWeather],
  messages: [{ role: "user", content: "What's the weather in Paris?" }],
});
```

### Code Execution
```typescript
const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  tools: [{ type: "code_execution_20260120", name: "code_execution" }],
  messages: [{ role: "user", content: "Analyze data..." }],
});
```

## Error Handling
Use typed exceptions: `Anthropic.RateLimitError`, `Anthropic.BadRequestError`, etc.
