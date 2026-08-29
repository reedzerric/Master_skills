---
name: evaluation-guide
description: 'How to measure MCP server quality: an LLM with no other context answering realistic, complex questions using only the server''s tools. Covers what makes a valid question, the evaluation XML format, and how to run the suite. Use when testing whether an MCP server''s tools are actually usable by a model, or when tool descriptions seem to be the problem. For building the server, use mcp-builder.'
version: 1.1.0
category: ai_infrastructure
triggers: [test my mcp server, are my mcp tools usable, write mcp evaluations, mcp quality check, evaluate my tool descriptions, my agent cannot use my tools]
dependencies: [mcp-deep-dive]
inputs: [an MCP server, realistic questions its users would ask]
outputs: [an evaluation XML suite, a measured quality score]
tags: [infrastructure, mcp, testing, evaluation]
links: ['[[mcp-deep-dive]]', '[[mcp-builder]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-kb
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
