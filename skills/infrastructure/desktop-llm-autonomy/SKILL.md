---
name: desktop-llm-autonomy
description: 'Autonomous computer-use and desktop action harness for any LLM (OpenAI, Gemini, Anthropic, Ollama) on Windows and macOS. Combines Playwright/browser-use DOM navigation with PyAutoGUI OS-level vision-action loops, safety confirmation gates, coordinate validation, and multi-model dispatch. Use when the user asks to give an LLM autonomy to take actions, automate desktop tasks, navigate web applications, click/type on their behalf, or build an autonomous computer-use agent. For building pure MCP servers without GUI control, use mcp-builder instead.'
version: 1.0.0
category: ai_infrastructure
triggers: [enable llm computer use, desktop autonomy for llm, give agent autonomy to take action, automate desktop with llm, browser-use agent, multi-llm computer use, autonomous desktop agent, desktop actions on my behalf, claude cowork alternative]
dependencies: [mcp-builder]
inputs: [task goal, target application or web URL, model provider credentials or local endpoint]
outputs: [executed desktop/browser action, execution history log, screenshot trajectory, completion status]
tags: [agent, automation, computer-use, browser-use, pyautogui, desktop, autonomy, vision-action]
links: ['[[mcp-builder]]', '[[agent-swarms-elite]]', '[[agent-handoff-elite]]']
confidence_score: 1.0
date: '2026-09-04'
task_ref: desktop-llm-autonomy-harness
---

# Desktop & Computer-Use LLM Autonomy

Enable any LLM (OpenAI, Anthropic, Gemini, local Ollama) to autonomously observe, navigate, and take actions on a computer on behalf of the user.

It does ONE thing: provide a robust dual-mode execution harness (Browser DOM + Desktop OS vision loop) with safety guardrails that allows models to drive desktop workflows. It does not build passive API-only MCP servers without UI execution (that is `mcp-builder`), and it does not coordinate multi-agent swarm handoffs without computer use (that is `agent-swarms-elite`).

## Operating Posture

Assume the agent has physical agency over the user's desktop. Every action (mouse click, keyboard stroke, form submission, page navigation) has real-world consequences. Prioritize determinism and safety above all:
1. **Never use pixels when DOM or APIs exist.** Browser DOM navigation via Playwright is 10x faster, resilient to screen resolution/scaling differences, and works headless.
2. **Enforce hard safety gates.** Block destructive commands (`format`, `rmdir /s`, credential tampering) and cap total execution steps.
3. **Respect user control.** Mouse movement to the top-left corner must trigger an immediate fail-safe abort.

## Hard Rules

1. **Hierarchy of Action:**
   - **Tier 1 (Direct API / MCP):** If an API or CLI command exists for the task, execute it directly.
   - **Tier 2 (Browser DOM):** If the task involves a web app, use Playwright / `browser-use` DOM locators and text extraction.
   - **Tier 3 (Desktop Vision GUI):** Use OS-level screenshot + click/type (`pyautogui`) strictly as a fallback for native legacy apps lacking accessible interfaces.
2. **Never click without bounds validation.** Screen coordinates must be strictly checked against active monitor dimensions.
3. **Fail-Safe Avoidance:** Never programmatically click in the (0-15px, 0-15px) corner; that zone is reserved for emergency human abort.
4. **Step Budget Limit:** Every autonomous session must have a hard `max_steps` threshold (default 15–25) to prevent infinite loops or token exhaustion.
5. **Handle Lock Screen Gracefully:** Windows GDI screenshot captures (`BitBlt`) fail when the workstation is locked or display is asleep. Headless browser automation continues to function regardless of lock state.

## Architecture

