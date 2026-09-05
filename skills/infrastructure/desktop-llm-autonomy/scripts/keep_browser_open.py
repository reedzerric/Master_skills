"""
Playwright live autonomous typing demo that stays open indefinitely on screen.
Does NOT auto-close so the user can inspect and interact with it.
"""

import asyncio
from playwright.async_api import async_playwright

HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Autonomous Computer-Use Demo</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #09090b;
      color: #fafafa;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
    }
    .card {
      background: #18181b;
      border: 2px solid #f59e0b;
      border-radius: 16px;
      padding: 36px 52px;
      box-shadow: 0 0 50px rgba(245, 158, 11, 0.25);
      text-align: center;
      max-width: 520px;
      width: 90%;
    }
    h2 {
      margin: 0 0 8px 0;
      color: #f59e0b;
      font-size: 24px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }
    p {
      color: #a1a1aa;
      font-size: 14px;
      margin-bottom: 24px;
    }
    input {
      width: 100%;
      box-sizing: border-box;
      padding: 16px 20px;
      font-size: 20px;
      font-weight: bold;
      border-radius: 10px;
      border: 2px solid #10b981;
      background: #09090b;
      color: #ffffff;
      outline: none;
      box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
    }
    .status {
      margin-top: 20px;
      font-family: monospace;
      font-size: 13px;
      color: #10b981;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="card">
    <h2>Autonomous Agent Action</h2>
    <p>Gemini driving browser on your behalf (Window Kept Open)</p>
    <input id="agent-input" type="text" value="" autofocus />
    <div id="status" class="status">● Status: Initializing...</div>
  </div>
</body>
</html>
"""


async def main():
    print("[*] Launching Chromium window (kept open)...")
    p = await async_playwright().start()
    browser = await p.chromium.launch(
        headless=False,
        args=["--start-maximized"]
    )
    context = await browser.new_context(no_viewport=True)
    page = await context.new_page()

    await page.set_content(HTML_INTERFACE)
    await asyncio.sleep(0.5)

    input_elem = page.locator("#agent-input")
    await input_elem.click()

    await page.evaluate("document.getElementById('status').innerText = '● Status: Typing active...'")
    await input_elem.type("hello world", delay=150)

    await page.evaluate("""
      document.getElementById('status').innerText = '✔ Done: \"hello world\" successfully typed on your behalf!';
    """)
    print("[+] SUCCESS: Window is open on screen and will stay open indefinitely!")

    # Keep alive until user closes the window manually
    while len(context.pages) > 0:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
