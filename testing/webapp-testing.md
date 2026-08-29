---
name: webapp-testing
description: 'Driving a local web application with Python Playwright: a decision tree for static files versus dynamic apps, server lifecycle through scripts/with_server.py, headless browser automation, and waiting on networkidle before touching a JavaScript-rendered DOM. Use when automating or testing a running web app, when a selector is not found because the page has not rendered yet, or when a test needs a dev server up first. For Python unit testing, use pytest-elite.'
version: 1.1.0
category: core
triggers: [automate a web page with playwright, test my local web app, playwright selector not found, wait for the page to render, run a dev server for tests, headless browser script, wait for networkidle]
dependencies: []
inputs: [a running web app or a static HTML file, an interaction to automate]
outputs: [a Playwright automation script, extracted selectors or page state]
tags: [testing, frontend, playwright, web]
links: ['[[pytest-elite]]', '[[js-html-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch2
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