```
                       User Goal / Objective
                                │
                 ┌──────────────▼──────────────┐
                 │    Multi-LLM Dispatcher     │
                 │ (OpenAI / Claude / Gemini)  │
                 └──────────────┬──────────────┘
                                │
                   Decision (Thought + Action)
                                │
                 ┌──────────────▼──────────────┐
                 │     Safety Guardrails       │
                 │  - Bounds & Fail-safe Check │
                 │  - Command Blocklist Filter │
                 │  - Step Budget Tracker      │
                 └──────────────┬──────────────┘
                                │
          ┌─────────────────────┴─────────────────────┐
          │                                           │
┌─────────▼─────────┐                       ┌─────────▼─────────┐
│   Browser Engine  │                       │   Desktop Engine  │
│ (Playwright DOM)  │                       │  (PyAutoGUI GUI)  │
│ - Selector Click  │                       │ - Screen Capture  │
│ - Text Fill       │                       │ - Coord Click     │
│ - DOM Extraction  │                       │ - Keystroke Type  │
└───────────────────┘                       └───────────────────┘
```

## Workflow

### Phase 1 — Route Execution Mode
Identify target environment:
- Web dashboard, SaaS, online form, search -> **Browser Engine** (`mode="browser"`).
- Native desktop app (Notepad, Excel, File Explorer, settings) -> **Desktop Engine** (`mode="desktop"`).

### Phase 2 — State Observation
- **Browser:** Extract interactive element hierarchy (`get_interactive_elements()`) and visible text snippet (`extract_visible_text()`).
- **Desktop:** Capture screen buffer (`capture_screen()`), optionally superimposing a 10x10 spatial grid to assist vision models with coordinate calibration.

### Phase 3 — Action Generation & Guardrails
- Dispatch state to LLM with structured JSON schema:
  ```json
  {
    "thought": "Reasoning for the action",
    "action": "click" | "type_text" | "press_key" | "navigate" | "finish",
    "params": { ... }
  }
  ```
- Pass proposed action through `SafetyGuard`:
  - Verify coordinates `(x, y)` are within display bounds.
  - Scan input text against destructive pattern regexes.
  - Increment step budget counter.

### Phase 4 — Execution & Verification
- Execute action through the target engine.
- Re-observe state on next turn to confirm the UI changed as expected.
- If objective satisfied, agent emits `action="finish"` with a concise result summary.

## Multi-Model Integration

The companion runner supports seamless model swapping:
- **Anthropic Claude:** `claude-3-5-sonnet-20241022` or `claude-3-7-sonnet` (exceptional computer-use spatial reasoning).
- **OpenAI:** `gpt-4o` or `gpt-4o-mini` (strong structured JSON adherence).
- **Google Gemini:** `gemini-2.0-flash` (ultra-fast latency for high-frequency loops).
- **Local Ollama:** `llama3.2-vision` or `qwen2.5-coder` (private local execution).

## Windows Quirks & Failure Modes

1. **Desktop Lock / Sleep:**
   - On Windows, `GetForegroundWindow() == 0` when the workstation is locked.
   - GDI `BitBlt` with `CAPTUREBLT` throws an `OSError: screen grab failed`.
   - **Mitigation:** Detect `is_desktop_locked()` early; prefer headless browser runs when unattended.
2. **Virtual Desktop & Sandbox Isolation (`WinSta0\Default`):**
   - Background runners, daemons, or CLI assistants often execute child processes on isolated virtual desktops (e.g. `exebox-...`), causing GUI windows to render invisibly.
   - **Fix:** Attach the execution thread to the interactive user desktop and specify `STARTUPINFO.lpDesktop = r"WinSta0\Default"` in `CreateProcessW`:
     ```python
     hdesk = ctypes.windll.user32.OpenDesktopW("Default", 0, False, 0x01FF)
     ctypes.windll.user32.SetThreadDesktop(hdesk)
     si.lpDesktop = r"WinSta0\Default"
     ```
3. **DPI Scaling:**
   - Windows 125% or 150% display scaling can cause coordinate offsets between screenshot pixel dimensions and PyAutoGUI click coordinates.
   - **Mitigation:** Use `pyautogui.size()` to normalize coordinate ratios or disable DPI virtualization.
