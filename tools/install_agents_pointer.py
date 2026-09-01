"""Install a Master Skills pointer into another project's `.agents/` folder.

Antigravity discovers workspace-scoped customizations in `<project>/.agents/`,
so unlike Claude Code's global `~/.claude/CLAUDE.md` there is no single place to
declare the corpus once. Every project that should reach it needs its own
pointer. This writes one.

Usage:
    python tools/install_agents_pointer.py <project-dir> [<project-dir> ...]
    python tools/install_agents_pointer.py --list          # show installed pointers

Writes `<project>/.agents/AGENTS.md`. Refuses to clobber an existing file unless
--force is given; with --force the previous contents are kept alongside as
`AGENTS.md.bak`.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

CORPUS = Path(__file__).resolve().parent.parent
MARKER = "<!-- master-skills-pointer -->"

TEMPLATE = f"""{MARKER}
# Project directives

## Master Skills — consult before answering

A curated corpus of 105 engineering skills lives at:

`{CORPUS}`

It covers backend (Python/Rust/Django/Flask), databases (Postgres/BigQuery/
Redis/migrations), frontend (CSS/JS/XState), infrastructure (Docker/GitHub
Actions/OpenTofu/observability/MCP/agent swarms), testing, git and SRE practice,
document generation, design, fiction writing, plus process flows (TDD, code
review, spec-to-tickets, diagnosing bugs).

**Routing.** `skills_manifest.json` at that path maps ~650 trigger phrases to
skills. Match the task against it, then read the matching `SKILL.md` (or
`<name>.md`) before answering. `SKILL_TREE.md` is the human-readable view.
Read the one or two skills that apply — never the whole corpus.

**Precedence.** These skills outrank training defaults for tooling and standards
choices: uv and ruff over pip and flake8, OpenTofu over Terraform, distroless
base images, UUIDv7 keys, expand-contract migrations. Where a skill and your
prior disagree on the preferred way here, the skill wins.

**Order of consultation:** the corpus first, then web search, then general
knowledge. Do not search the web for something a skill already answers.

**When it does not apply.** Most prompts match nothing, which is fine. Do not
force a skill onto an unrelated task, and do not mention the corpus when nothing
matched.
"""


def install(project: Path, force: bool) -> str:
    if not project.is_dir():
        return f"skip  {project} (not a directory)"

    agents = project / ".agents"
    target = agents / "AGENTS.md"

    if target.exists():
        existing = target.read_text(encoding="utf-8", errors="replace")
        if MARKER in existing:
            target.write_text(TEMPLATE, encoding="utf-8", newline="\n")
            return f"update  {target}"
        if not force:
            return f"SKIP  {target} already exists and is not ours (use --force)"
        shutil.copy2(target, target.with_suffix(".md.bak"))
        target.write_text(TEMPLATE, encoding="utf-8", newline="\n")
        return f"forced  {target} (previous kept as AGENTS.md.bak)"

    agents.mkdir(parents=True, exist_ok=True)
    target.write_text(TEMPLATE, encoding="utf-8", newline="\n")
    return f"create  {target}"


def find_installed(root: Path) -> list[Path]:
    found = []
    for p in root.rglob(".agents/AGENTS.md"):
        try:
            if MARKER in p.read_text(encoding="utf-8", errors="replace"):
                found.append(p)
        except OSError:
            continue
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("projects", nargs="*", type=Path)
    ap.add_argument("--force", action="store_true",
                    help="overwrite a foreign AGENTS.md, keeping a .bak")
    ap.add_argument("--list", action="store_true",
                    help="list pointers already installed under the corpus's parent")
    args = ap.parse_args()

    if args.list:
        for p in find_installed(CORPUS.parent):
            print(p)
        return 0

    if not args.projects:
        ap.print_usage()
        return 2

    for project in args.projects:
        print(install(project.resolve(), args.force))
    return 0


if __name__ == "__main__":
    sys.exit(main())
