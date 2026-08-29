# Productivity Skills

Thinking and communication skills. Not tied to a codebase — they operate on a
plan, a conversation, or the user's own understanding. Most are user-invoked
(`disable-model-invocation: true`): they run when named, not when guessed at.

## The skills

| Skill | Does |
| :--- | :--- |
| [grilling](grilling/SKILL.md) | The interview primitive: rounds, frontier, facts vs decisions |
| [grill-me](grill-me/SKILL.md) | Stateless grilling, for when there's no repo under you |
| [handoff](handoff/SKILL.md) | Compacts a conversation into a portable handoff document |
| [teach](teach/SKILL.md) | Multi-session learning with mission, glossary, learning record |
| [to-questionnaire](to-questionnaire/SKILL.md) | Turns an unanswerable decision into questions for a human |
| [wait-what](wait-what/SKILL.md) | Re-pitches a message that didn't land |
| [writing-for-agents](writing-for-agents/SKILL.md) | Standards for docs agents read: skills, AGENTS.md, CLAUDE.md |

`grill-with-docs` is the stateful counterpart to `grill-me` and lives in
[`../engineering/`](../engineering/README.md) because it writes into a repo.

## Provenance

Imported from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT,
© Matt Pocock). Bodies are upstream; frontmatter was rewritten to this
repository's schema in [`SKILL_STANDARD.md`](../../SKILL_STANDARD.md).

Note where `writing-for-agents` and `SKILL_STANDARD.md` overlap:
`writing-for-agents` governs the *prose* — what to say and how densely.
`SKILL_STANDARD.md` governs the *frontmatter and section order*. When they
disagree on structure, `SKILL_STANDARD.md` wins, because the validator
enforces it.
