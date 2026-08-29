---
name: mcp-builder
description: 'Building an MCP server end to end: choosing the stack, the implementation cycle, and verifying the result is usable by a model with no other context. Use when exposing a system''s capabilities to an agent over MCP. For SDK-level reference, use mcp-deep-dive; for measuring the result, use evaluation-guide.'
version: 1.1.0
category: ai_infrastructure
triggers: [build an mcp server, expose my api to claude, wrap a service as mcp tools, mcp server from scratch, connect my system to an agent]
dependencies: [skill-creator]
inputs: [a system to expose, its API surface]
outputs: [a working MCP server, tool definitions]
tags: [infrastructure, mcp, protocol, tools, agent]
links: ['[[mcp-deep-dive]]', '[[evaluation-guide]]', '[[tool-use-concepts]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
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
