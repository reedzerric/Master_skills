---
title: Claude API Tool Use Concepts
date: 2026-03-08
task_ref: skill-migration
confidence_score: 1.0
tags: [ai, claude, api, tools, agents]
links: ["[[skills/backend/claude-api]]"]
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
