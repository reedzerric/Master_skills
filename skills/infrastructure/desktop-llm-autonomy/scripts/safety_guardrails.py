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
    r"wallet",
    r"metamask",
    r"authenticator",
    r"banking",
]


class SafetyViolation(Exception):
    """Raised when an agent action violates a safety rule."""
    pass


class SafetyGuard:
    def __init__(self, screen_size: Tuple[int, int], max_steps: int = 25, require_confirmation: bool = False):
        self.screen_width, self.screen_height = screen_size
        self.max_steps = max_steps
        self.current_step = 0
        self.require_confirmation = require_confirmation

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

    def check_app_target(self, window_title: str) -> bool:
        """Verify the active window is not a blocked credential or banking manager."""
        for pattern in RESTRICTED_APP_PATTERNS:
            if re.search(pattern, window_title, re.IGNORECASE):
                raise SafetyViolation(
                    f"Action blocked: active application matches restricted security pattern '{pattern}'"
                )
        return True
