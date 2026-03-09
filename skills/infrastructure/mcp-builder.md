---
title: MCP Server Development
date: 2026-03-08
task_ref: initial-setup
confidence_score: 1.0
tags: [infrastructure, mcp, protocol, tools, agent]
links: ["[[skills/skill-creator]]"]
---

# MCP Server Development

## 🎯 Purpose
Guidelines for building high-quality Model Context Protocol (MCP) servers to integrate external APIs/services with LLMs.

## 🛠️ The Process / Fact

### 1. Technology Stack
- **Language:** TypeScript (recommended for best SDK support and static typing).
- **Transport:** Streamable HTTP (remote) or stdio (local).
- **Frameworks:** `@modelcontextprotocol/sdk` (Node) or `fastmcp` (Python).

### 2. Implementation Cycle
- **Research:** Check `https://modelcontextprotocol.io/specification/` for protocol updates.
- **Design:** Prioritize comprehensive API coverage.
- **Tooling:** Use Zod/Pydantic for input schemas with clear descriptions and examples.
- **Errors:** Provide actionable error messages that guide the LLM to a solution.

### 3. Verification
- **MCP Inspector:** Always test with `npx @modelcontextprotocol/inspector`.
- **Evals:** Create a `qa_pair` XML file with 10 complex, realistic questions to test effectiveness.

## ⚠️ Known Quirks or Edge Cases
- **Tool Naming:** Use clear prefixes (e.g., `github_`) to avoid collisions.
- **Latency:** Agents prefer focused, paginated data over large, raw API responses.

## 🔗 Related Memories
- [[skills/skill-creator]]
- [[skills/backend/claude-api]]
- [[knowledgebase/infrastructure/mcp/mcp-deep-dive]]
- [[knowledgebase/infrastructure/mcp/evaluation-guide]]
