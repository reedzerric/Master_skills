@echo off
setlocal enabledelayedexpansion

echo =======================================================
echo  Desktop LLM Autonomy - Zero-Effort Setup Bootstrap
echo =======================================================

cd /d "%~dp0"

REM 1. Set local portable browser storage (keeps binaries inside folder, not global AppData)
set "PLAYWRIGHT_BROWSERS_PATH=%~dp0.browsers"
echo [*] Local Browser Storage: %PLAYWRIGHT_BROWSERS_PATH%

REM 2. Detect uv or python
where uv >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [*] Using uv fast package manager...
    if not exist ".venv" (
        echo [*] Creating virtual environment...
        uv venv .venv
    )
    echo [*] Installing dependencies from requirements.txt...
    uv pip install --python .venv\Scripts\python.exe -r requirements.txt
    
    echo [*] Installing Playwright Chromium browser binary...
    .venv\Scripts\playwright.exe install chromium
) else (
    echo [*] uv not found, falling back to python...
    if not exist ".venv" (
        echo [*] Creating virtual environment...
        python -m venv .venv
    )
    echo [*] Installing dependencies from requirements.txt...
    .venv\Scripts\pip.exe install -r requirements.txt
    
    echo [*] Installing Playwright Chromium browser binary...
    .venv\Scripts\playwright.exe install chromium
)

echo.
echo [*] Running verification test harness...
.venv\Scripts\python.exe scripts\test_harness.py

echo.
echo =======================================================
echo  Setup Complete!
echo  To run the agent:
echo    .venv\Scripts\python.exe scripts\run_agent.py --mode browser --goal "Your objective"
echo =======================================================
