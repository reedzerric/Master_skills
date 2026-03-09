import yaml
import re
from pathlib import Path
from typing import Optional

class MemoryValidator:
    """
    Validates the integrity of memory files in the 'Master Skills' framework.
    Ensures YAML headers and mandatory fields like 'confidence_score' are present.
    """

    def validate_file(self, file_path: Path) -> bool:
        """
        Validates a single markdown file for elite memory standards.
        """
        try:
            content = file_path.read_text(encoding="utf-8")
            
            # Extract YAML header using regex
            match = re.search(r"^---(.*?)---", content, re.DOTALL | re.MULTILINE)
            if not match:
                return False
            
            yaml_content = match.group(1)
            data = yaml.safe_load(yaml_content)
            
            if not data:
                return False
            
            # Check for mandatory elite fields
            mandatory_fields = ["confidence_score", "title"]
            for field in mandatory_fields:
                if field not in data:
                    return False
            
            return True
            
        except (yaml.YAMLError, OSError):
            return False

    def scan_directory(self, dir_path: Path) -> dict[str, bool]:
        """
        Scans a directory recursively and validates all .md files.
        """
        results = {}
        for md_file in dir_path.rglob("*.md"):
            results[str(md_file)] = self.validate_file(md_file)
        return results
