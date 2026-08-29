---
name: agentic-rag-elite
description: 'RAG that reasons rather than retrieving once: Self-RAG self-correction loops, multi-hop and GraphRAG traversal for questions a single lookup cannot answer, and the latency work that makes the loop affordable. Use when retrieval returns plausible but wrong context, when a question needs several hops, or when the RAG loop is too slow. For exposing tools to an agent, use mcp-builder.'
version: 1.1.0
category: ai_infrastructure
triggers: [rag returns wrong context, multi hop question, graphrag, self correcting retrieval, my rag loop is too slow, retrieval quality is poor, rerank retrieved results]
dependencies: [agent-swarms-elite]
inputs: [a corpus and the distribution of questions asked of it]
outputs: [a retrieval loop design, a graph or multi-hop strategy]
tags: [infrastructure, agents, rag, reasoning, loops, graphrag]
links: ['[[agent-swarms-elite]]', '[[evaluation-guide]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
---

# Agentic RAG & Reasoning Loops (2026)

## 🎯 Purpose
Guidelines for architecting autonomous reasoning systems that go beyond simple "Retrieve -> Generate" pipelines.

## 🛠️ The Process / Fact

### 1. Self-Correction Loops (Self-RAG)
- **Standard:** Never trust the first retrieval.
- **Critic Phase:** Use a "Critic" agent to score retrieved chunks for relevance. Fallback to web search or query rewriting if scores are low.
- **Reflection Tokens:** Implement post-generation verification to ensure every claim is explicitly supported by the context.

### 2. Multi-Hop & GraphRAG (Deep Reasoning)
- **Query Decomposition:** Break complex queries (e.g., "Compare X and Y") into atomic sub-queries.
- **Knowledge Graphs:** Use GraphRAG to follow entity relationships (e.g., from *Product* to *Manufacturer* to *Policy*).
- **Multi-Step Retrieval:** Retrieve A -> Update Plan -> Retrieve B -> Synthesize.

### 3. Latency & Performance Optimization
- **Planner vs. Executor:** Use a high-reasoning model (Pro) for the "Planner" and a fast model (Flash) for "Tool Use" and "Reranking."
- **Parallel Tool Use:** Execute all identified sub-queries in parallel to minimize "Time to First Token."

## ⚠️ Known Quirks or Edge Cases
- **The RAG Hallucination:** Even with context, models can misinterpret. Use automated metrics like **RAGAS Faithfulness** and **Citation Precision** to audit.
- **Contextual Headers:** Pre-process chunks to include the document title and section summary for better retrieval accuracy.

## 🔗 Related Memories
- [[skills/infrastructure/agent-swarms-elite]]
- [[knowledgebase/system-design-elite]]
