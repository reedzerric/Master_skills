"""Validation for skill files in the Master Skills framework.

Enforces the hybrid schema defined in SKILL_STANDARD.md: the Agent Skills
contract (`name`, `description`) plus this repository's routing extensions
(`version`, `category`).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

#: The six canonical categories. See SKILL_STANDARD.md.
CANONICAL_CATEGORIES = frozenset({
    "core",
    "game_design",
    "creative_3d",
    "ai_infrastructure",
    "utilities",
    "design_media",
})

#: Fields every skill file must carry.
REQUIRED_FIELDS = ("name", "description", "version", "category")

#: Framework/entry-point docs that describe the system rather than a capability.
NON_SKILL_FILES = frozenset({
    "SKILL_TREE.md",
    "SKILL_STANDARD.md",
    "README.md",
    "agent.md",
    "CLAUDE.md",
    "CORE_MEMORY_PROTOCOL.md",
    "WORKSPACE_INDEX.md",
    "THIRD_PARTY_LICENSES.md",
    "AGENTS.md",
})

#: `.scratch` holds the local-markdown issue tracker (maps, tickets, specs).
#: Those are work artifacts, not skills, and carry no frontmatter.
SKIP_DIRS = frozenset({
    ".git", ".pytest_cache", ".venv", ".templates", "__pycache__", ".scratch",
})

_FRONTMATTER = re.compile(r"\A---\s*$(.*?)^---\s*$", re.DOTALL | re.MULTILINE)
_SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass
class ValidationResult:
    """Outcome of validating one file. Falsy when the file is invalid."""

    path: Path
    valid: bool
    errors: list[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.valid


class MemoryValidator:
    """Validates skill files against the hybrid schema.

    Legacy memory fields (`title`, `confidence_score`, `tags`, `links`) are
    preserved when present but are no longer mandatory — the Agent Skills
    contract replaced them as the required set.
    """

    def validate_file(self, file_path: Path) -> bool:
        """Return True when the file satisfies the schema."""
        return self.check_file(file_path).valid

    def check_file(self, file_path: Path) -> ValidationResult:
        """Validate one file and report every problem found."""
        errors: list[str] = []

        try:
            content = file_path.read_text(encoding="utf-8")
        except OSError as exc:
            return ValidationResult(file_path, False, [f"unreadable: {exc}"])

        match = _FRONTMATTER.match(content)
        if not match:
            return ValidationResult(file_path, False, ["missing YAML frontmatter"])

        try:
            data = yaml.safe_load(match.group(1))
        except yaml.YAMLError as exc:
            return ValidationResult(file_path, False, [f"malformed YAML: {exc}"])

        if not isinstance(data, dict) or not data:
            return ValidationResult(file_path, False, ["empty frontmatter"])

        for required in REQUIRED_FIELDS:
            if required not in data:
                errors.append(f"missing required field: {required}")

        category = data.get("category")
        if category is not None and category not in CANONICAL_CATEGORIES:
            errors.append(
                f"category {category!r} is not one of "
                f"{sorted(CANONICAL_CATEGORIES)}"
            )

        version = data.get("version")
        if version is not None and not _SEMVER.match(str(version)):
            errors.append(f"version {version!r} is not semver (MAJOR.MINOR.PATCH)")

        # `name` must match the filename, or the folder name for SKILL.md.
        name = data.get("name")
        if name:
            expected = (
                file_path.parent.name
                if file_path.name == "SKILL.md"
                else file_path.stem
            )
            if name != expected:
                errors.append(f"name {name!r} does not match path ({expected!r})")

        score = data.get("confidence_score")
        if score is not None and not (0.0 <= float(score) <= 1.0):
            errors.append(f"confidence_score {score!r} outside 0.0-1.0")

        return ValidationResult(file_path, not errors, errors)

    def scan_directory(self, dir_path: Path) -> dict[str, bool]:
        """Validate every skill file under `dir_path`.

        Companion reference files that sit beside a SKILL.md (RECIPES.md,
        *-TEMPLATE.md) are progressive-disclosure payloads, not skills, and
        are not validated.
        """
        return {
            str(path): self.validate_file(path)
            for path in self._skill_files(dir_path)
        }

    def report(self, dir_path: Path) -> list[ValidationResult]:
        """Return a full result per skill file, invalid ones first."""
        results = [self.check_file(p) for p in self._skill_files(dir_path)]
        return sorted(results, key=lambda r: (r.valid, str(r.path)))

    @staticmethod
    def _skill_files(dir_path: Path):
        for path in sorted(dir_path.rglob("*.md")):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.name in NON_SKILL_FILES:
                continue
            if path.name != "SKILL.md" and (path.parent / "SKILL.md").exists():
                continue
            yield path
