---
name: wait-what
description: Stops and re-pitches the last message when it did not land. User-invoked. Use when the user says 'wait, what', 'that made no sense', or asks for the last explanation again from a different angle.
version: 1.0.0
category: utilities
triggers: [wait what, that did not land, re-pitch that, say that again differently]
dependencies: []
inputs: [the previous message]
outputs: [a re-pitched explanation]
tags: [communication, clarity]
links: ['[[skill-router]]']
confidence_score: 0.9
date: '2026-08-28'
task_ref: pocock-skills-import
disable-model-invocation: true
---

Wait, I don't understand where you've got to here. Re-pitch that: give me a little bit of context, talk in ASD-STE100 Simplified Technical English, and use the ubiquitous language from `CONTEXT.md` (follow `CONTEXT-MAP.md` to the right one if the repo has more than one).
