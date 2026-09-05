"""
Live autonomous browser demonstration:
Opens a visible browser window on user's desktop, focuses input, and types 'hello world'.
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
      border: 1px solid #27272a;
      border-radius: 16px;
      padding: 32px 48px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.6);
      text-align: center;
      max-width: 500px;
      width: 90%;
    }
    h2 {
      margin: 0 0 8px 0;
      color: #f59e0b;
      font-size: 22px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }
    p {
      color: #a1a1aa;
      font-size: 13px;
      margin-bottom: 24px;
    }
    input {
      width: 100%;
      box-sizing: border-box;
      padding: 14px 18px;
      font-size: 18px;
      font-weight: bold;
      border-radius: 10px;
      border: 2px solid #f59e0b;
      background: #09090b;
      color: #ffffff;
      outline: none;
      box-shadow: 0 0 15px rgba(245, 158, 11, 0.2);
      transition: all 0.2s;
    }
    .status {
      margin-top: 16px;
      font-family: monospace;
      font-size: 12px;
      color: #34d399;
    }
  </style>
</head>
<body>
  <div class="card">
    <h2>Autonomous Agent Action</h2>
    <p>Gemini pair-programming agent driving browser on user behalf</p>
    <input id="agent-input" type="text" placeholder="Awaiting agent keystrokes..." autofocus />
    <div id="status" class="status">● Status: Initialized</div>
  </div>
</body>
</html>
"""


async def main():
    print("[*] Launching visible Chromium browser window on desktop...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--start-maximized", "--window-size=1280,800"]
        )
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()

        print("[*] Rendering interactive interface...")
        await page.set_content(HTML_INTERFACE)
        await asyncio.sleep(1)

        print("[*] Focusing target input element...")
        input_elem = page.locator("#agent-input")
        await input_elem.click()

        print("[*] Typing 'hello world' character-by-character on user behalf...")
        await page.evaluate("document.getElementById('status').innerText = '● Status: Typing active...'")
        await input_elem.type("hello world", delay=150)

        await page.evaluate("""
          document.getElementById('status').innerText = '✔ Done: \"hello world\" successfully typed on user behalf!';
          document.getElementById('status').style.color = '#10b981';
          document.getElementById('agent-input').style.borderColor = '#10b981';
        """)
        print("\n[+] SUCCESS: 'hello world' typed into visible browser window!")
        print("[*] Keeping window open for 10 seconds for user inspection...")
        await asyncio.sleep(10)

        print("[*] Closing browser session.")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
