---
name: webapp-testing
description: Guidelines for testing local web applications using native Python Playwright scripts and server management helpers. Use when working with testing, frontend, playwright.
version: 1.0.0
category: core
triggers: [testing, frontend, playwright, web, webapp]
dependencies: []
inputs: [source files, project config]
outputs: [refactored code, review findings]
title: Web Application Testing (Playwright)
date: 2026-03-08
task_ref: initial-setup
confidence_score: 1.0
tags: [testing, frontend, playwright, web]
links: ["[[knowledgebase/playwright-patterns]]"]
---

# Web Application Testing (Playwright)

## 🎯 Purpose
Guidelines for testing local web applications using native Python Playwright scripts and server management helpers.

## 🛠️ The Process / Fact

### 1. Decision Tree
- **Static HTML:** Read file directly for selectors.
- **Dynamic App:** Run server -> Wait for `networkidle` -> Inspect rendered DOM -> Identify selectors -> Execute actions.

### 2. Using `with_server.py`
To manage server lifecycle for automation:
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python automation.py
```

### 3. Automation Script Template
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always headless
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle') # CRITICAL for JS
    # ... logic
    browser.close()
```

## ⚠️ Known Quirks or Edge Cases
- **Missing Waits:** Failing to wait for `networkidle` on dynamic apps will cause selector failures.
- **Headless Mode:** Always use `headless=True` in shared environments.

## 🔗 Related Memories
- [[knowledgebase/playwright-patterns]]
- [[testing/playwright/examples/element_discovery]]
- [[testing/playwright/examples/console_logging]]
- [[testing/playwright/examples/static_html_automation]]
- [[testing/playwright/scripts/with_server]]
