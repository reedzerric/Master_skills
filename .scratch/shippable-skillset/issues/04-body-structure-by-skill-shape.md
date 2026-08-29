# 04 — Reconcile SKILL_STANDARD's body structure with the three skill shapes

Type: grilling
Status: open
Blocked by: —

## Question

`SKILL_STANDARD.md` prescribes one body structure for every skill: Operating
Posture, Hard Rules, Workflow with per-phase completion criteria, Known Quirks,
Related.

That structure does not fit every skill, and forcing it is actively harmful. The
routing-repair pass classified the corpus into three shapes:

- **Procedure** — has commands that change state (`docker-elite`,
  `zero-downtime-migrations`, `wizard`). The prescribed structure fits.
- **Reference** — states facts an agent reads (`architectural-patterns`,
  `error-codes`, `models`). **There is no workflow.** Demanding one produces
  invented procedure, which is the worst failure mode available here.
- **Judgment flow** — drives an interview or decision loop with no deterministic
  commands (`grilling`, `wayfinder`, `code-review`). Has phases but not commands.

Current state: 54 skills still carry the legacy `🎯 Purpose` / `🛠️ The Process
/ Fact` / `🔗 Related Memories` template, 11 carry the standard's structure,
39 carry neither (mostly the vendored pocock skills, which have their own
coherent shape and are upstream's to change).

Resolve: whether `SKILL_STANDARD.md` grows a per-shape body contract, whether
shape becomes a frontmatter field or stays an authoring judgement, and what the
vendored skills are held to given their bodies are upstream's.

This gates the body rewrite (05) — rewriting 54 bodies against a structure that
is about to change would be wasted work.

## Comments
