# Master Skills — workspace directives

You are working inside the Master Skills corpus itself: 105 agent skills plus
the tooling that validates and routes them.

Full contributor guidance is in [`../AGENTS.md`](../AGENTS.md) at the repository
root — routing rules, the frontmatter constraints that fail silently, the two
gates, and the known rough edges. Read it before editing any skill.

## The short version

- **Route via `skills_manifest.json`.** Its `trigger_index` maps ~650 phrases to
  skills. Read the one or two that match; never read the whole corpus.
- **Gates before committing:** `python tools/build_manifest.py` (no dangling
  dependencies) and `uv run pytest tests/` (46 tests).
- **Frontmatter lists must be flow style** — `triggers: [a, b]`. The manifest
  builder parses by regex, not YAML, and silently mangles block lists.
- `skills/engineering/` and `skills/productivity/` are vendored from
  mattpocock/skills under MIT. Bodies are upstream; do not rewrite them.