4. **Emergency Stop:**
   - Moving the physical mouse rapidly to any screen corner trips PyAutoGUI's built-in `FailSafeException`.

## Portable Packaging & Zero-Setup Deployment

Git rejects files >100MB, preventing direct commit of Playwright's 306MB Chromium binary. This skill resolves portability via dual packaging:

1. **One-Click Bootstrap (`setup.bat` / `setup.ps1`):**
   - Sets `PLAYWRIGHT_BROWSERS_PATH=.browsers` locally inside the folder.
   - Bootstraps virtual environment via `uv` (or `python -m venv`).
   - Installs dependencies and downloads Chromium in <15 seconds.
   - Run immediately after `git clone` or pull:
     ```cmd
     setup.bat
     ```
2. **Offline Air-Gapped Bundle (`package_offline_bundle.py`):**
   - For environments without internet access or storing as a GitHub Release asset:
     ```bash
     python scripts/package_offline_bundle.py --include-binaries
     ```
   - Bundles the skill, code, `.venv`, and pre-installed Chromium into a self-contained archive ready for USB/offline execution.

## Voice (Ears & Mouth) and Vision (Eyes) Multimodal Companion

Fido integrates native zero-dependency Windows voice duplex and screen perception:

- **Ears (Speech Recognition):** Uses Windows native `System.Speech.Recognition` (`MS-1033-80-DESK`) to capture headset microphone input via push-to-talk or on-demand listening (`tools/fido_listen.py`).
- **Mouth (Speech Synthesis):** Uses Windows native `System.Speech.Synthesis` (`Microsoft Zira Desktop` / `Microsoft David Desktop`) for instant audio output to the user's headset (`tools/fido_speak.py`).
- **Eyes (Screen Perception):** High-speed desktop snapshot via `tools/fido_vision.py`. Automatically downscales to max 1024px for token efficiency, extracts active foreground window title, and handles workstation lock states gracefully.
- **Interactive Companion (`tools/fido_companion.py`):** Interactive voice loop bridging headset mic, eyes, and active Gemini session:
  ```bash
  fido speak "Task complete"
  fido look
  fido listen
  fido companion
  ```

## Companion Files in this Skill

- [`setup.bat`](setup.bat): 1-click Windows bootstrap launcher.
- [`setup.ps1`](setup.ps1): 1-click PowerShell bootstrap launcher.
- [`requirements.txt`](requirements.txt): Pinned minimal dependencies (`playwright`, `pyautogui`, `pillow`, `mss`).
- [`.gitignore`](.gitignore): Excludes bulky `.venv/` and `.browsers/` from Git tracking.
- [`scripts/package_offline_bundle.py`](scripts/package_offline_bundle.py): Standalone zip packager.
- [`scripts/safety_guardrails.py`](scripts/safety_guardrails.py): Coordinate limits, destructive command blocklist, step budgeting.
- [`scripts/desktop_engine.py`](scripts/desktop_engine.py): Windows OS screenshot capture, coordinate grid, mouse/keyboard primitives.
- [`scripts/browser_engine.py`](scripts/browser_engine.py): Playwright DOM engine for web autonomy.
- [`scripts/multi_llm_runner.py`](scripts/multi_llm_runner.py): Universal dispatcher for OpenAI, Anthropic, Gemini, and Ollama.
- [`scripts/run_agent.py`](scripts/run_agent.py): CLI orchestrator.
- [`scripts/test_harness.py`](scripts/test_harness.py): Comprehensive test suite.
- [`../../tools/fido_speak.py`](../../tools/fido_speak.py): Native Windows headset TTS synthesizer.
- [`../../tools/fido_listen.py`](../../tools/fido_listen.py): Native Windows headset STT speech recognizer.
- [`../../tools/fido_vision.py`](../../tools/fido_vision.py): Token-efficient screen perception capture.
- [`../../tools/fido_companion.py`](../../tools/fido_companion.py): Interactive voice & vision companion loop.


