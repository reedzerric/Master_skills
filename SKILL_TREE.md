# 🌳 Master Skills — Skill Tree

The routing map. 104 skills across six categories, addressed by capability
rather than by folder.

**Machine-readable form:** [`skills_manifest.json`](skills_manifest.json) — an
agent should parse that to discover prerequisites and chain multi-step tasks.
This file is the human-readable view of the same data.

**Schema:** [`SKILL_STANDARD.md`](SKILL_STANDARD.md).
**Directory map:** [`WORKSPACE_INDEX.md`](WORKSPACE_INDEX.md).

> Category and folder are deliberately decoupled. A skill's `category` says
> what it is *for*; its path says where it *lives*. The existing
> `skills/`, `knowledgebase/`, `testing/`, and `misc/` folders are unchanged —
> this tree is a view over them, not a reorganization of them.

---

## How an agent uses this

1. **Match intent to a skill** via `trigger_index` in the manifest (469 trigger
   phrases → skill names), or by scanning `description` fields.
2. **Resolve `dependencies` first.** They are guaranteed acyclic and every edge
   resolves to a skill in the manifest — load prerequisites before the target.
3. **Check `inputs`.** If a required input is missing, that is the question to
   ask the user, not an assumption to make.
4. **Chain on `outputs` → `inputs`.** One skill's outputs feeding another's
   inputs is the composition signal.
5. **Load companions on demand.** A skill with a non-empty `companions` list
   keeps its bulk reference material there. Load `SKILL.md` first; pull in
   `RECIPES.md` or a template only when the workflow says to.

```bash
# Which skill handles this?
jq -r '.trigger_index | to_entries[] | select(.key|test("session")) | "\(.key) -> \(.value|join(", "))"' skills_manifest.json

# What must load first?
jq -r '.skills[] | select(.name=="django-auth-hardening") | .dependencies[]' skills_manifest.json

# Everything in a category
jq -r '.categories.game_design[]' skills_manifest.json
```

---

## `core` — 58 skills

Foundational reasoning, code, architecture, data, and operations. The default
bucket: if a skill is about *building software correctly*, it lives here.

Two shapes live here and they compose rather than compete. **Domain standards**
say *how to write the code*; **engineering flows** say *what to do next*. A
flow like `implement` loads whichever domain standard covers the file it is
touching.

| Domain | Skills |
| :--- | :--- |
| **Engineering flows** ᵖ | `skill-router` · `setup-engineering-flows` · `grill-with-docs` · `to-spec` · `to-tickets` · `implement` · `tdd` · `code-review` · `diagnosing-bugs` · `resolving-merge-conflicts` · `triage` · `wayfinder` · `prototype` · `research` · `domain-modeling` · `codebase-design` · `improve-codebase-architecture` · `wizard` |
| **Backend** | `python-elite` · `rust-elite` · `flask-elite` · `django-elite` · `api-contracts-elite` |
| **Auth** | `django-auth-hardening` ⁺ · `auth-ux-patterns` ⁺ |
| **Frontend** | `css-elite` · `js-html-elite` · `local-first-ai-elite` · `xstate-formalism-elite` |
| **Database** | `postgresql-elite` · `bigquery-elite` · `redis-elite` · `zero-downtime-migrations` |
| **Infrastructure** | `docker-elite` · `github-actions-elite` · `gcloud-deployment-elite` · `iac-opentofu-elite` · `serverless-edge-elite` · `observability-elite` · `chaos-engineering-elite` |
| **Testing** | `pytest-elite` · `webapp-testing` · `tla-plus-formalism` · `agentic-security-elite` |
| **Architecture** | `architectural-patterns` · `system-design-elite` · `marketplace-pattern` · `multiplayer-interruption-pattern` |
| **Security & governance** | `security-agentic-elite` · `privacy-by-design-elite` · `finops-value-elite` |
| **Operations** | `git-ops-elite` · `git-velocity-elite` · `sre-incident-protocol` |
| **Meta** | `skill-standard` · `skill-creator` · `agent-skills-spec` |

## `ai_infrastructure` — 17 skills

Retrieval, LLM pipelines, prompt chaining, agent orchestration, and the Claude
platform surface.

| Domain | Skills |
| :--- | :--- |
| **Agent orchestration** | `agent-swarms-elite` · `agent-handoff-elite` · `agent-consensus-elite` |
| **Retrieval** | `agentic-rag-elite` · `rag-content-generation` ⁺ |
| **Prompt chaining** | `product-spec-chain` ⁺ |
| **MCP** | `mcp-builder` · `mcp-deep-dive` · `evaluation-guide` |
| **Claude platform** | `claude-api` · `models` · `error-codes` · `tool-use-concepts` · `python-deep-dive` · `typescript-deep-dive` |
| **Agent tooling** | `web-artifacts-builder` · `memory-validation` |

## `game_design` — 5 skills

Game systems, economy balancing, simulation mechanics, and narrative systems.
Extracted from `Simulacri_game/` and `Duke's Demise/`; the source projects are
untouched.

