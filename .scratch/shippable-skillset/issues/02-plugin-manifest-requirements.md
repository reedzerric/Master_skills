# 02 — What does a Claude Code plugin actually require?

Type: research
Status: open
Blocked by: —

## Question

Establish, from primary sources rather than inference, what this repo must
produce to be installable via `/plugin marketplace add`.

Specifically:

- Exact required shape of `.claude-plugin/plugin.json` and
  `.claude-plugin/marketplace.json`: required fields, how the `skills` array
  addresses skills, whether paths are directories or files.
- Whether a skill can be a bare `<name>.md` or must be `<name>/SKILL.md`.
  Every skill in the `anthropics/skills` clone at `../skills/` is a directory
  and pocock's `plugin.json` lists directories, but neither is the spec.
- Frontmatter fields the runtime actually reads, and any length limit on
  `description`. Our mean is 346 chars; the longest should be checked against
  the limit.
- How `disable-model-invocation`, `argument-hint` and `allowed-tools` behave,
  since the vendored pocock skills use the first two.
- Whether unknown frontmatter keys (`version`, `category`, `triggers`,
  `dependencies`, `inputs`, `outputs`, `tags`, `links`, `confidence_score`)
  are ignored gracefully or rejected.

Primary sources: <https://agentskills.io/specification>, Claude Code plugin
docs, and the two working examples on disk (`../skills/`, and the pocock layout
preserved under `skills/engineering/`).

**Note on execution:** wayfinder would normally fire this as a parallel
research subagent. This session is operating under a constraint against
spawning agents unasked, so it is worked in-session or by the user invoking
`/research` directly.

## Comments
