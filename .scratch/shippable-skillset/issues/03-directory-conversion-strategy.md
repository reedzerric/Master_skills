# 03 — How do 76 single-file skills become directories?

Type: grilling
Status: open
Blocked by: 02

## Question

76 of 104 skills are `<category>/<name>.md`. If 02 confirms the runtime requires
`<name>/SKILL.md`, they must all become directories. Decide the strategy.

Scope is settled by 01: everything ships, so all 76 convert. The "only the
shipped set" option below is discharged.

The rename is not local. It moves:

- `path` in every `skills_manifest.json` entry
- the `name`-matches-path rule the validator enforces
  (`validator.py` already handles both shapes, so this is safe, but it must be
  re-verified per file)
- relative links between companion files
- anything in `WORKSPACE_INDEX.md`, `SKILL_TREE.md` or `CLAUDE.md` naming a path

Open sub-decisions:

- Does the directory layout keep the current category folders
  (`skills/backend/python-elite/SKILL.md`) or flatten to match upstream
  (`skills/python-elite/SKILL.md`)? Category is already carried in frontmatter,
  so the folder is redundant for routing but useful for humans.
- `git mv` per file, or a script? A script is faster and reviewable; `git mv`
  preserves rename detection in history.
- Whether to fold in the `security-agentic-elite` / `agentic-security-elite`
  rename while every path is moving anyway (currently in the map's fog).

Resolve: scope of conversion, target layout, mechanism, and the order that keeps
gates green throughout.

## Comments
