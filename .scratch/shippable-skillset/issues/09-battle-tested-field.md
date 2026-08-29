# 09 — How does `battle_tested` accrete, and what eventually reads it?

Type: grilling
Status: open
Blocked by: 06

## Question

01 deferred the ship cut because there is no honest signal for "battle-tested".
This ticket builds the signal so the cut can be made later on evidence.

Hard-won constraint from earlier work: **a new frontmatter field is inert until
`tools/build_manifest.py` reads it.** The validator tolerates unknown keys and
the manifest builder constructs entries from a fixed key list, so a field can
look like it works while being invisible to every consumer. Whatever is added
here must be wired through the builder in the same change.

Open sub-decisions:

- Shape. Boolean `battle_tested: true`, or something with more information —
  a date last used in anger, a count, a free-text note on what it was used for?
  A boolean is cheap and honest; a date decays gracefully and shows staleness.
- Who sets it, and when. Manually by the author after using a skill, or
  semi-automatically from some observable signal? There is no usage telemetry,
  so it is almost certainly manual — which means it must be near-zero friction
  or it will not happen.
- What is the default for the existing 104? Absent, rather than `false` — an
  unmarked skill is unproven, not disproven, and stamping `false` everywhere
  repeats the mistake `confidence_score` already made.
- What does `confidence_score` become? It currently carries the exact meaning
  this field is meant to carry, and carries it falsely on almost every file.
  Deprecate it, redefine it, or leave it as decoration.
- What reads the flag: the eventual cut, the gates, `skill-router`, a report?

Resolve: field shape, default, who sets it, the builder wiring, and the fate of
`confidence_score`.

## Comments
