---
name: implement
description: Implements a piece of work from a spec or a set of tickets, driving tests and review as it goes. Use when the user says to build the spec or work the tickets. For deciding what to build, use to-spec or to-tickets first.
version: 1.0.0
category: core
triggers: [implement the spec, build the tickets, start implementation, work the backlog]
dependencies: [tdd, code-review]
inputs: [a spec or tickets]
outputs: [implemented and reviewed code]
tags: [implementation, workflow]
links: ['[[tdd]]', '[[code-review]]']
confidence_score: 0.9
date: '2026-08-28'
task_ref: pocock-skills-import
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use /code-review to review the work.

Commit your work to the current branch.
