# Desktop LLM Autonomy - Zero-Effort Setup Bootstrap (PowerShell)
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host " Desktop LLM Autonomy - Setup Bootstrap" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan

# Set local browser path so binaries live in local folder
$env:PLAYWRIGHT_BROWSERS_PATH = Join-Path $ScriptDir ".browsers"
Write-Host "[*] Local Browser Path: $env:PLAYWRIGHT_BROWSERS_PATH"

$hasUv = Get-Command uv -ErrorAction SilentlyContinue

if ($hasUv) {
    Write-Host "[*] Using uv package manager..." -ForegroundColor Green
    if (-not (Test-Path ".venv")) {
        Write-Host "[*] Creating .venv..."
        uv venv .venv
    }
    Write-Host "[*] Installing dependencies..."
    uv pip install --python .\.venv\Scripts\python.exe -r requirements.txt
    
    Write-Host "[*] Installing Playwright Chromium browser..."
    & .\.venv\Scripts\playwright.exe install chromium
} else {
    Write-Host "[*] Using standard python..." -ForegroundColor Yellow
    if (-not (Test-Path ".venv")) {
        Write-Host "[*] Creating .venv..."
        python -m venv .venv
    }
    Write-Host "[*] Installing dependencies..."
    & .\.venv\Scripts\pip.exe install -r requirements.txt
    
    Write-Host "[*] Installing Playwright Chromium browser..."
    & .\.venv\Scripts\playwright.exe install chromium
}

Write-Host "`n[*] Verifying test suite..." -ForegroundColor Cyan
& .\.venv\Scripts\python.exe scripts\test_harness.py

Write-Host "`n=======================================================" -ForegroundColor Green
Write-Host " Setup Complete! Ready for autonomous agent execution." -ForegroundColor Green
Write-Host "=======================================================" -ForegroundColor Green