| Skill | Covers |
| :--- | :--- |
| `roguelike-scoring` ⁺ | Chips × multiplier scoring, combo tables, modifier resolution order, target curves |
| `run-economy-balancing` ⁺ | Flat-vs-scaling penalties, resource caps, rarity tiers, reward curve validation |
| `narrative-event-system` ⁺ | Event JSON schema, outcome gating, weighted selection, chaining, LLM content generation |
| `social-deduction-design` ⁺ | The five psychological drives, scene-fragment clues, three story layers, offline secret distribution |

**Chain:** `roguelike-scoring` → `run-economy-balancing` → `narrative-event-system`.

## `design_media` — 7 skills

2D visual design, generative art, branding, and theming.

`frontend-design` · `canvas-design` · `algorithmic-art` · `brand-guidelines` ·
`theme-factory` · `themes` · `slack-gif-creator`

> This is the one category added beyond the originally-specified five. Forcing
> `brand-guidelines` into `creative_3d` (which is 3D) or `utilities` (which is
> tooling) would misroute it.

## `creative_3d` — 1 skill

Python-driven 3D workflows and procedural geometry.

| Skill | Covers |
| :--- | :--- |
| `blender-procedural-modeling` ⁺ | `bpy` primitive-plus-boolean construction, parametric dimensioning, dovetail joints, 3D-print sliding-fit tolerances |

## `utilities` — 16 skills

Standalone tooling: document generation, communication, thinking aids, and
one-off analysis.

| Domain | Skills |
| :--- | :--- |
| **Documents** | `docx` · `pdf` · `pptx` · `xlsx` · `document-tooling-deep-dive` |
| **Communication** | `internal-comms` · `internal-comms-deep-dive` · `doc-coauthoring` |
| **Thinking aids** ᵖ | `grilling` · `grill-me` · `handoff` · `teach` · `to-questionnaire` · `wait-what` |
| **Agent authoring** ᵖ | `writing-for-agents` |
| **Analysis** | `frequency-analysis-simulation` ⁺ |

⁺ = authored in this consolidation pass.
ᵖ = imported from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT).
See [`skills/engineering/README.md`](skills/engineering/README.md) for what was
adapted and how to re-sync.

---

## Multi-file skills

Twelve skills use progressive disclosure — `SKILL.md` holds the workflow, and
bulk reference material loads on demand. The authoritative list is the
`companions` field in the manifest:

```bash
jq -r '.skills[] | select(.companions|length>0) | "\(.name): \(.companions|join(\", \"))"' skills_manifest.json
```

| Skill | Companions |
| :--- | :--- |
| `product-spec-chain` | `PRD-TEMPLATE.md`, `UX-TEMPLATE.md`, `SRS-TEMPLATE.md` |
| `django-auth-hardening` | `RECIPES.md` |
| `skill-router` | `PHASE-BOUNDARIES.md` |
| `setup-engineering-flows` | `issue-tracker-github.md`, `issue-tracker-gitlab.md`, `issue-tracker-local.md`, `triage-labels.md`, `domain.md` |
| `codebase-design` | `DEEPENING.md`, `DESIGN-IT-TWICE.md` |
| `domain-modeling` | `ADR-FORMAT.md`, `CONTEXT-FORMAT.md` |
| `improve-codebase-architecture` | `HTML-REPORT.md` |
| `prototype` | `LOGIC.md`, `UI.md` |
| `tdd` | `tests.md`, `mocking.md` |
| `triage` | `AGENT-BRIEF.md`, `OUT-OF-SCOPE.md` |
| `teach` | `MISSION-FORMAT.md`, `GLOSSARY-FORMAT.md`, `LEARNING-RECORD-FORMAT.md`, `RESOURCES-FORMAT.md` |
| `writing-for-agents` | `SKILL-MECHANICS.md` |

---

## Cross-repository skills (not in this repo)

Real, valid Agent Skills that live with the code they operate on. Referenced
here so an agent can find them; **not** copied in, because they are coupled to
their repositories.

| Skill | Location | Purpose |
| :--- | :--- | :--- |
| `add-lang` | `codegraph/.claude/skills/add-lang/` | Wire a new tree-sitter language into codegraph end-to-end |
| `agent-eval` | `codegraph/.claude/skills/agent-eval/` | Benchmark codegraph retrieval quality with vs. without |

Upstream references kept as git clones, not vendored:

| Repository | Path | Role |
| :--- | :--- | :--- |
| `anthropics/skills` | `../skills/` | The Agent Skills spec plus 17 reference skills. `git pull` to update. |
| `mattpocock/skills` | *vendored, not cloned* | 25 process flows imported into `skills/engineering/` and `skills/productivity/` (MIT). Bodies are upstream; frontmatter is ours. Re-sync by diffing bodies only. |
| `JuliusBrussee/caveman` | `../Duke's Demise/caveman/` | Vendored OSS plugin; also installed globally at `~/.claude/plugins/`. |

---

## Validation

```bash
uv run pytest tests/          # 23 tests, incl. a repo-wide schema check
```

`tests/test_validator.py::test_repository_is_valid` validates every skill file
in the repository against `SKILL_STANDARD.md`. It fails the build on a missing
required field, a non-canonical `category`, a non-semver `version`, or a `name`
that does not match its path.

Regenerate the manifest after adding or renaming a skill — a stale manifest
routes agents to paths that no longer exist.
