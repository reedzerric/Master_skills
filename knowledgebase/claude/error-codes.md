---
name: error-codes
description: Always use the SDK's typed exception classes instead of string matching. Use when working with ai, claude, api.
version: 1.0.0
category: ai_infrastructure
triggers: [ai, claude, api, errors, troubleshooting, error, codes]
dependencies: [claude-api]
inputs: [corpus or prompt, model config]
outputs: [pipeline code, evaluation results]
title: Claude API Error Codes
date: 2026-03-08
task_ref: skill-migration
confidence_score: 1.0
tags: [ai, claude, api, errors, troubleshooting]
links: ["[[skills/backend/claude-api]]"]
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
