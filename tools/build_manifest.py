"""Build skills_manifest.json from the frontmatter of every skill file.

Scans Master_skills for `*.md` carrying the hybrid schema, emits a machine-
readable routing map, and reports any file that fails validation.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "skills_manifest.json"

SKIP_DIRS = {
    ".git", ".pytest_cache", ".venv", ".templates", "__pycache__", ".scratch",
}
SKIP_FILES = {
    "SKILL_TREE.md",
    "README.md",
    "agent.md",
    "CLAUDE.md",
    "CORE_MEMORY_PROTOCOL.md",
    "WORKSPACE_INDEX.md",
    "THIRD_PARTY_LICENSES.md",
}

CANONICAL = {
    "core",
    "game_design",
    "creative_3d",
    "ai_infrastructure",
    "utilities",
    "design_media",
}

FM = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def parse_fm(text: str) -> dict[str, str]:
    m = FM.match(text)
    if not m:
        return {}
    fields: dict[str, str] = {}
    key = None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if km:
            key = km.group(1)
            fields[key] = km.group(2).strip()
        elif key and line.strip():
            fields[key] += " " + line.strip()
    return fields


def as_list(value: str) -> list[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [p.strip().strip("\"'") for p in value.split(",") if p.strip()]


def main() -> None:
    entries: list[dict] = []
    problems: list[str] = []

    for path in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        # Companion reference files (RECIPES.md, *-TEMPLATE.md) are not skills.
        if path.name != "SKILL.md" and path.parent.joinpath("SKILL.md").exists():
            continue

        fm = parse_fm(path.read_text(encoding="utf-8"))
        rel = path.relative_to(ROOT).as_posix()

        if not fm.get("name"):
            problems.append(f"{rel}: missing `name`")
            continue
        category = fm.get("category", "")
        if category not in CANONICAL:
            problems.append(f"{rel}: category {category!r} not canonical")

        companions = []
        if path.name == "SKILL.md":
            companions = sorted(
                p.name for p in path.parent.glob("*.md") if p.name != "SKILL.md"
            )

        entries.append({
            "name": fm["name"],
            "path": rel,
            "category": category,
            "version": fm.get("version", "0.0.0"),
            "description": fm.get("description", ""),
            "triggers": as_list(fm.get("triggers", "")),
            "dependencies": as_list(fm.get("dependencies", "")),
            "inputs": as_list(fm.get("inputs", "")),
            "outputs": as_list(fm.get("outputs", "")),
            "tags": as_list(fm.get("tags", "")),
            "companions": companions,
        })

    # Dependency edges that point at nothing are dangling, not fatal.
    known = {e["name"] for e in entries}
    dangling = sorted({
        d for e in entries for d in e["dependencies"] if d not in known
    })

    by_category: dict[str, list[str]] = defaultdict(list)
    for e in entries:
        by_category[e["category"]].append(e["name"])

    trigger_index: dict[str, list[str]] = defaultdict(list)
    for e in entries:
        for t in e["triggers"]:
            trigger_index[t].append(e["name"])

    manifest = {
        "schema_version": "1.0.0",
        "generated": date.today().isoformat(),
        "repository": "Master_skills",
        "categories": {k: sorted(v) for k, v in sorted(by_category.items())},
        "skills": sorted(entries, key=lambda e: (e["category"], e["name"])),
        "trigger_index": {k: sorted(v) for k, v in sorted(trigger_index.items())},
        "dangling_dependencies": dangling,
    }

    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"{len(entries)} skills -> {OUT.name}")
    for cat, names in sorted(by_category.items()):
        print(f"  {cat:20} {len(names)}")
    if dangling:
        print(f"\ndangling dependencies ({len(dangling)}): {', '.join(dangling)}")
    if problems:
        print(f"\nvalidation problems ({len(problems)}):")
        for p in problems:
            print(f"  {p}")


if __name__ == "__main__":
    main()
