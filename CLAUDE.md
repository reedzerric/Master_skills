# CLAUDE.MD: ACTIVE SKILLSET ADOPTION

## 🚀 Initialization
Claude, you are working within the "Master Skills" framework. You must **INSTALL** the standards found in this repository as your default operating procedure for this user.

## 🧠 Core Directives
0. **Routing First:** Parse `skills_manifest.json` to find the skill that matches the task, resolve its `dependencies`, then load it. `SKILL_TREE.md` is the human-readable view of the same map.
1. **Primary Source:** Read `agent.md` and `WORKSPACE_INDEX.md` before taking any action.
2. **Priority:** The memories in `/skills/`, `/knowledgebase/`, and `/testing/` take absolute precedence over your baseline training data.
3. **Standards:** Use the **Elite Series** (uv, ruff, rust-tokio, postgres-18, temporal-api) for all code generation.
4. **Learning Loop:** You are required to document any new patterns or environmental quirks using the established memory protocol.

## 🕸️ Knowledge Graph Gate (run before broad exploration)

Before grepping or reading your way around an unfamiliar part of the workspace,
check the graph. Decision order:

1. **Does `graphify-out/graph.json` exist?**
   - **No** → say so and offer to build it. Do not build unasked.
     Free build: `graphify extract . --code-only` (local AST, no API key).
   - **Yes** → continue to 2.
2. **Is it current?** `graphify check-update .`
   - Silent + exit 0 → **current. Skip the rebuild.** Do not re-run extraction.
   - Reports pending → `graphify update .` (free, AST-only, code files).
3. **Query instead of grepping** — but pick the right tool for the question:

   | Question shape | Works? | Command |
   | :--- | :--- | :--- |
   | Named symbol — `TreeSitterExtractor`, a class, a function | **yes** | `graphify query "<symbol>" --budget 2000` |
   | How two things connect | **yes** | `graphify path "<A>" "<B>"` |
   | Architectural hubs | **yes** | `graphify god-nodes --top 10` |
   | Conceptual — "where is auth handled?" | **no, in code-only mode** | fall back to grep |

   Concept-level retrieval requires the semantic doc pass, which the current
   graph does **not** have. In code-only mode `query` matches node *labels*, so
   "authentication" will not find `auth_views.py`. Query the identifier, or grep.

**Still read raw files** to modify or debug specific lines. The graph orients;
it does not replace the file you are about to edit.

## 🔁 Rebuild policy — incremental only

The full semantic build is a **one-time** cost. After it, never re-run a full
extraction; graphify is incremental by default and re-extracts only files whose
content hash changed.

| Situation | Command | Cost |
| :--- | :--- | :--- |
| Code changed | `graphify update .` | free — AST only, no LLM |
| Docs/markdown changed | `graphify extract . --backend claude-cli --max-concurrency 1 --token-budget 4000` | only the changed files |
| Nothing changed | *skip* — `check-update` exits 0 | none |

Confirm incremental actually engaged: the run prints
`incremental summary: N cached/unchanged, M re-extracted, K deleted`.
If `M` equals the whole corpus, the manifest gate was bypassed — check for a
stray `--force` or `GRAPHIFY_FORCE=1`.

**Never pass `--force`** unless deliberately rebuilding from scratch. It skips
the manifest gate *and* the semantic cache, re-paying the entire build.

**Backend:** `--backend claude-cli` routes through the local `claude` CLI and
bills the Claude Code plan — no `ANTHROPIC_API_KEY`, no GPU load. Measured 3×
better edge density and zero schema violations vs. a local 14B model.

**Exclusions** live in `.graphifyignore` at the workspace root. Never index
`venv/`, `node_modules/`, or `site-packages/` — they are 149k of the
workspace's 151k files. Secrets (`.env`, `*.pem`, `*credentials*.json`) are
excluded there too.

**Never set `GRAPHIFY_OLLAMA_NUM_CTX`.** It overrides graphify's auto-sizing
and over-allocates KV cache, which exhausts VRAM and slows extraction ~6×.

## 🔍 Key Paths
- **Routing map (machine):** `skills_manifest.json`
- **Skill tree (human):** `SKILL_TREE.md`
- **Schema for new skills:** `SKILL_STANDARD.md`
- **Directives:** `agent.md`
- **Map:** `WORKSPACE_INDEX.md`
- **Patterns:** `grep -r "#elite" .`

## ✅ Before Committing a Skill
The pre-commit hook does both automatically. **Install it once per clone:**
```bash
git config core.hooksPath tools/hooks
```
It regenerates `skills_manifest.json` (staging it if stale) and runs the schema
suite, blocking the commit on a validation failure. To run them by hand:
```bash
python tools/build_manifest.py   # regenerate the routing map
uv run pytest tests/             # validate every file against the schema
```

**STewardship Active:** Use this repo to build, refine, and protect the user's tools.
