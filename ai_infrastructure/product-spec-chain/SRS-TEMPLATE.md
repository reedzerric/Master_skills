# Software Requirements Specification Template

Load during Phase 3. Input is the PRD **and** the UX document. Emit as
`software-specifications.md`.

Questions to resolve before generating:
- Expected scale at launch and at 12 months (users, requests, data volume)
- Hosting constraints (existing cloud account, on-prem, edge)
- Non-negotiable technology (a language the team knows, a DB already in use)
- Budget ceiling, if any — it changes the architecture

---

## System Overview

One paragraph restating what is being built, from an engineering perspective.
Then a component diagram or bulleted component list: what runs where.

## Technology Stack

State each choice **and the reason**. A stack list without rationale gets
second-guessed in review.

| Layer | Choice | Why |
| :--- | :--- | :--- |
| Language / runtime | | |
| Framework | | |
| Database | | |
| Auth | | |
| Hosting / deploy | | |
| Background jobs | | |

Defaults worth arguing from: `uv` + `ruff` for Python, PostgreSQL 18 with
UUIDv7 keys, Docker distroless images, GitHub Actions with OIDC (no long-lived
secrets).

## Data Model

Every entity, its fields with types, and its relationships. Mark which fields
are indexed and why. Note any field carrying PII — it affects retention and
logging.

## API Surface

Every endpoint: method, path, request shape, response shape, auth requirement,
and error cases. If the frontend is the only consumer, say so — it changes
whether this needs to be a stable public contract.

## Authentication & Authorization

The flow end to end. Session storage, token lifetime, refresh strategy, and the
permission model (roles? per-resource ACLs? owner-only?). Name the specific
attacks being defended against.

## Non-Functional Requirements

- **Performance:** target latencies for the paths that matter
- **Availability:** what uptime is actually required, and what degradation is acceptable
- **Security:** transport, at-rest encryption, secret management, dependency policy
- **Observability:** what is logged, what is traced, what alerts fire

## Deployment & Environments

Environments, how code reaches each, migration strategy, and rollback plan.
Zero-downtime migrations use expand-contract: add the new column, backfill,
switch reads, then drop the old one — never in one deploy.

## Testing Strategy

What is unit-tested, what is integration-tested, what is end-to-end tested, and
where the line sits. State the coverage bar and whether it gates merge.

---

## Risks & Open Questions

Each risk: what could go wrong, how likely, and what the mitigation or the
decision point is.
