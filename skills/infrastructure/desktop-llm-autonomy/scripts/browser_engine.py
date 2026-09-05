"""
Browser DOM automation engine for autonomous web tasks.
Uses Playwright to provide structured element targeting, text extraction, and navigation.
"""

from typing import Dict, Any, Optional, List
import base64
import asyncio
from playwright.async_api import async_playwright, Browser, Page, BrowserContext

from safety_guardrails import SafetyGuard, SafetyViolation


class BrowserEngine:
    def __init__(self, guard: Optional[SafetyGuard] = None, headless: bool = True):
        self.guard = guard or SafetyGuard(screen_size=(1280, 800))
        self.headless = headless
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

    async def start(self, viewport_width: int = 1280, viewport_height: int = 800):
        """Initialize Playwright browser and open initial page."""
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=self.headless)
        self._context = await self._browser.new_context(
            viewport={"width": viewport_width, "height": viewport_height}
        )
        self._page = await self._context.new_page()

    async def close(self):
        """Cleanly terminate browser session."""
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def goto(self, url: str) -> Dict[str, Any]:
        """Navigate to URL and wait for DOM load."""
        self.guard.increment_step()
        if not self._page:
            raise RuntimeError("Browser not started. Call start() first.")
        
        response = await self._page.goto(url, wait_until="domcontentloaded", timeout=30000)
        title = await self._page.title()
        return {
            "url": self._page.url,
            "title": title,
            "status": response.status if response else None,
        }

    async def click(self, selector: str) -> bool:
        """Click on element matching CSS selector, text, or accessibility locator."""
        self.guard.increment_step()
        if not self._page:
            raise RuntimeError("Browser not started.")
        
        element = self._page.locator(selector).first
        await element.click(timeout=10000)
        return True

    async def type_text(self, selector: str, text: str, press_enter: bool = False):
        """Type text into input field matching selector."""
        self.guard.increment_step()
        self.guard.validate_text_input(text)
        if not self._page:
            raise RuntimeError("Browser not started.")
        
        element = self._page.locator(selector).first
        await element.fill(text, timeout=10000)
        if press_enter:
            await element.press("Enter")

    async def extract_visible_text(self) -> str:
        """Extract primary readable text content from the current page."""
        if not self._page:
            raise RuntimeError("Browser not started.")
        return await self._page.inner_text("body")

    async def capture_screenshot(self) -> Dict[str, Any]:
        """Take screenshot of current page view."""
        if not self._page:
            raise RuntimeError("Browser not started.")
        
        img_bytes = await self._page.screenshot(type="jpeg", quality=85)
        b64_data = base64.b64encode(img_bytes).decode("utf-8")
        return {
            "url": self._page.url,
            "title": await self._page.title(),
            "base64_jpeg": b64_data,
            "raw_bytes": img_bytes,
        }

    async def get_interactive_elements(self) -> List[Dict[str, str]]:
        """List clickable/input interactive elements on page for agent targeting."""
        if not self._page:
            raise RuntimeError("Browser not started.")
        
        elements = await self._page.query_selector_all("button, a, input, select, textarea, [role='button']")
        results = []
        for i, el in enumerate(elements[:30]):  # Limit to first 30 elements
            tag = await el.evaluate("el => el.tagName.toLowerCase()")
            text = (await el.inner_text()).strip() if tag not in ["input", "select"] else ""
            input_type = await el.get_attribute("type") or ""
            placeholder = await el.get_attribute("placeholder") or ""
            selector = await el.evaluate("""el => {
                if (el.id) return '#' + el.id;
                if (el.name) return `[name="${el.name}"]`;
                return el.tagName.toLowerCase();
            }""")
            results.append({
                "index": i,
                "tag": tag,
                "type": input_type,
                "text": text[:40],
                "placeholder": placeholder,
                "selector": selector,
            })
        return results
