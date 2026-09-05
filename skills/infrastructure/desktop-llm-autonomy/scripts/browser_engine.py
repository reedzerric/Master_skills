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
        self.guard.validate_url(url)
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
        
        current_url = self._page.url
        self.guard.validate_email_transmission(current_url, selector)
        
        try:
            element = self._page.locator(selector).first
            await element.click(timeout=8000)
            return True
        except Exception:
            try:
                alt = self._page.get_by_text(selector, exact=False).first
                await alt.click(timeout=5000)
                return True
            except Exception:
                raise

    async def type_text(self, selector: Optional[str], text: str, press_enter: bool = False):
        """Type text into input field matching selector with credential field protection."""
        self.guard.increment_step()
        self.guard.validate_text_input(text)
        if not self._page:
            raise RuntimeError("Browser not started.")
        
        element = None
        if selector:
            try:
                candidate = self._page.locator(selector).first
                if await candidate.count() > 0:
                    element = candidate
            except Exception:
                element = None

        if not element:
            candidate = self._page.locator("textarea:visible, input:visible:not([type='file']), [contenteditable='true']").first
            try:
                if await candidate.count() > 0:
                    element = candidate
            except Exception:
                pass

        if element:
            try:
                el_type = await element.get_attribute("type") or ""
                el_name = await element.get_attribute("name") or ""
                el_auto = await element.get_attribute("autocomplete") or ""
                self.guard.validate_input_element({"type": el_type, "name": el_name, "autocomplete": el_auto})
            except SafetyViolation:
                raise
            except Exception:
                pass

            try:
                await element.fill(text, timeout=5000)
                if press_enter:
                    await element.press("Enter")
                return
            except Exception:
                # Fallback to click + keyboard typing
                try:
                    await element.click(timeout=3000)
                except Exception:
                    pass

        await self._page.keyboard.type(text)
        if press_enter:
            await self._page.keyboard.press("Enter")

    async def press_key(self, key: str):
        """Press keyboard key on page."""
        self.guard.increment_step()
        if not self._page:
            raise RuntimeError("Browser not started.")
        key_norm = "Enter" if key.lower() == "enter" else key
        await self._page.keyboard.press(key_norm)

    async def wait(self, seconds: float = 1.0):
        """Wait for specified duration."""
        await asyncio.sleep(seconds)

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
