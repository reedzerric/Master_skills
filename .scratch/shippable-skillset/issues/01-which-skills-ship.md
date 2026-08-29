# 01 — Which skills ship?

Type: grilling
Status: open
Blocked by: —

## Question

Produce the actual list of skills the plugin ships, and the rule that decides
membership so the list can be re-derived rather than re-argued.

Constraints already settled: a curated subset, not all 104. Full-corpus cost is
~36 KB of descriptions (~9K tokens) loaded every session.

The candidate rule from charting was: **process flows and domain standards ship;
reference material stays in the repo and is reached some other way.** That rule
is untested. Things it does not obviously handle:

- `models` and `error-codes` are reference, but an agent writing Claude API code
  needs them constantly. Does "reference" really mean "do not ship"?
- The vendored pocock flows (25) are all process and would all ship, taking the
  count past 40 before any of this repo's own standards are counted.
- `document-tooling-deep-dive` is reference, but `pdf`/`xlsx`/`docx`/`pptx` are
  procedures that link to it. Shipping a skill whose companion does not ship is
  a broken pointer.
- Some domain standards are narrow enough to be dead weight for most users
  (`slack-gif-creator`, `blender-procedural-modeling`, the four game_design
  skills). Narrowness is a different axis from reference-vs-process.

Resolve: the membership rule, the resulting list, and what happens to the
excluded ones. A count and a token budget for the shipped set is part of the
answer.

## Comments
