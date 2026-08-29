---
name: mcp-deep-dive
description: 'MCP server implementation reference: FastMCP in Python and the TypeScript SDK, transport choices, resources, prompts, sampling, and the quality bar a tool description has to clear. Use when writing or debugging MCP server code. For a guided build workflow, use mcp-builder; for measuring the result, use evaluation-guide.'
version: 1.1.0
category: ai_infrastructure
triggers: [write an mcp server, fastmcp, mcp transport stdio or http, expose a resource over mcp, mcp tool description quality, debug my mcp server]
dependencies: [mcp-builder, evaluation-guide]
inputs: [a capability to expose over MCP]
outputs: [MCP server code]
tags: [infrastructure, mcp, protocol, typescript, python]
links: ['[[mcp-builder]]', '[[evaluation-guide]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-kb
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
