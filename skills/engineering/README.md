# Engineering Flows

Process skills: how a piece of work travels from idea to shipped. They answer
*what to do next*. The domain standards elsewhere in `skills/` answer *how to
write it*. Start at [`skill-router`](skill-router/SKILL.md) if you don't know
which applies.

Run [`setup-engineering-flows`](setup-engineering-flows/SKILL.md) once per
repository before using `triage`, `to-spec`, `to-tickets`, `wayfinder`, or
`code-review` — they all read the issue-tracker config it writes.

## The skills

| Skill | Does |
| :--- | :--- |
| [skill-router](skill-router/SKILL.md) | Picks the skill and flow for a situation |
| [setup-engineering-flows](setup-engineering-flows/SKILL.md) | One-time per-repo config: tracker, labels, doc layout |
| [grill-with-docs](grill-with-docs/SKILL.md) | Interview that sharpens a design and writes the ADRs |
| [to-spec](to-spec/SKILL.md) | Conversation → published spec |
| [to-tickets](to-tickets/SKILL.md) | Spec → tracer-bullet tickets with blocking edges |
| [implement](implement/SKILL.md) | Spec or tickets → built, tested, reviewed code |
| [tdd](tdd/SKILL.md) | Red-green-refactor, integration-first |
| [code-review](code-review/SKILL.md) | Two-axis review of a diff: Standards and Spec |
| [diagnosing-bugs](diagnosing-bugs/SKILL.md) | Diagnosis loop for hard bugs and regressions |
| [resolving-merge-conflicts](resolving-merge-conflicts/SKILL.md) | Works a live merge or rebase conflict by intent |
| [triage](triage/SKILL.md) | Incoming issues and PRs → agent-ready briefs |
| [wayfinder](wayfinder/SKILL.md) | Charts work too big for one session as decision tickets |
| [prototype](prototype/SKILL.md) | Throwaway code that answers one design question |
| [research](research/SKILL.md) | Delegated reading against primary sources |
| [domain-modeling](domain-modeling/SKILL.md) | The project's vocabulary: CONTEXT.md and ADRs |
| [codebase-design](codebase-design/SKILL.md) | Deep-module vocabulary for designing one module |
| [improve-codebase-architecture](improve-codebase-architecture/SKILL.md) | Repo-wide sweep for deepening opportunities |
| [wizard](wizard/SKILL.md) | Generates a bash wizard for steps only a human can take |

## Provenance

Imported from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT,
© Matt Pocock). Bodies are upstream; frontmatter was rewritten to this
repository's schema in [`SKILL_STANDARD.md`](../../SKILL_STANDARD.md), which
upstream does not use.

Two skills were adapted rather than copied:

| Upstream | Here | Why |
| :--- | :--- | :--- |
| `ask-matt` | `skill-router` | Routes over this repo's `skills_manifest.json`, not upstream's skill list |
| `setup-matt-pocock-skills` | `setup-engineering-flows` | Name no longer refers to an external repo |

Upstream's `in-progress/` and `misc/` buckets were not imported. To re-sync,
diff bodies against upstream and leave the frontmatter blocks alone.
