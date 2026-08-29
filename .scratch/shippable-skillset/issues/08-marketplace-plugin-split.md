# 08 — Which plugins does the marketplace host, and what goes in each?

Type: grilling
Status: open
Blocked by: 02

## Question

Settled in 01: a marketplace hosting several plugins, and everything ships (no
cut). This ticket decides the split.

Sketch from charting, untested:

- `master-skills-core` — engineering domain standards: backend, database,
  frontend, infrastructure, testing, ops/git.
- `master-skills-flows` — the 25 vendored pocock process skills. Already a
  coherent published plugin upstream; keeping them together preserves that
  identity and keeps the MIT attribution legible in one place.
- `master-skills-creative` — game_design, creative_3d, media, documents.

Open sub-decisions:

- Where does `knowledgebase/` go? It is reference, not process, and cuts across
  all three. Its own plugin, or distributed into whichever plugin its subject
  matter serves (`models` and `error-codes` alongside `claude-api` in core)?
- Where do the meta skills go — `skill-standard`, `skill-creator`,
  `memory-validation`, `agent-skills-spec`, `writing-for-agents`? They are about
  authoring this repo, not about building software. A fourth `meta` plugin, or
  core, or not shipped at all since they only matter when working *in* this
  repo, which is exactly when the files are already on disk?
- Do cross-plugin `dependencies` edges work, or must a plugin be closed under
  its dependency graph? `django-elite` depends on `python-elite`,
  `postgresql-elite`, `django-auth-hardening`, `zero-downtime-migrations`. If
  those land in different plugins, installing one gives a skill whose
  prerequisites are absent. Needs the answer from 02 about how the runtime
  treats unknown fields — if `dependencies` is invisible to it, this is a
  documentation problem rather than a functional one.
- Does the vendored set keep upstream's own skill names, or take a prefix?

Resolve: the plugin list, the assignment rule, and what happens to dependency
edges that cross a plugin boundary.

## Comments
