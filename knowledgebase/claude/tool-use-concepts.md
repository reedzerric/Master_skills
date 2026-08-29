---
name: tool-use-concepts
description: 'The conceptual model behind Claude tool use: user-defined tools and their schemas, server-side tools (code execution, web search and fetch), and structured outputs. Use when designing a tool definition, writing a tool description, or deciding between a client-side and a server-side tool. For SDK code that runs the loop, use python-deep-dive or typescript-deep-dive.'
version: 1.1.0
category: ai_infrastructure
triggers: [how do i define a tool for claude, tool schema design, server side tools, code execution tool, web search tool, structured outputs from claude, client tool or server tool]
dependencies: [claude-api]
inputs: [a capability to expose as a tool]
outputs: [a tool definition, a client-versus-server decision]
tags: [ai, claude, api, tools, agents]
links: ['[[claude-api]]', '[[python-deep-dive]]', '[[typescript-deep-dive]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-kb
---

# Tool Use Concepts

This file covers the conceptual foundations of tool use with the Claude API.

## User-Defined Tools

### Tool Definition Structure
Each tool requires a name, description, and JSON Schema for its inputs.

```json
{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "City and state, e.g., San Francisco, CA"
      }
    },
    "required": ["location"]
  }
}
```

### Tool Choice Options
| Value | Behavior |
| --- | --- |
| `{"type": "auto"}` | Claude decides whether to use tools (default) |
| `{"type": "any"}` | Claude must use at least one tool |
| `{"type": "tool", "name": "..."}` | Claude must use the specified tool |

## Server-Side Tools: Code Execution
The code execution tool lets Claude run code in a secure, sandboxed container.
- Runs in an isolated container (1 CPU, 5 GiB RAM).
- No internet access.
- Python 3.11 with data science libraries.

## Server-Side Tools: Web Search & Fetch
Web search and web fetch let Claude search the web and retrieve page content.
- Supports **dynamic filtering** (Opus 4.6 / Sonnet 4.6).
- Claude writes code to filter search results for accuracy.

## Structured Outputs
- **JSON outputs** (`output_config.format`): Control Claude's response format.
- **Strict tool use** (`strict: true`): Guarantee valid tool parameter schemas.
