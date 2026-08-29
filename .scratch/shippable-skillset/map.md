# Map: Shippable Skillset

Label: `wayfinder:map`

## Destination

Master_skills installs as a Claude Code plugin others can add: a curated subset
of skills loads and fires on its own `description`, and every shipped skill's
body conforms to `SKILL_STANDARD.md`. Reaching the end means someone can run
`/plugin marketplace add reedzerric/Master_skills`, install, and have the
skills route without being told to grep anything.

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

_(none yet — charting resolves nothing)_

## Not yet specified

- **Release discipline once it is a plugin.** Version bumps, tags, changelog.
  pocock uses changesets; unclear whether that is worth adopting here. Waits on
  the manifest shape (02).
- **What `skill-router` becomes.** Once Claude Code routes by description
  automatically, a hand-written router skill may be redundant, may be the
  plugin's entry point, or may be the thing that reaches the *non-shipped*
  reference docs. Waits on the ship list (01).
- **How non-shipped reference material is reached.** If `error-codes` and
  `models` do not ship, something has to point an agent at them. Waits on 01.
- **README and install docs for a third party.** Waits on the manifest shape (02).
- **The `security-agentic-elite` / `agentic-security-elite` near-anagram.**
  A rename cascades through manifest paths, dependency edges and links. If the
  directory conversion (03) is happening anyway, it may be nearly free to fold
  in. Waits on 03.
- **Whether `CLAUDE.md`'s "grep the repo" guidance survives** once skills load
  natively. Waits on 01 and 06.

## Out of scope

- **A routing eval harness** (utterance corpus asserted against expected skill).
  Considered as a destination and not chosen; worth doing once there is a
  shipped surface to measure, as a fresh effort.
- **graphify integration.** `CLAUDE.md` leans on it heavily but it is orthogonal
  to whether the skills load.
- **`.gitattributes` / CRLF normalisation.** Real, trivial, unrelated to the
  destination. Do it whenever; it needs no ticket.
