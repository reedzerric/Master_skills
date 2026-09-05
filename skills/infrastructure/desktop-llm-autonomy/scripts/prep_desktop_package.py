"""
Prepares the complete FIDO_OFFLINE_PACKAGE directory on Desktop with:
1. Single complete full zip
2. Standard sub-15MB email split chunks + 1-click batch reconstructor
3. Strict-firewall email chunks (.dat) + 1-click PowerShell reconstructor
4. Instructions text file
"""

import os
import shutil
import hashlib
from pathlib import Path

DESKTOP = Path(r"C:\Users\reedz\OneDrive\Desktop")
PACKAGE_DIR = DESKTOP / "FIDO_OFFLINE_PACKAGE"
SRC_DIR = Path(r"C:\Users\reedz\OneDrive\Documents\Automation\MM\Python\Master_skills\skills\infrastructure\desktop-llm-autonomy\dist_email_chunks")
FULL_ZIP = SRC_DIR / "fido_offline_bundle.zip"

PACKAGE_DIR.mkdir(parents=True, exist_ok=True)

# 1. Full single zip
shutil.copy2(FULL_ZIP, PACKAGE_DIR / "fido_full_bundle.zip")

# 2. Folder 1: Standard Split Chunks for Email
split_dir = PACKAGE_DIR / "1_SPLIT_CHUNKS_FOR_EMAIL"
split_dir.mkdir(exist_ok=True)
for p in SRC_DIR.glob("fido_bundle.part*"):
    shutil.copy2(p, split_dir / p.name)
shutil.copy2(SRC_DIR / "rejoin_and_unpack.bat", split_dir / "rejoin_and_unpack.bat")
shutil.copy2(SRC_DIR / "rejoin_and_unpack.ps1", split_dir / "rejoin_and_unpack.ps1")

# 3. Folder 2: Obfuscated DAT files for strict email filters (e.g. Gmail / corporate scanners)
dat_dir = PACKAGE_DIR / "2_OBFUSCATED_DAT_FOR_STRICT_EMAIL"
dat_dir.mkdir(exist_ok=True)
for p in SRC_DIR.glob("fido_part*.dat"):
    shutil.copy2(p, dat_dir / p.name)

# Create unmask & unpack script in dat_dir
unmask_ps1 = dat_dir / "unmask_and_unpack.ps1"
with open(unmask_ps1, "w") as f:
    f.write("""# Auto-recombine and unmask Fido package
Write-Host "[*] Recombining and unmasking parts..." -ForegroundColor Cyan
$key = 0xAA
$outFile = "fido_offline_bundle.zip"
$fs = [System.IO.File]::Create($outFile)

Get-ChildItem -Filter "fido_part*.dat" | Sort-Object Name | ForEach-Object {
    Write-Host "  + Processing $($_.Name)..."
    $bytes = [System.IO.File]::ReadAllBytes($_.FullName)
    for ($i = 0; $i -lt $bytes.Length; $i++) {
        $bytes[$i] = $bytes[$i] -bxor $key
    }
    $fs.Write($bytes, 0, $bytes.Length)
}
$fs.Close()

Write-Host "[*] Extracting package..." -ForegroundColor Cyan
tar -xf $outFile
Write-Host "[+] Complete! You can now run setup.bat or tools\\fido.bat" -ForegroundColor Green
""")

unmask_bat = dat_dir / "unmask_and_unpack.bat"
with open(unmask_bat, "w") as f:
    f.write("""@echo off
powershell -ExecutionPolicy Bypass -File "%~dp0unmask_and_unpack.ps1"
pause
""")

# 4. Instructions
instructions = PACKAGE_DIR / "HOW_TO_USE.txt"
with open(instructions, "w") as f:
    f.write("""========================================================================
FIDO OFFLINE STANDALONE PACKAGE
========================================================================

OPTION A: SEND VIA GOOGLE DRIVE / ONEDRIVE
- Send "fido_full_bundle.zip" directly as a cloud link.
- On recipient machine: Right-click -> Extract All, then run setup.bat.

OPTION B: SEND VIA EMAIL (Standard Attachments)
- Use files inside "1_SPLIT_CHUNKS_FOR_EMAIL":
    Email 1: fido_bundle.part01 + rejoin_and_unpack.bat
    Email 2: fido_bundle.part02
    Email 3: fido_bundle.part03
    Email 4: fido_bundle.part04
- On recipient machine: Put all parts in one folder and double-click:
    rejoin_and_unpack.bat

OPTION C: STRICT EMAIL FILTERS (If Gmail/Outlook blocks zip headers)
- Use files inside "2_OBFUSCATED_DAT_FOR_STRICT_EMAIL":
    Email 1: fido_part01.dat + unmask_and_unpack.bat
    Email 2: fido_part02.dat
    Email 3: fido_part03.dat
    Email 4: fido_part04.dat
- On recipient machine: Put all parts in one folder and double-click:
    unmask_and_unpack.bat

========================================================================
AFTER EXTRACTING:
- Run tools\\fido.bat "<your objective>"
- Or setup.bat for local python virtual environment
========================================================================
""")

print(f"[+] All files prepared on Desktop: {PACKAGE_DIR}")
