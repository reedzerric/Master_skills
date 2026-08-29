# Map: Shippable Skillset

Label: `wayfinder:map`

## Destination

Master_skills installs as a Claude Code plugin **for its author**, structured as
a marketplace hosting several plugins so it can be opened up later without
rework. Skills load and fire on their own `description` rather than being
grepped, and shipped bodies conform to `SKILL_STANDARD.md`.

Public README, install documentation and release discipline are **out of scope**
for this effort.

> Amended after ticket 01. Charting originally set the destination as a
> shareable plugin; the author scoped it back to a personal install while the
> corpus is still being worked on. The marketplace structure is retained,
> because that is the part that costs real plumbing and the part that would be
> expensive to retrofit.

## Notes

**Domain.** A 104-skill markdown corpus with a bespoke routing layer
(`skills_manifest.json`, 647 trigger phrases, dependency edges) that no runtime
reads. Claude Code loads `name` + `description` from `<name>/SKILL.md`
directories. 76 of the 104 skills are currently single `.md` files.

**Skills every session should consult.** `skill-standard` (the schema),
`skill-creator` (authoring), `memory-validation` (the gates), `agent-skills-spec`
(the upstream contract), `writing-for-agents` (prose standards).

**Standing preferences, settled while charting:**

- Shareable plugin, not a personal install. Packaging, naming, README and
  versioning discipline are all in scope because someone else will install it.
- A curated subset ships, not all 104. All descriptions loaded is ~36 KB
  (~9K tokens) of standing rent per session.
- The manifest and its routing layer are **kept and demoted to build-time**.
  They serve `skill-router`, the collision checks and the validation gates.
  `description` is the only field the runtime sees.
- Body conformance covers **what ships**, plus anything the shipped set links
  to. A reference doc nobody loads does not need a hand-written Operating
  Posture.

**Gates, every session.** `python tools/build_manifest.py` clean, no dangling
dependencies; `uv run pytest tests/` green. A batch is not done until both pass.

## Decisions so far

<!-- one line per resolved ticket, gist plus link -->

- [01 — Which skills ship?](issues/01-which-skills-ship.md): the axis is
  battle-tested, but the **cut is deferred** — `confidence_score` is false on
  almost every file and git history cannot separate battle-tested from
  bulk-authored (63 of 65 have exactly one authoring commit; only 9 were ever
  revisited). Everything ships for now; a `battle_tested` flag accretes as
  skills get used, and the cut happens later on evidence. Token budget was
  ruled out as the binding constraint (9K of a 1M window); routing dilution is
  the real cost, and it is low for a personal install.

## Not yet specified

- **What `skill-router` becomes.** Once Claude Code routes by description
  automatically, a hand-written router skill may be redundant, may be the
  marketplace's entry point, or may be what reaches material the plugins do not
  surface. Waits on the plugin split (08).
- **The `security-agentic-elite` / `agentic-security-elite` near-anagram.**
  A rename cascades through manifest paths, dependency edges and links. The
  directory conversion (03) moves every path anyway, so folding it in may be
  nearly free. Waits on 03.
- **Whether `CLAUDE.md`'s "grep the repo" guidance survives** once skills load
  natively. Directive 0 tells an agent to parse the manifest to find a skill,
  which is the job the runtime will be doing. Waits on 06.
- **Whether the corpus tolerates being structurally mixed.** 03 wants to convert
  all 76 files at once to avoid a split corpus; 05 may want body conformance to
  trail `battle_tested` over months. Those pull opposite ways on the same
  question — how much inconsistency is acceptable, and for how long. Waits on
  03 and 05.

## Out of scope

- **A routing eval harness** (utterance corpus asserted against expected skill).
  Considered as a destination and not chosen; worth doing once there is a
  shipped surface to measure, as a fresh effort.
- **graphify integration.** `CLAUDE.md` leans on it heavily but it is orthogonal
  to whether the skills load.
- **`.gitattributes` / CRLF normalisation.** Real, trivial, unrelated to the
  destination. Do it whenever; it needs no ticket.
- **Public README, install docs and release discipline.** Ruled out by the
  destination amendment after ticket 01 — this is a personal install for now.
  Returns only if the destination is redrawn to a shareable plugin, and then as
  a fresh effort.
- **Making the ship cut.** Deferred by
  [01](issues/01-which-skills-ship.md) for want of evidence. It happens once
  `battle_tested` (ticket 09) has accreted real data — a separate pass, not a
  step on this route.
