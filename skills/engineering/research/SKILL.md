---
name: research
description: Investigates a question against high-trust primary sources and captures the findings as a Markdown file in the repository. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated.
version: 1.0.0
category: core
triggers: [research this, look up the docs, gather sources, find out how x works]
dependencies: []
inputs: [a research question]
outputs: [a Markdown findings file with cited sources]
tags: [research, documentation]
links: ['[[skill-router]]']
confidence_score: 0.9
date: '2026-08-28'
task_ref: pocock-skills-import
---

Spin up a **background agent** to do the research, so you keep working while it reads.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.
