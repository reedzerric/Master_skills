"""
Builds an offline self-contained bundle of desktop-llm-autonomy (code + site-packages)
and splits it into email-safe chunks (<15MB each) with an auto-rejoin script.
"""

import os
import sys
import hashlib
import zipfile
import shutil
from pathlib import Path

# Paths
SKILL_ROOT = Path(r"C:\Users\reedz\OneDrive\Documents\Automation\MM\Python\Master_skills\skills\infrastructure\desktop-llm-autonomy")
SITE_PACKAGES = Path(r"C:\Users\reedz\OneDrive\Documents\Automation\MM\Python\Master_skills\.venv\Lib\site-packages")
OUTPUT_DIR = SKILL_ROOT / "dist_email_chunks"
BUNDLE_ZIP = OUTPUT_DIR / "fido_offline_bundle.zip"

CHUNK_SIZE = 14 * 1024 * 1024  # 14 MB (well under 20MB / 25MB MIME limits)

PACKAGES_TO_INCLUDE = [
    "playwright",
    "pyautogui",
    "PIL",
    "mss",
    "pygetwindow",
    "pyrect",
    "pyscreeze",
    "pytweening",
    "mouseinfo",
]


def sha256_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def build_bundle():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    # Clean previous chunks if any
    for p in OUTPUT_DIR.glob("*"):
        if p.is_file():
            p.unlink()

    print("[*] Creating offline bundle zip...")
    with zipfile.ZipFile(BUNDLE_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. Add skill code and scripts
        for root, dirs, files in os.walk(SKILL_ROOT):
            dirs[:] = [d for d in dirs if d not in {"__pycache__", ".git", "dist_bundle", "dist_email_chunks", ".venv", ".browsers"}]
            for file in files:
                if file.endswith((".zip", ".pyc", ".part", ".tmp")):
                    continue
                fp = Path(root) / file
                arcname = fp.relative_to(SKILL_ROOT)
                zf.write(fp, arcname)

        # 2. Add Fido tools
        tools_dir = SKILL_ROOT.parent.parent.parent / "tools"
        if (tools_dir / "fido.py").exists():
            zf.write(tools_dir / "fido.py", "tools/fido.py")
        if (tools_dir / "fido.bat").exists():
            zf.write(tools_dir / "fido.bat", "tools/fido.bat")

        # 3. Add offline Python packages into packages/ directory inside zip
        print("[*] Bundling pre-installed Python packages...")
        for pkg in PACKAGES_TO_INCLUDE:
            pkg_path = SITE_PACKAGES / pkg
            if pkg_path.is_dir():
                for root, dirs, files in os.walk(pkg_path):
                    dirs[:] = [d for d in dirs if d != "__pycache__"]
                    for file in files:
                        fp = Path(root) / file
                        arcname = Path("site_packages") / fp.relative_to(SITE_PACKAGES)
                        zf.write(fp, arcname)
            elif (SITE_PACKAGES / f"{pkg}.py").exists():
                fp = SITE_PACKAGES / f"{pkg}.py"
                zf.write(fp, Path("site_packages") / fp.name)

            # Include dist-info metadata
            for dist_info in SITE_PACKAGES.glob(f"{pkg}*.dist-info"):
                for root, dirs, files in os.walk(dist_info):
                    for file in files:
                        fp = Path(root) / file
                        arcname = Path("site_packages") / fp.relative_to(SITE_PACKAGES)
                        zf.write(fp, arcname)

    orig_size_mb = BUNDLE_ZIP.stat().st_size / (1024 * 1024)
    orig_sha = sha256_file(BUNDLE_ZIP)
    print(f"[+] Bundle created: {BUNDLE_ZIP.name} ({orig_size_mb:.2f} MB)")
    print(f"[+] Original SHA256: {orig_sha}")

    # 4. Split into chunks
    print(f"[*] Splitting into <= {CHUNK_SIZE // (1024*1024)} MB chunks...")
    chunks = []
    with open(BUNDLE_ZIP, "rb") as f:
        idx = 1
        while True:
            data = f.read(CHUNK_SIZE)
            if not data:
                break
            chunk_name = f"fido_bundle.part{idx:02d}"
            chunk_path = OUTPUT_DIR / chunk_name
            with open(chunk_path, "wb") as cf:
                cf.write(data)
            chunk_mb = chunk_path.stat().st_size / (1024 * 1024)
            print(f"  + Generated {chunk_name} ({chunk_mb:.2f} MB)")
            chunks.append(chunk_path)
            idx += 1

    # 5. Generate 1-click Rejoin script (Batch)
    rejoin_bat = OUTPUT_DIR / "rejoin_and_unpack.bat"
    with open(rejoin_bat, "w") as f:
        f.write("@echo off\n")
        f.write("echo [*] Rejoining Fido split archive...\n")
        f.write("copy /b fido_bundle.part* fido_offline_bundle.zip\n")
        f.write("if not exist fido_offline_bundle.zip (\n")
        f.write("    echo [!] Error: Failed to reassemble fido_offline_bundle.zip\n")
        f.write("    pause\n")
        f.write("    exit /b 1\n")
        f.write(")\n")
        f.write("echo [*] Extracting fido_offline_bundle.zip...\n")
        f.write("tar -xf fido_offline_bundle.zip\n")
        f.write("echo [!] Setup complete! You can now run setup.bat or tools\\fido.bat\n")
        f.write("pause\n")

    # 6. Generate 1-click Rejoin script (PowerShell)
    rejoin_ps1 = OUTPUT_DIR / "rejoin_and_unpack.ps1"
    with open(rejoin_ps1, "w") as f:
        f.write("Write-Host '[*] Rejoining Fido split archive...' -ForegroundColor Cyan\n")
        f.write("cmd.exe /c 'copy /b fido_bundle.part* fido_offline_bundle.zip'\n")
        f.write("Write-Host '[*] Extracting fido_offline_bundle.zip...' -ForegroundColor Cyan\n")
        f.write("Expand-Archive -Path 'fido_offline_bundle.zip' -DestinationPath '.' -Force\n")
        f.write("Write-Host '[+] Successfully unpacked!' -ForegroundColor Green\n")

    # 7. Verification: Reassemble and verify hash match
    test_reassemble = OUTPUT_DIR / "verify_reassembly.tmp"
    with open(test_reassemble, "wb") as out_f:
        for c in chunks:
            with open(c, "rb") as in_f:
                out_f.write(in_f.read())
    reass_sha = sha256_file(test_reassemble)
    test_reassemble.unlink()

    assert reass_sha == orig_sha, "Checksum mismatch on split reassembly!"
    print(f"[+] Verification SUCCESS: Split chunks reassemble bit-for-bit identical to original.")
    print(f"[+] Files ready in: {OUTPUT_DIR}")

    return {
        "output_dir": str(OUTPUT_DIR),
        "total_mb": orig_size_mb,
        "chunks": [c.name for c in chunks],
        "chunk_count": len(chunks),
        "sha256": orig_sha
    }


if __name__ == "__main__":
    build_bundle()
