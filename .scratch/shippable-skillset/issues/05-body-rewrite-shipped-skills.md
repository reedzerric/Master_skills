# 05 — Rewrite the shipped skills' bodies to the agreed structure

Type: task
Status: open
Blocked by: 01, 04

## Question

Nothing to decide — this is the execution ticket that carries destination B.
It exists so the map does not pretend the work is free.

Once 01 fixes the ship list and 04 fixes the per-shape body contract, rewrite
every shipped skill's body to conform, plus anything the shipped set links to.

Scope depends entirely on its blockers. Upper bound is the 54 files still on the
legacy template; the shipped subset will be smaller.

Batch it the way the routing repair was batched: smallest directory first, gates
green after each, one commit per batch. Do not start a batch on a red gate.

Per batch, record: files touched, shape classified per file, and gate output
verbatim.

## Comments
