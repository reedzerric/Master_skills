---
title: API Contract-First Engineering (2026)
date: 2026-03-08
task_ref: mit-professor-critique
confidence_score: 1.0
tags: [backend, api, openapi, grpc, protobuf, contracts]
links: ["[[knowledgebase/architectural-patterns]]"]
---

# API Contract-First Engineering (2026)

## 🎯 Purpose
Guidelines for enforcing strict, machine-readable contracts between all microservices, frontends, and AI agents BEFORE writing business logic.

## 🛠️ The Process / Fact

### 1. Contract-First Workflow
- **Rule:** Never write an API controller before the contract is approved.
- **REST APIs:** Use **OpenAPI 3.1+**. Store `openapi.yaml` in a central schema registry.
- **Internal Services:** Use **gRPC and Protocol Buffers (Protobuf)** for high-throughput, strictly-typed binary communication between internal microservices.

### 2. Automated Generation
- **Server Stubs:** Generate backend routing interfaces directly from the OpenAPI/Protobuf definitions.
- **Client SDKs:** Generate frontend TypeScript clients (using tools like `Orval` or `buf`) to ensure compile-time synchronization with the backend.
- **Agentic Tools:** OpenAPI specs serve directly as the definition schemas for MCP (Model Context Protocol) servers and LLM tool arrays.

### 3. Contract Evolution & Versioning
- **Never Break the Contract:** APIs must be strictly additive.
- **Deprecation:** Use the `@deprecated` directive in Protobuf/OpenAPI and monitor telemetry before sunsetting fields.
- **Linting:** Use `Spectral` (for OpenAPI) or `Buf` (for Protobuf) in CI/CD to enforce naming conventions and catch breaking changes instantly.

## ⚠️ Known Quirks or Edge Cases
- **JSON Serialization:** When bridging gRPC and REST (via gRPC-Gateway), be cautious of `int64` serialization to JSON, which loses precision in JavaScript. Always transmit 64-bit integers as strings.

## 🔗 Related Memories
- [[knowledgebase/architectural-patterns]]
- [[skills/infrastructure/mcp-builder]]
