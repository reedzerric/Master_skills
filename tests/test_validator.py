import pytest
import yaml
from pathlib import Path
from memory_validator.validator import MemoryValidator

@pytest.fixture
def mock_memory_file(tmp_path):
    """Fixture to create a temporary memory file."""
    def _create_file(content, filename="test_skill.md"):
        file_path = tmp_path / filename
        file_path.write_text(content, encoding="utf-8")
        return file_path
    return _create_file

def test_validate_valid_file(mock_memory_file):
    """Test that a valid memory file passes validation."""
    content = """---
title: Test Skill
date: 2026-03-08
confidence_score: 1.0
---
# Test Content"""
    file_path = mock_memory_file(content)
    validator = MemoryValidator()
    assert validator.validate_file(file_path) is True

def test_validate_missing_yaml(mock_memory_file):
    """Test that a file missing YAML header fails."""
    content = "# Just Content"
    file_path = mock_memory_file(content)
    validator = MemoryValidator()
    assert validator.validate_file(file_path) is False

def test_validate_missing_confidence_score(mock_memory_file):
    """Test that a file missing confidence_score fails."""
    content = """---
title: Test Skill
date: 2026-03-08
---
# Test Content"""
    file_path = mock_memory_file(content)
    validator = MemoryValidator()
    assert validator.validate_file(file_path) is False
