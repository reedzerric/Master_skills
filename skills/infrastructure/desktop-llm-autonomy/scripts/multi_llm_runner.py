"""
Multi-LLM Dispatcher for Autonomous Agents.
Supports Anthropic, OpenAI, Google Gemini, Ollama, and Mock testing modes.
"""

from typing import Dict, Any, List, Optional
import os
import json
import urllib.request
import urllib.error

# Canonical system prompt for computer use / browser autonomy
AGENT_SYSTEM_PROMPT = """You are an autonomous computer-use agent acting on behalf of the user.
You observe the screen or browser DOM and produce the next single tool action to achieve the goal.

Action Guidelines:
1. If the goal is satisfied, call finish(result="...").
2. Prefer DOM element selectors or exact text when in browser mode.
3. In desktop mode, estimate coordinates (x, y) accurately.
4. Avoid clicking anywhere near the top-left (0-15px) corner to prevent emergency fail-safe abort.
5. If an unexpected error or popup occurs, dismiss it or adapt.

Output your decision as a valid JSON object with fields:
{
  "thought": "Brief reasoning for this action",
  "action": "click" | "type_text" | "press_key" | "navigate" | "finish",
  "params": { ... }
}
"""


class MultiLLMDispatcher:
    def __init__(self, provider: str = "mock", model_name: Optional[str] = None, api_key: Optional[str] = None):
        self.provider = provider.lower()
        self.model_name = model_name
        self.api_key = api_key or os.environ.get(f"{self.provider.upper()}_API_KEY")

        # Set default model per provider if unspecified
        if not self.model_name:
            defaults = {
                "anthropic": "claude-3-5-sonnet-20241022",
                "openai": "gpt-4o",
                "gemini": "gemini-2.0-flash",
                "ollama": "llama3.2-vision",
                "mock": "mock-test-agent",
            }
            self.model_name = defaults.get(self.provider, "mock-test-agent")

    def decide_next_action(
        self,
        goal: str,
        history: List[Dict[str, Any]],
        current_state: Dict[str, Any],
        mode: str = "browser"
    ) -> Dict[str, Any]:
        """
        Takes the goal, action history, and current environment state (DOM or screenshot).
        Returns a structured action dictionary.
        """
        if self.provider == "mock":
            return self._mock_decision(goal, history, current_state, mode)
        elif self.provider == "openai":
            return self._call_openai(goal, history, current_state, mode)
        elif self.provider == "anthropic":
            return self._call_anthropic(goal, history, current_state, mode)
        elif self.provider == "gemini":
            return self._call_gemini(goal, history, current_state, mode)
        elif self.provider == "ollama":
            return self._call_ollama(goal, history, current_state, mode)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def _mock_decision(
        self, goal: str, history: List[Dict[str, Any]], current_state: Dict[str, Any], mode: str
    ) -> Dict[str, Any]:
        """Deterministic mock responses for test verification."""
        step = len(history)
        if mode == "browser":
            if step == 0:
                return {
                    "thought": "Navigate to the requested target URL.",
                    "action": "navigate",
                    "params": {"url": "https://example.com"},
                }
            elif step == 1:
                return {
                    "thought": "Page loaded. Verify content and finish.",
                    "action": "finish",
                    "params": {"result": f"Successfully verified page content for goal: {goal}"},
                }
        else:  # desktop
            if step == 0:
                return {
                    "thought": "Move to central area and click.",
                    "action": "click",
                    "params": {"x": 500, "y": 400},
                }
            elif step == 1:
                return {
                    "thought": "Type verification text.",
                    "action": "type_text",
                    "params": {"text": "Agent Autonomy Test", "press_enter": True},
                }
            else:
                return {
                    "thought": "Desktop actions verified.",
                    "action": "finish",
                    "params": {"result": "Desktop autonomy sequence completed successfully."},
                }

    def _call_openai(self, goal: str, history: List[Dict[str, Any]], current_state: Dict[str, Any], mode: str) -> Dict[str, Any]:
        """Call OpenAI chat completions API with JSON output mode."""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAI provider.")

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        user_content = [
            {"type": "text", "text": f"Goal: {goal}\nMode: {mode}\nHistory: {json.dumps(history)}\nState: {json.dumps({k: v for k, v in current_state.items() if k != 'base64_jpeg'})}"}
        ]
        if "base64_jpeg" in current_state:
            user_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{current_state['base64_jpeg']}"}
            })

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": AGENT_SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1,
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            return json.loads(content)

    def _call_anthropic(self, goal: str, history: List[Dict[str, Any]], current_state: Dict[str, Any], mode: str) -> Dict[str, Any]:
        """Call Anthropic Messages API."""
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required for Anthropic provider.")

        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
        }

        content_blocks = [
            {"type": "text", "text": f"Goal: {goal}\nMode: {mode}\nHistory: {json.dumps(history)}\nState summary: {json.dumps({k: v for k, v in current_state.items() if k != 'base64_jpeg'})}"}
        ]
        if "base64_jpeg" in current_state:
            content_blocks.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": current_state["base64_jpeg"],
                }
            })

        payload = {
            "model": self.model_name,
            "max_tokens": 1024,
            "system": AGENT_SYSTEM_PROMPT + "\nRespond with raw JSON only, no markdown markers.",
            "messages": [{"role": "user", "content": content_blocks}],
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            text = data["content"][0]["text"].strip()
            # Strip code blocks if present
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            return json.loads(text.strip())

    def _call_gemini(self, goal: str, history: List[Dict[str, Any]], current_state: Dict[str, Any], mode: str) -> Dict[str, Any]:
        """Call Google Gemini REST endpoint."""
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required for Gemini provider.")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}

        parts = [
            {"text": f"{AGENT_SYSTEM_PROMPT}\n\nGoal: {goal}\nMode: {mode}\nHistory: {json.dumps(history)}\nState: {json.dumps({k: v for k, v in current_state.items() if k != 'base64_jpeg'})}"}
        ]
        if "base64_jpeg" in current_state:
            parts.append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": current_state["base64_jpeg"],
                }
            })

        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {"response_mime_type": "application/json"}
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(text)

    def _call_ollama(self, goal: str, history: List[Dict[str, Any]], current_state: Dict[str, Any], mode: str) -> Dict[str, Any]:
        """Call local Ollama instance (http://localhost:11434)."""
        url = "http://localhost:11434/api/generate"
        headers = {"Content-Type": "application/json"}

        prompt = f"{AGENT_SYSTEM_PROMPT}\n\nGoal: {goal}\nHistory: {json.dumps(history)}\nState: {json.dumps({k: v for k, v in current_state.items() if k != 'base64_jpeg'})}"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "format": "json",
            "stream": False,
        }
        if "base64_jpeg" in current_state:
            payload["images"] = [current_state["base64_jpeg"]]

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return json.loads(data["response"])
