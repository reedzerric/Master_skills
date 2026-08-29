---
name: local-first-ai-elite
description: 'Running AI in the browser: the WebGPU and transformers.js stack, the load-and-warm lifecycle, progressive enhancement so the page works before the model arrives, and hybrid patterns that fall back to a server. Use when running inference client-side, when model download blocks first paint, or when deciding what stays local and what goes to the server. For the privacy rationale, use privacy-by-design-elite.'
version: 1.1.0
category: core
triggers: [run a model in the browser, webgpu inference, transformers.js, model download blocks the page, offline ai features, local or server inference, progressive enhancement for ai]
dependencies: [js-html-elite]
inputs: [a model and a target device budget]
outputs: [a client-side inference pipeline, a server fallback strategy]
tags: [frontend, ai, local-first, webgpu, onnx, transformersjs]
links: ['[[js-html-elite]]', '[[privacy-by-design-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
---

# Local-First & Edge AI Mastery (2026)

## 🎯 Purpose
Guidelines for architecting privacy-centric, low-latency applications that run AI models entirely on-device (browser or edge).

## 🛠️ The Process / Fact

### 1. Technology Stack
- **WebGPU:** Primary compute layer for hardware acceleration (70-90% native GPU performance).
- **ONNX Runtime Web:** Preferred execution engine with WebGPU Execution Provider.
- **Transformers.js v3:** Standard high-level API for running Llama, Phi, and Whisper models in-browser.

### 2. Implementation Lifecycle
- **Quantization:** ALWAYS use 4-bit (Q4) or 8-bit (INT8) models to reduce VRAM usage and model size.
- **Worker Execution:** Execute inference in a dedicated **Web Worker** to prevent blocking the UI thread.
- **Model Caching:** Use the **Origin Private File System (OPFS)** for model storage to ensure instant loads and offline access.

### 3. Progressive Enhancement Strategy
1.  **Try WebGPU:** Attempt high-performance on-device inference.
2.  **Fallback to Wasm:** Use CPU (WebAssembly) if GPU is unavailable or low-powered.
3.  **Fallback to Cloud:** Use a remote API (e.g., Claude) only for heavy reasoning or unsupported devices.

### 4. Hybrid Patterns
- **Sidecar Pattern:** Use a local model (e.g., Phi-3) for real-time tasks (PII masking, autocomplete) and a cloud model for complex logic.
- **Zero-Upload Analytics:** Process sensitive CSVs or documents locally via embeddings and vector search (e.g., LanceDB).

## ⚠️ Known Quirks or Edge Cases
- **VRAM Capping:** Browsers may cap VRAM (e.g., 2GB). Avoid loading massive models (>7B) on-device.
- **Warm-up:** Always perform a "dummy" inference run to trigger JIT compilation of GPU kernels before the first user interaction.

## 🔗 Related Memories
- [[skills/frontend/js-html-elite]]
- [[skills/infrastructure/serverless-edge-elite]]
