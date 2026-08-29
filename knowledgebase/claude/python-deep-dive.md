---
name: python-deep-dive
description: 'Working Python patterns for the anthropic SDK: client setup, streaming, automatic prompt caching, the tool-use loop, MCP clients, and error handling. Use when writing or debugging Python that calls the Claude API. For the same ground in TypeScript, use typescript-deep-dive; for tool design rather than tool code, use tool-use-concepts.'
version: 1.1.0
category: ai_infrastructure
triggers: [call claude from python, anthropic python sdk, stream a claude response in python, prompt caching in python, python tool use loop, async anthropic client]
dependencies: [claude-api, tool-use-concepts]
inputs: [a Python Claude API integration task]
outputs: [working Python SDK code]
tags: [ai, claude, api, python, sdk]
links: ['[[claude-api]]', '[[tool-use-concepts]]', '[[typescript-deep-dive]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-kb
---

# Claude API Python Deep Dive

## Installation & Initialization
```python
pip install anthropic
import anthropic
client = anthropic.Anthropic()
```

## Core Patterns

### Basic Message
```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Prompt Caching (90% cost savings)
```python
# Automatic caching of the last cacheable block
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    cache_control={"type": "ephemeral"},
    system="Large context here...",
    messages=[{"role": "user", "content": "Summarize"}]
)
```

### Adaptive Thinking (Opus 4.6)
```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[{"role": "user", "content": "Solve this..."}]
)
```

## Tool Use & Agents

### Tool Runner (Recommended)
The tool runner handles the agentic loop automatically.
```python
from anthropic import beta_tool

@beta_tool
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get current weather for a location.
    Args:
        location: City and state, e.g., San Francisco, CA.
    """
    return f"72°F in {location}"

runner = client.beta.messages.tool_runner(
    model="claude-opus-4-6",
    max_tokens=4096,
    tools=[get_weather],
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
)
for message in runner:
    print(message)
```

### MCP Tool Conversion
Convert MCP tools for use with the tool runner (`pip install anthropic[mcp]`).
```python
from anthropic.lib.tools.mcp import async_mcp_tool
# ... inside async context with mcp_client
tools = [async_mcp_tool(t, mcp_client) for t in tools_result.tools]
```

### Code Execution
```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    tools=[{"type": "code_execution_20260120", "name": "code_execution"}],
    messages=[{"role": "user", "content": "Analyze data..."}]
)
```

## Error Handling
Always use typed exceptions: `anthropic.BadRequestError`, `anthropic.RateLimitError`, etc.
