from pathlib import Path

import pytest

from memory_validator.validator import CANONICAL_CATEGORIES, MemoryValidator

VALID = """---
name: test-skill
description: A test skill. Use when testing the validator.
version: 1.0.0
category: core
triggers: [test]
dependencies: []
inputs: [a file]
outputs: [a result]
confidence_score: 1.0
---
# Test Content
"""


@pytest.fixture
def memory_file(tmp_path):
    """Write `content` to a temp file and return its path."""

    def _create(content: str, filename: str = "test-skill.md") -> Path:
        path = tmp_path / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    return _create


@pytest.fixture
def validator() -> MemoryValidator:
    return MemoryValidator()


def test_valid_file_passes(memory_file, validator):
    assert validator.validate_file(memory_file(VALID)) is True


def test_missing_frontmatter_fails(memory_file, validator):
    result = validator.check_file(memory_file("# Just Content"))
    assert not result
    assert "missing YAML frontmatter" in result.errors


def test_malformed_yaml_fails(memory_file, validator):
    content = "---\nname: [unclosed\n---\n# Body\n"
    assert validator.validate_file(memory_file(content)) is False


@pytest.mark.parametrize("field", ["name", "description", "version", "category"])
def test_each_required_field_is_enforced(memory_file, validator, field):
    stripped = "\n".join(
        line for line in VALID.splitlines() if not line.startswith(f"{field}:")
    )
    result = validator.check_file(memory_file(stripped + "\n"))
    assert not result
    assert any(field in err for err in result.errors)


def test_non_canonical_category_fails(memory_file, validator):
    content = VALID.replace("category: core", "category: backend")
    result = validator.check_file(memory_file(content))
    assert not result
    assert any("not one of" in err for err in result.errors)


@pytest.mark.parametrize("category", sorted(CANONICAL_CATEGORIES))
def test_every_canonical_category_is_accepted(memory_file, validator, category):
    content = VALID.replace("category: core", f"category: {category}")
    assert validator.validate_file(memory_file(content)) is True


def test_non_semver_version_fails(memory_file, validator):
    content = VALID.replace("version: 1.0.0", "version: v1")
    result = validator.check_file(memory_file(content))
    assert not result
    assert any("semver" in err for err in result.errors)


def test_name_must_match_filename(memory_file, validator):
    path = memory_file(VALID, filename="different-name.md")
    result = validator.check_file(path)
    assert not result
    assert any("does not match path" in err for err in result.errors)


def test_name_matches_folder_for_skill_md(memory_file, validator):
    path = memory_file(VALID, filename="test-skill/SKILL.md")
    assert validator.validate_file(path) is True


def test_out_of_range_confidence_score_fails(memory_file, validator):
    content = VALID.replace("confidence_score: 1.0", "confidence_score: 1.5")
    assert validator.validate_file(memory_file(content)) is False


def test_legacy_fields_are_optional(memory_file, validator):
    """`title` and `confidence_score` are preserved but no longer mandatory."""
    stripped = "\n".join(
        line for line in VALID.splitlines()
        if not line.startswith("confidence_score:")
    )
    assert validator.validate_file(memory_file(stripped + "\n")) is True


def test_scan_skips_companion_reference_files(tmp_path, validator):
    skill_dir = tmp_path / "test-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(VALID, encoding="utf-8")
    (skill_dir / "RECIPES.md").write_text("# Recipes\n", encoding="utf-8")

    results = validator.scan_directory(tmp_path)

    assert len(results) == 1
    assert all(results.values())


def test_scan_skips_framework_docs(tmp_path, validator):
    (tmp_path / "test-skill.md").write_text(VALID, encoding="utf-8")
    (tmp_path / "WORKSPACE_INDEX.md").write_text("# Index\n", encoding="utf-8")

    assert len(validator.scan_directory(tmp_path)) == 1


def test_report_sorts_invalid_first(tmp_path, validator):
    (tmp_path / "test-skill.md").write_text(VALID, encoding="utf-8")
    (tmp_path / "broken.md").write_text("# no frontmatter\n", encoding="utf-8")

    report = validator.report(tmp_path)

    assert not report[0].valid
    assert report[0].path.name == "broken.md"


def test_repository_is_valid():
    """Every skill file in this repository satisfies the schema."""
    root = Path(__file__).resolve().parent.parent
    failures = [r for r in MemoryValidator().report(root) if not r.valid]
    assert not failures, "\n".join(
        f"{r.path}: {'; '.join(r.errors)}" for r in failures
    )
