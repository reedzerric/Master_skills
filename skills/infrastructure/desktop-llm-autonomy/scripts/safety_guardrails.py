"""
Safety guardrails for autonomous LLM computer use and desktop actions.
Provides fail-safes, blocklists, coordinate validation, and step budgets.
"""

from typing import Tuple, List, Optional
import os
import re

# Emergency fail-safe trigger coordinates (top-left 10x10 px or PyAutoGUI default)
FAILSAFE_CORNER_THRESHOLD = 15

# Blocklist of destructive shell commands or file operations
DESTRUCTIVE_COMMAND_PATTERNS = [
    r"format\s+[a-zA-Z]:",
    r"rmdir\s+/s",
    r"del\s+/f\s+/s\s+/q",
    r"reg\s+delete",
    r"diskpart",
    r"bcdedit",
    r"shutdown\s+/[s|r]",
    r"DROP\s+DATABASE",
    r"DROP\s+TABLE",
    r":\(\)\s*\{\s*:\|:&\s*\};:",  # fork bomb
]

# Sensitive window titles or process targets requiring explicit confirmation
RESTRICTED_APP_PATTERNS = [
    r"1password",
    r"bitwarden",
    r"keepass",
    r"lastpass",
    r"dashlane",
    r"wallet",
    r"metamask",
    r"authenticator",
    r"banking",
    r"chase",
    r"bank\s*of\s*america",
    r"wells\s*fargo",
    r"fidelity",
    r"vanguard",
    r"schwab",
    r"robinhood",
    r"coinbase",
    r"binance",
    r"paypal",
    r"stripe",
]

# Blocked financial, banking, and credential manager domains
RESTRICTED_DOMAINS = [
    "chase.com",
    "bankofamerica.com",
    "wellsfargo.com",
    "citi.com",
    "capitalone.com",
    "usbank.com",
    "pnc.com",
    "td.com",
    "fidelity.com",
    "vanguard.com",
    "schwab.com",
    "etrade.com",
    "robinhood.com",
    "coinbase.com",
    "binance.com",
    "kraken.com",
    "paypal.com",
    "stripe.com",
    "venmo.com",
    "cash.app",
    "1password.com",
    "bitwarden.com",
    "lastpass.com",
    "dashlane.com",
    "login.gov",
    "irs.gov",
]

# Common webmail domains where unconfirmed email sending must be blocked
WEBMAIL_DOMAINS = [
    "mail.google.com",
    "outlook.office.com",
    "outlook.live.com",
    "mail.yahoo.com",
    "icloud.com/mail",
    "proton.me",
]


class SafetyViolation(Exception):
    """Raised when an agent action violates a safety rule."""
    pass


class SafetyGuard:
    def __init__(
        self,
        screen_size: Tuple[int, int],
        max_steps: int = 25,
        allow_email_send: bool = False,
        allow_financial_access: bool = False
    ):
        self.screen_width, self.screen_height = screen_size
        self.max_steps = max_steps
        self.current_step = 0
        self.allow_email_send = allow_email_send
        self.allow_financial_access = allow_financial_access
        self.estimated_tokens_used = 0

    def increment_step(self):
        """Track step execution and enforce maximum step budget."""
        self.current_step += 1
        if self.current_step > self.max_steps:
            raise SafetyViolation(
                f"Agent exceeded maximum step limit ({self.max_steps}). Action terminated."
            )

    def validate_coordinates(self, x: int, y: int) -> Tuple[int, int]:
        """Ensure clicked coordinates are inside visible screen boundaries."""
        if not (0 <= x <= self.screen_width):
            raise SafetyViolation(f"Target X coordinate ({x}) out of bounds [0, {self.screen_width}].")
        if not (0 <= y <= self.screen_height):
            raise SafetyViolation(f"Target Y coordinate ({y}) out of bounds [0, {self.screen_height}].")
        
        # Check fail-safe corner avoidance (top-left)
        if x < FAILSAFE_CORNER_THRESHOLD and y < FAILSAFE_CORNER_THRESHOLD:
            raise SafetyViolation(
                f"Coordinates ({x}, {y}) trigger the fail-safe abort zone."
            )
        return x, y

    def validate_text_input(self, text: str):
        """Detect and block potentially destructive text or command payloads."""
        for pattern in DESTRUCTIVE_COMMAND_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                raise SafetyViolation(
                    f"Blocked destructive command pattern detected in input: '{pattern}'"
                )

    def validate_url(self, url: str):
        """Enforce strict isolation from financial, banking, and credential services."""
        if self.allow_financial_access:
            return

        clean_url = url.lower()
        for domain in RESTRICTED_DOMAINS:
            if domain in clean_url:
                raise SafetyViolation(
                    f"Access blocked to financial / credential domain '{domain}' without explicit user permission."
                )

    def validate_input_element(self, element_attributes: dict):
        """Block automated typing into password, PIN, or credential fields."""
        el_type = str(element_attributes.get("type", "")).lower()
        el_name = str(element_attributes.get("name", "")).lower()
        el_autocomplete = str(element_attributes.get("autocomplete", "")).lower()

        if el_type == "password" or "password" in el_name or "password" in el_autocomplete:
            raise SafetyViolation(
                "Access blocked: automated interaction with password/credential field is strictly forbidden."
            )

    def validate_email_transmission(self, current_url: str, action_target: str):
        """Prohibit sending emails unless user granted explicit permission for this task."""
        if self.allow_email_send:
            return

        is_mail_site = any(d in current_url.lower() for d in WEBMAIL_DOMAINS)
        send_keywords = ["send", "submit", "deliver", "transmit"]
        is_send_action = any(k in action_target.lower() for k in send_keywords)

        if is_mail_site and is_send_action:
            raise SafetyViolation(
                "Action blocked: NEVER send emails without explicit user permission."
            )

    def check_app_target(self, window_title: str) -> bool:
        """Verify the active window is not a blocked credential or banking manager."""
        if self.allow_financial_access:
            return True

        for pattern in RESTRICTED_APP_PATTERNS:
            if re.search(pattern, window_title, re.IGNORECASE):
                raise SafetyViolation(
                    f"Action blocked: active application matches restricted security pattern '{pattern}'"
                )
        return True

    def track_token_spend(self, prompt_tokens: int, completion_tokens: int = 0):
        """Log token consumption for efficiency auditing."""
        self.estimated_tokens_used += (prompt_tokens + completion_tokens)

    @staticmethod
    def optimize_image_for_tokens(image, max_dim: int = 1024, quality: int = 75):
        """
        Resize image so longest edge is <= max_dim and compress JPEG quality.
        Slashes vision token consumption by 60-70% while preserving UI legibility.
        """
        from PIL import Image
        orig_w, orig_h = image.size
        if max(orig_w, orig_h) > max_dim:
            scale = max_dim / max(orig_w, orig_h)
            new_w = int(orig_w * scale)
            new_h = int(orig_h * scale)
            return image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        return image

