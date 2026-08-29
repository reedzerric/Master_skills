# 🗺️ Master Workspace Cognitive Index

This index is the **directory map** — what lives where on disk.

For **capability routing** — which skill handles a given task, and what must
load first — use [`SKILL_TREE.md`](SKILL_TREE.md) or parse
[`skills_manifest.json`](skills_manifest.json) directly. Category and folder are
decoupled: a skill's `category` says what it is for, its path says where it
lives.

Every skill file conforms to [`SKILL_STANDARD.md`](SKILL_STANDARD.md); the
schema is enforced by `uv run pytest tests/`.

## 📂 /skills/ - Actionable Processes
*How to build things with 2026-level precision.*

| Domain | Key Memories | Purpose |
| :--- | :--- | :--- |
| **Backend** | `python-elite.md`, `flask-elite.md`, `rust-elite.md`, `api-contracts-elite.md` | uv/ruff standards, App Factory, Async Tokio, OpenAPI/gRPC. |
| **Frontend** | `css-elite.md`, `js-html-elite.md`, `local-first-ai-elite.md`, `xstate-formalism-elite.md` | Subgrid/Layers, Temporal API, WebGPU AI, Actor Model logic. |
| **Infra** | `docker-elite.md`, `github-actions-elite.md`, `serverless-edge-elite.md`, `agent-swarms-elite.md`, `agent-handoff-elite.md`, `chaos-engineering-elite.md`, `iac-opentofu-elite.md` | Distroless, OIDC CI/CD, Edge AI, MAS Orchestration, Handoff Protocols, Resilience. |
| **Database** | `postgresql-elite.md`, `bigquery-elite.md`, `redis-elite.md`, `zero-downtime-migrations.md` | AIO/UUIDv7, Cost-first SQL, TTL Jitter, Expand-Contract. |
| **Documents** | `pdf.md`, `xlsx.md`, `docx.md`, `pptx.md` | Specialized document extraction and creation. |
| **Media** | `frontend-design.md`, `theme-factory.md`, `algorithmic-art.md`, `brand-guidelines.md`, `slack-gif-creator.md`, `canvas-design.md` | Anti-AI-slop design, Branding, Generative Art. |
| **Engineering** | `skill-router/`, `grill-with-docs/`, `to-spec/`, `to-tickets/`, `implement/`, `tdd/`, `code-review/`, `diagnosing-bugs/`, `wayfinder/`, `triage/`, +8 more | Process flows: idea → spec → tickets → build → review. Start at `skill-router`. See [`skills/engineering/README.md`](skills/engineering/README.md). |
| **Productivity** | `grilling/`, `grill-me/`, `handoff/`, `teach/`, `to-questionnaire/`, `wait-what/`, `writing-for-agents/` | Thinking and communication aids, mostly user-invoked. See [`skills/productivity/README.md`](skills/productivity/README.md). |

> The two folders above hold **process** skills — *what to do next*. Everything
> else in `/skills/` holds **domain standards** — *how to write the code*. They
> stack: `implement` and `tdd` load the domain standard for whatever file they
> are touching. Both are imported from
> [mattpocock/skills](https://github.com/mattpocock/skills) (MIT).

## 📂 /knowledgebase/ - Factual References
*Architectural decisions, theorems, and immutable facts.*

| Category | Key Memories | Purpose |
| :--- | :--- | :--- |
| **Architecture** | `architectural-patterns.md`, `system-design-elite.md`, `agent-consensus-elite.md` | DDD, Hexagonal, PACELC, Cell-based design, Adjudicator Pattern. |
| **Security** | `security-agentic-elite.md`, `privacy-by-design-elite.md` | OWASP Agentic Top 10, Zero-Trust, Cryptographic Shredding. |
| **Business** | `finops-value-elite.md`, `claude/models.md` | FOCUS standards, Unit Economics, LLM Tiers. |

## 📂 /testing/ - Validation Rules
*Mathematical verification and test-driven standards.*

| Type | Key Memories | Purpose |
| :--- | :--- | :--- |
| **Formalism** | `tla-plus-formalism.md` | Mathematical verification of distributed logic. |
| **Unit/Int** | `pytest-elite.md`, `webapp-testing.md`, `agentic-security-elite.md` | Mocker patterns, Playwright, Autonomous security audits. |

## 📂 /misc/ - Operations
*Semantic workflows and incident response.*

| Type | Key Memories | Purpose |
| :--- | :--- | :--- |
| **Git** | `git-ops-elite.md`, `git-velocity-elite.md` | Semantic commits, Trunk-Based Dev, Stacked PRs (Graphite). |
| **SRE** | `sre-incident-protocol.md` | Automated response, Blameless Post-Mortems, SLO-as-Code. |

---

## 🛠️ How to Search
If you are looking for a specific topic, use `grep_search` across the root:
- `grep -r "pattern" .` to find specific code snippets.
- `grep -r "#tags" .` to find domain-specific memories (e.g., `#backend`, `#distributed`).
- `grep -r "confidence_score: 1.0" .` to find the most battle-tested protocols.

## 📂 Domains added in the consolidation pass

| Folder | Contents |
| :--- | :--- |
| `/game_design/` | `roguelike-scoring`, `run-economy-balancing`, `narrative-event-system`, `social-deduction-design` |
| `/ai_infrastructure/` | `product-spec-chain/` (multi-file), `rag-content-generation` |
| `/creative_3d/` | `blender-procedural-modeling` |
| `/utilities/` | `frequency-analysis-simulation` |
| `/tools/` | `build_manifest.py` — regenerates `skills_manifest.json` |
| `/tools/hooks/` | `pre-commit` — blocks commits on a stale manifest or an invalid skill file |

## 🔄 How to Expand
1. Author the file against [`SKILL_STANDARD.md`](SKILL_STANDARD.md) — the
   hybrid schema (`name`, `description`, `version`, `category` required).
2. Link it to related skills with `[[wiki-links]]` and `dependencies`.
3. Regenerate and validate — the pre-commit hook does this for you once
   installed (`git config core.hooksPath tools/hooks`, once per clone):
   ```bash
   python tools/build_manifest.py
   uv run pytest tests/
   ```

`/.templates/standard-memory.md` is the legacy memory template, superseded by
`SKILL_STANDARD.md` for anything that is a skill.
