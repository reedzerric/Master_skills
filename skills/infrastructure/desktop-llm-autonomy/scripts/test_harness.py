"""
Automated Test Suite for Desktop LLM Autonomy.
Verifies safety guardrails, desktop screenshot capture, browser automation, and dispatch loops.
"""

import asyncio
import sys
import unittest
import base64

from safety_guardrails import SafetyGuard, SafetyViolation
from desktop_engine import DesktopEngine
from browser_engine import BrowserEngine
from multi_llm_runner import MultiLLMDispatcher
from run_agent import run_browser_loop


class TestSafetyGuardrails(unittest.TestCase):
    def setUp(self):
        self.guard = SafetyGuard(screen_size=(1920, 1080), max_steps=3)

    def test_coordinate_validation(self):
        # Valid coords
        x, y = self.guard.validate_coordinates(500, 500)
        self.assertEqual((x, y), (500, 500))

        # Out of bounds coords
        with self.assertRaises(SafetyViolation):
            self.guard.validate_coordinates(-10, 500)
        with self.assertRaises(SafetyViolation):
            self.guard.validate_coordinates(500, 2000)

        # Fail-safe corner trigger (top-left 0-15px)
        with self.assertRaises(SafetyViolation):
            self.guard.validate_coordinates(5, 5)

    def test_destructive_command_blocking(self):
        # Safe input
        self.guard.validate_text_input("echo 'Hello World'")

        # Dangerous inputs
        with self.assertRaises(SafetyViolation):
            self.guard.validate_text_input("format C: /y")
        with self.assertRaises(SafetyViolation):
            self.guard.validate_text_input("rmdir /s /q test_dir")
        with self.assertRaises(SafetyViolation):
            self.guard.validate_text_input("del /f /s /q *.*")

    def test_step_budget_enforcement(self):
        self.guard.increment_step()  # Step 1
        self.guard.increment_step()  # Step 2
        self.guard.increment_step()  # Step 3
        with self.assertRaises(SafetyViolation):
            self.guard.increment_step()  # Step 4 (exceeds max_steps=3)

    def test_financial_domain_blocking(self):
        # Blocked domains
        with self.assertRaises(SafetyViolation):
            self.guard.validate_url("https://www.chase.com/login")
        with self.assertRaises(SafetyViolation):
            self.guard.validate_url("https://paypal.com/signin")
        with self.assertRaises(SafetyViolation):
            self.guard.validate_url("https://app.1password.com")
        
        # Allowed benign domain
        self.guard.validate_url("https://example.com/dashboard")

    def test_password_field_protection(self):
        with self.assertRaises(SafetyViolation):
            self.guard.validate_input_element({"type": "password"})
        with self.assertRaises(SafetyViolation):
            self.guard.validate_input_element({"name": "current_password", "type": "text"})
        
        # Benign input
        self.guard.validate_input_element({"type": "text", "name": "search_query"})

    def test_unauthorized_email_sending_blocked(self):
        # Default guard blocks email sending
        with self.assertRaises(SafetyViolation):
            self.guard.validate_email_transmission("https://mail.google.com/mail/u/0", "button:has-text('Send')")
        with self.assertRaises(SafetyViolation):
            self.guard.validate_email_transmission("https://outlook.office.com/mail", "click send")

        # Non-mail domain is fine
        self.guard.validate_email_transmission("https://github.com", "submit issue")

        # Explicitly permitted guard allows send
        perm_guard = SafetyGuard(screen_size=(1920, 1080), allow_email_send=True)
        perm_guard.validate_email_transmission("https://mail.google.com/mail/u/0", "button:has-text('Send')")

    def test_token_image_optimization(self):
        from PIL import Image
        big_img = Image.new("RGB", (1920, 1080), color=(100, 100, 100))
        optimized = SafetyGuard.optimize_image_for_tokens(big_img, max_dim=1024)
        self.assertLessEqual(max(optimized.size), 1024)
        self.assertEqual(optimized.size[0], 1024)



class TestDesktopEngine(unittest.TestCase):
    def test_screen_capture_and_dimensions(self):
        engine = DesktopEngine(fallback_on_locked=True)
        data = engine.capture_screen(scale_down_factor=0.5, add_grid=True)
        self.assertIn("width", data)
        self.assertIn("height", data)
        self.assertIn("base64_jpeg", data)
        self.assertTrue(len(data["base64_jpeg"]) > 100)
        self.assertEqual(data["scaled_width"], data["width"] // 2)


class TestBrowserEngine(unittest.IsolatedAsyncioTestCase):
    async def test_browser_navigation_and_extraction(self):
        engine = BrowserEngine(headless=True)
        await engine.start(viewport_width=800, viewport_height=600)
        try:
            res = await engine.goto("https://example.com")
            self.assertIn("Example Domain", res["title"])

            text = await engine.extract_visible_text()
            self.assertIn("Example Domain", text)
            self.assertIn("documentation examples", text)

            shot = await engine.capture_screenshot()
            self.assertTrue(len(shot["base64_jpeg"]) > 100)

            elements = await engine.get_interactive_elements()
            self.assertTrue(isinstance(elements, list))
        finally:
            await engine.close()


class TestEndToEndAutonomy(unittest.IsolatedAsyncioTestCase):
    async def test_mock_browser_autonomous_loop(self):
        dispatcher = MultiLLMDispatcher(provider="mock")
        res = await run_browser_loop(
            dispatcher=dispatcher,
            goal="Navigate to example.com and verify the domain title",
            max_steps=5,
            headless=True
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["steps"], 2)
        self.assertIn("Successfully verified", res["result"])


if __name__ == "__main__":
    unittest.main()
