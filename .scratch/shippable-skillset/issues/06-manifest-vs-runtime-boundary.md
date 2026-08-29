# 06 — Where does the manifest sit once the runtime ignores it?

Type: grilling
Status: open
Blocked by: 02

## Question

Settled while charting: the manifest and its 647 triggers are kept and demoted
to build-time. This ticket decides what that means concretely.

Claude Code reads `name` and `description`. It ignores `category`, `triggers`,
`dependencies`, `inputs`, `outputs`, `tags`, `links`, `confidence_score` —
which is most of the schema, and all of the part just repaired.

Open sub-decisions:

- Where is the boundary documented so a future author does not assume `triggers`
  routes anything? `SKILL_STANDARD.md` currently implies the routing extensions
  are load-bearing. It should say plainly which fields the runtime sees and
  which exist only for the build.
- Does `skills_manifest.json` ship inside the plugin, or stay a repo artifact?
  It is useful to `skill-router` at runtime only if something reads it.
- Do the gates gain a check that `description` alone is sufficient to route —
  i.e. that negative scope really is in the prose, not leaning on `triggers`?
- Does anything in the corpus currently instruct an agent to parse the manifest
  in a way that breaks once skills auto-load? (`CLAUDE.md` directive 0 does
  exactly this.)

Resolve: the documented field-visibility contract, the manifest's shipping
status, and any gate that enforces the boundary.

## Comments
