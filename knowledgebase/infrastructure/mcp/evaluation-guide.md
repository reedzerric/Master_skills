---
title: MCP Evaluation Guide
date: 2026-03-08
task_ref: skill-migration
confidence_score: 1.0
tags: [infrastructure, mcp, testing, evaluation]
links: ["[[knowledgebase/infrastructure/mcp/mcp-deep-dive]]"]
---

# MCP Evaluation Guide

## The Gold Standard
The quality of an MCP server is measured by how well an LLM (with NO other context) can answer complex, realistic questions using ONLY the provided tools.

## Question Requirements
1. **Independent:** No question depends on another.
2. **Read-Only:** No state-modifying operations.
3. **Complex:** Requires multiple (potentially dozens) of tool calls.
4. **Stable:** Answers won't change over time (use historical data).
5. **Verifiable:** Single, unambiguous value (String Comparison).

## Evaluation XML Format
```xml
<evaluation>
   <qa_pair>
      <question>Find the project created in Q2 2024 with the highest number of completed tasks. What is the project name?</question>
      <answer>Website Redesign</answer>
   </qa_pair>
</evaluation>
```

## Implementation Workflow
1. **Tool Inspection:** Understand schemas without calling tools.
2. **Content Exploration:** Use READ-ONLY tools to find interesting data points.
3. **Task Generation:** Create 10 human-readable questions.
4. **Verification:** Solve the questions yourself to verify the answers.

## Running Evaluations
Use `scripts/evaluation.py` (standard in the MCP toolkit).
- **stdio:** Script launches the server for you.
- **sse/http:** You must start the server first.
