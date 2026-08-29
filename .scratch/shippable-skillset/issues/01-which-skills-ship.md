# 01 — Which skills ship?

Type: grilling
Status: resolved
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

## Answer

**The membership axis is battle-tested. The cut is deferred, because the
evidence to make it does not exist yet.**

Rejected on the numbers: the charting hypothesis (reference stays, process
ships) removes 19 skills and 1,818 tokens — 20% — and leaves 85 skills still
loading. It was aimed at the wrong axis.

Also rejected as the *binding* constraint: the token budget. 8,996 tokens
against a 1M window is 0.9%. The real cost of a wide install is routing
dilution, not context. That cost is much lower for a personal install, where
the author already knows what is in their own toolkit.

**Why the cut is deferred rather than made.** `confidence_score` cannot carry
the battle-tested signal — 1.0 was stamped on almost everything by the schema
migration, not earned. Git history was measured as a substitute and does not
separate the two either: 63 of 65 skills with any non-bulk commit have exactly
one, which is the original authoring commit. The only genuine signal is the
nine skills that were *revisited* — `claude-api` (3 commits), then
`algorithmic-art`, `docx`, `pdf`, `pptx`, `xlsx`, `mcp-builder`,
`theme-factory`, `webapp-testing` (2 each). Nine is too few to be a plugin, and
inventing the rest would launder guesses as the author's experience.

**Consequently:**

1. Everything ships into the personal marketplace for now. No cut.
2. A `battle_tested` flag is introduced and accretes honestly as skills are
   used over the coming weeks (ticket 09).
3. The cut happens when the data exists, as a fresh pass — not in this map.

**Knock-on effects:**

- The directory conversion (03) now has a settled scope: all 104, since
  everything ships. Its dependency on this ticket is discharged.
- The body rewrite (05) inherits an expanded scope. "Body conformance covers
  what ships" plus "everything ships" means all 54 legacy-template files, which
  is the opposite of what deciding "only what ships" was meant to achieve. 05
  now carries an open sub-decision: rewrite all 54, or let body conformance
  follow `battle_tested` as it accretes.
- Which plugin each skill lands in is now its own question (ticket 08).

## Comments
