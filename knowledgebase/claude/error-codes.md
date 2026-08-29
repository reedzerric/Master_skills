---
name: error-codes
description: HTTP status codes the Claude API returns, which of them are retryable, and the typed SDK exception classes to catch instead of matching on error strings. Use when handling a 429, 400, 500 or 529 from Claude, or deciding whether a failure should be retried. For model IDs, pricing and request-shape rules, use models.
version: 1.1.0
category: ai_infrastructure
triggers: [claude api returned 429, anthropic overloaded error, rate limited by anthropic, should i retry this claude error, catch anthropic sdk exception, 529 from claude, invalid request error from claude]
dependencies: [claude-api]
inputs: [an HTTP status code or SDK exception]
outputs: [the exception class to catch, a retry decision]
tags: [ai, claude, api, errors, troubleshooting]
links: ['[[claude-api]]', '[[models]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-kb
title: Claude API Error Codes
---

# HTTP Error Codes Reference

| Code | Error Type | Retryable | Common Cause |
| --- | --- | --- | --- |
| 400 | `invalid_request_error` | No | Invalid request format or parameters |
| 401 | `authentication_error` | No | Invalid or missing API key |
| 429 | `rate_limit_error` | Yes | Too many requests |
| 529 | `overloaded_error` | Yes | API is temporarily overloaded |

## Typed Exceptions in SDKs
Always use the SDK's typed exception classes instead of string matching.

| HTTP Code | TypeScript Class | Python Class |
| --- | --- | --- |
| 400 | `Anthropic.BadRequestError` | `anthropic.BadRequestError` |
| 429 | `Anthropic.RateLimitError` | `anthropic.RateLimitError` |
| 500+ | `Anthropic.InternalServerError` | `anthropic.InternalServerError` |
