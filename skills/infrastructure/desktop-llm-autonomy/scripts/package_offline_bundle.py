"""
Package Desktop LLM Autonomy into a portable, standalone archive.
Can produce a lightweight release (code + bootstrap) or a fully offline bundle (including .venv and .browsers).
"""

import os
import sys
import zipfile
import argparse
from pathlib import Path


def create_bundle(include_binaries: bool = False, output_zip: str = "dist_bundle/desktop-llm-autonomy.zip"):
    skill_dir = Path(__file__).resolve().parent.parent
    out_path = skill_dir / output_zip
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[*] Packaging bundle from: {skill_dir}")
    print(f"[*] Include heavy binaries/browsers: {include_binaries}")

    exclude_dirs = {"__pycache__", ".git", "dist_bundle"}
    if not include_binaries:
        exclude_dirs.add(".venv")
        exclude_dirs.add(".browsers")

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_dir):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if file.endswith(".zip") or file.endswith(".pyc"):
                    continue
                file_path = Path(root) / file
                arc_name = file_path.relative_to(skill_dir)
                print(f"  + Adding {arc_name}")
                zf.write(file_path, arc_name)

    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"\n[+] Bundle created successfully: {out_path} ({size_mb:.2f} MB)")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Package Desktop LLM Autonomy into a portable zip bundle.")
    parser.add_argument(
        "--include-binaries",
        action="store_true",
        help="Include .venv and .browsers directory for 100% offline air-gapped execution (warning: >300MB)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="dist_bundle/desktop-llm-autonomy.zip",
        help="Target zip archive destination"
    )
    args = parser.parse_args()
    create_bundle(include_binaries=args.include_binaries, output_zip=args.output)


if __name__ == "__main__":
    main()
