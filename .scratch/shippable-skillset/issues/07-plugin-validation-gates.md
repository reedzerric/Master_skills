# 07 — Extend the gates to cover the plugin surface

Type: task
Status: open
Blocked by: 02, 03

## Question

Nothing to decide once 02 and 03 land — this makes the packaging non-regressable.

The existing suite validates frontmatter against `SKILL_STANDARD.md`. It knows
nothing about the plugin. Add checks so a broken package fails the pre-commit
hook rather than a stranger's install:

- Every path listed in `.claude-plugin/plugin.json` exists and contains a
  `SKILL.md`.
- Every shipped skill's `name` matches its directory name.
- No shipped skill's `description` exceeds the runtime limit found in 02.
- `marketplace.json` and `plugin.json` agree with each other and parse.
- The shipped set's total description budget is reported, and optionally capped,
  so the cost from 01 cannot silently creep back up.
- Nothing ships that links to a companion or skill that does not ship.

Wire into `tools/hooks/pre-commit` alongside the manifest rebuild and pytest.

## Comments
