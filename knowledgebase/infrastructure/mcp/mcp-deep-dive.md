---
name: mcp-deep-dive
description: from mcp.server.fastmcp import FastMCP. Use when working with infrastructure, mcp, protocol.
version: 1.0.0
category: ai_infrastructure
triggers: [infrastructure, mcp, protocol, typescript, python, deep, dive]
dependencies: [mcp-builder, evaluation-guide]
inputs: [corpus or prompt, model config]
outputs: [pipeline code, evaluation results]
title: MCP Server Deep Dive
date: 2026-03-08
task_ref: skill-migration
confidence_score: 1.0
tags: [infrastructure, mcp, protocol, typescript, python]
links: ["[[skills/infrastructure/mcp-builder]]", "[[knowledgebase/infrastructure/mcp/evaluation-guide]]"]
---

# MCP Server Deep Dive

## Quick Reference
- **Python Naming:** `{service}_mcp` (e.g., `slack_mcp`)
- **Node Naming:** `{service}-mcp-server` (e.g., `slack-mcp-server`)
- **Tool Naming:** `{service}_{action}_{resource}` (e.g., `github_create_issue`)
- **Transport:** Use `stdio` for local, `streamable_http` for remote.

## Implementation Patterns

### 1. Tool Design
- Use **snake_case** for all tool names.
- Always include a **service prefix** to avoid collisions.
- Provide clear **annotations** (`readOnlyHint`, `destructiveHint`, etc.).
- Return both **JSON** (programmatic) and **Markdown** (human-readable) formats.

### 2. Python (FastMCP)
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my_service_mcp")

@mcp.tool()
async def my_tool(param: str) -> str:
    """Tool description with clear parameter info."""
    return f"Result: {param}"

if __name__ == "__main__":
    mcp.run()
```

### 3. TypeScript (McpServer)
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

const server = new McpServer({
  name: "my-service-mcp-server",
  version: "1.0.0"
});

server.tool("my_tool", 
  { param: z.string() }, 
  async ({ param }) => ({
    content: [{ type: "text", text: `Result: ${param}` }]
  })
);
```

## Advanced Features
- **Context Injection:** Access `Context` for logging, progress reporting, and user input (`ctx.elicit`).
- **Resources:** Use `@mcp.resource("uri://...")` for static/semi-static data.
- **Lifespan:** Use async context managers to manage persistent DB connections or config.

## Quality Standards
- **DRY:** Extract common API logic into shared clients.
- **Pagination:** Always respect `limit` and return `has_more`.
- **Errors:** Return actionable error messages that guide the LLM.
