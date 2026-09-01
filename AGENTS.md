# AGENTS.md

Cross-tool entry point for this repository. Read by Antigravity, Cursor, Codex,
Copilot and others; Claude Code reads `CLAUDE.md`, which carries the same
routing rules plus graphify-specific guidance.

## What this repository is

A corpus of 105 agent skills — reusable engineering standards and process
workflows — plus the tooling that validates and routes them. It is not an
application. The deliverable is the skill files themselves.

## Routing: find the skill before you answer

1. Parse `skills_manifest.json`. Its `trigger_index` maps ~650 natural
   phrases to skill names; its `skills` array carries every skill's path,
   description, inputs and outputs.
2. Read the matching `SKILL.md` (multi-file skills) or `<name>.md` (single-file
   skills) before answering.
3. `SKILL_TREE.md` is the human-readable view of the same data.

**Do not read the whole corpus.** It is ~36 KB of descriptions alone. Route to
the one or two skills that apply.

Skills marked with a `companions` list keep bulk reference material in sibling
files (`RECIPES.md`, `BENCHMARKS.md`, `STANDARDS.md`). Load `SKILL.md` first;
pull in a companion only when the workflow says to.

## Precedence

These skills outrank training defaults for this user's tooling and standards
choices — uv and ruff over pip and flake8, OpenTofu over Terraform, distroless
base images, UUIDv7 keys, expand-contract migrations. If a skill and your prior
disagree on the preferred way here, the skill wins.

Consult the corpus first, then web search, then general knowledge.

## Editing a skill

Every skill conforms to `SKILL_STANDARD.md`. Required frontmatter is `name`,
`description`, `version`, `category`; `category` must be one of `core`,
`game_design`, `creative_3d`, `ai_infrastructure`, `utilities`, `design_media`.

Three constraints that are easy to violate and hard to notice:

- **Frontmatter lists must be flow style** — `triggers: [a, b]`, never a block
  list. `tools/build_manifest.py` parses frontmatter by regex, not YAML, and
  silently folds a block list into one string.
- **`name` must match the path** — `<dir>/<name>.md`, or the folder name for
  `SKILL.md`. A mismatch breaks routing without erroring.
- **`links` take a skill name, never a path** — `[[python-elite]]` resolves,
  `[[skills/backend/python-elite]]` does not. Links to framework docs
  (`[[SKILL_TREE]]`, `[[WORKSPACE_INDEX]]`) legitimately do not resolve.

Triggers are what a *user says* ("my migration locked the table"); tags are what
the file *is about* (`postgres`, `ddl`). Single-word triggers are almost always
tags in disguise and will collide across a dozen skills.

## Gates — both must pass before committing

```bash
python tools/build_manifest.py   # regenerate routing map; must report no dangling dependencies
uv run pytest tests/             # 46 tests, incl. a repo-wide schema check
```

The pre-commit hook runs both. Install once per clone:

```bash
git config core.hooksPath tools/hooks
```

A stale `skills_manifest.json` routes agents to paths that no longer exist, so
regenerate it after adding, renaming, or re-triggering any skill.

## Known rough edges

- **The dependency graph has 9 cycles** (`claude-api` ↔ `models`,
  `docker-elite` ↔ `github-actions-elite`, `python-elite` ↔ `flask-elite`, and
  six more) plus some nonsense edges. `SKILL_STANDARD.md` claims the manifest
  builder rejects cycles; it contains no cycle check. Treat `dependencies` as
  unreliable until audited.
- **54 skills still carry a legacy body template** (`🎯 Purpose` /
  `🛠️ The Process / Fact`) rather than the structure `SKILL_STANDARD.md`
  prescribes. Frontmatter is conformant corpus-wide; bodies are not yet.
- `skills/engineering/` and `skills/productivity/` are vendored from
  mattpocock/skills under MIT. **Bodies are upstream — do not rewrite them.**
  Frontmatter is local. See `THIRD_PARTY_LICENSES.md`.

## Planning artifacts

`.scratch/` holds the local-markdown issue tracker used by the `wayfinder`
skill — maps and decision tickets, not skills. Both the validator and the
manifest builder skip it.
