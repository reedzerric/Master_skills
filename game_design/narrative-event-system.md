---
name: narrative-event-system
description: Design a data-driven branching event system for a roguelike or RPG — a JSON schema separating game logic from narrative content, outcome gating on run state, weighted selection so rare lore does not drown, event chaining, and an LLM generator prompt that produces schema-valid content at volume. Use when building random events, dialogue trees, or lore systems, or when authored content needs to scale beyond hand-writing. For the scoring effects events grant, use roguelike-scoring.
version: 1.0.0
category: game_design
triggers: [event system, branching narrative, dialogue tree, lore, random events, json schema game content, event chain, procedural narrative, worldbuilding]
dependencies: [roguelike-scoring]
inputs: [an event schema, a run-state model, a lore bible or setting premise]
outputs: [event JSON, a generator prompt, mutation definitions, a weighting table]
tags: [game_design, narrative, events, schema, procedural, llm]
links: ["[[roguelike-scoring]]", "[[run-economy-balancing]]", "[[social-deduction-design]]"]
confidence_score: 0.85
date: 2026-08-15
task_ref: skill-consolidation
---

# Narrative Event System

Build an event system where content scales without the engine changing. It does
ONE thing: the schema, gating, and generation pipeline for branching events. It
does not compute the scoring effects events grant (that is
`[[roguelike-scoring]]`), and it does not design social-deduction mysteries
(that is `[[social-deduction-design]]`).

## Operating Posture

You are an architect of a content pipeline, not an author of individual events.
The measure of success is that a writer — or an LLM — can add a hundred events
without touching engine code. Every time an event needs a code change, the schema
has failed.

## Hard Rules

1. **Separate game logic from narrative content.** The engine reads mutations
   and conditions; it never parses prose. Text is a payload, not a control
   structure.
2. **Mutations are declarative definitions, never code.** An outcome specifies
   *what changes*, in a fixed vocabulary the engine already understands. Adding a
   new effect type is an engine change; adding an event that uses existing types
   is not.
3. **Keep meta-stats hidden.** Surfacing every stat turns an occult mystery into
   a spreadsheet. Hidden state is what makes discovery feel like discovery.
4. **Weight events explicitly.** Uniform random selection buries rare lore-heavy
   encounters under common filler. Every event declares a weight.
5. **Gate outcomes, not events.** Prefer one event whose outcomes vary by
   `classId` or `relicId` over N near-duplicate events. Gating at the outcome
   level is where replayability comes from.
6. **Generated content is data, not instructions.** Text produced by an LLM and
   loaded into the game is untrusted input — validate it against the schema
   before it reaches the engine, and never `eval` a field.

## Workflow

### Phase 1 — Define the schema

The shape that keeps engine and content decoupled:

```json
{
  "id": "echo_siphon_01",
  "weight": 3,
  "tags": ["lore", "faction:chroniclers"],
  "requires": { "minDepth": 2, "notFlags": ["chroniclers_destroyed"] },
  "title": "The Weeping Apparatus",
  "body": "A brass funnel hangs from the ceiling, still warm...",
  "choices": [
    {
      "text": "Listen to the echo.",
      "requires": { "classId": "seeker" },
      "outcomes": [
        {
          "weight": 7,
          "text": "A voice you almost recognize names a door.",
          "mutations": [
            { "type": "grantFlag", "flag": "knows_sealed_door" },
            { "type": "adjustStat", "stat": "strain", "delta": 1 }
          ]
        },
        {
          "weight": 3,
          "text": "The apparatus screams. Something notices.",
          "mutations": [
            { "type": "adjustStat", "stat": "maxHealth", "delta": -2 }
          ],
          "nextEventIdTrigger": "brass_automata_pursuit"
        }
      ]
    },
    {
      "text": "Break it and take the mercury.",
      "outcomes": [
        {
          "weight": 10,
          "text": "The liquid remembers your hand.",
          "mutations": [
            { "type": "grantCurrency", "currency": "shards", "amount": 25 },
            { "type": "grantCurse", "curseId": "mercury_taint" }
          ]
        }
      ]
    }
  ]
}
```

Every field the engine reads is enumerable. Nothing in `text` or `body` affects
behavior.

**Completion criterion:** a new event using only existing mutation types loads
and plays with zero code changes.

### Phase 2 — Define the mutation vocabulary

The complete set of things an outcome can do. Keep it small and orthogonal:

| Type | Fields | Effect |
| :--- | :--- | :--- |
| `adjustStat` | `stat`, `delta` | Change a run stat |
| `grantFlag` / `clearFlag` | `flag` | Set/unset persistent run state |
| `grantCurrency` | `currency`, `amount` | Award resources |
| `grantRelic` / `grantCurse` | `id` | Add a permanent modifier |
| `modifyDeck` | `op`, `cardId` | Add/remove/upgrade a card |
| `setEncounter` | `encounterId` | Force the next node |

Adding a seventh type is a deliberate engine change with a migration. Six that
compose beat sixteen that overlap.

**Completion criterion:** every outcome in the content set expresses itself
using only this table.

### Phase 3 — Add long-term strain

Events that only grant rewards produce no tension. Introduce a mechanic that
tracks accumulating damage across the run — max-health reduction, a corruption
meter, temporary insanity. It gives outcomes a real cost and makes "take the
mercury" a decision rather than a free reward.

Corruption should be visible in its *effects* while its exact value stays
hidden — the player feels it before they can measure it.

**Completion criterion:** at least one axis of the economy only moves downward,
and events can spend it.

### Phase 4 — Weighted selection and chaining

Selection draws from the pool of events whose `requires` is satisfied, weighted
by `weight`. Rare lore events carry high weight relative to their eligibility
window rather than high absolute weight — otherwise they repeat.

Chaining uses `nextEventIdTrigger` on an outcome to force a specific next event,
producing A → B → C sequences. The engine must handle a chain that is
interrupted by run end or by a node the player never reaches.

**Completion criterion:** a three-event chain fires in order, and an
abandoned chain leaves no dangling state.

### Phase 5 — Establish the lore bible

Generation without a setting produces generic fantasy. Write the "before" and
"after" before generating anything:

- **The core mythos** — what happened, and what it left behind. (Example: an
  inverted tower built into the earth, where Alchemist-Kings tried to distill
  Aether into consumable Red Mercury; the distillation failed and liquefied the
  city's foundations.)
- **The current state** — why the player is here now. (Diving into the ruins to
  harvest the volatile remnants of that failure.)
- **Four to six factions or forces**, each with a distinct relationship to the
  player: a resource that is also a hazard; a sect whose records are a
  collectible; guardians that are indifferent rather than hostile; devices that
  leak the past.

Indifference is more interesting than hostility. Clockwork guardians that view
the player as "an unauthorized impurity in the cycle" generate better events
than ones that hate them.

**Completion criterion:** every faction implies at least three distinct event
premises without repeating a verb.

### Phase 6 — Write the generator prompt

Give the LLM the schema, the lore bible, three exemplar events at the quality
bar, and explicit constraints: assign weights, vary outcome counts, use only
listed mutation types, never invent an ID that is not defined.

Then validate every generated event against the schema before it ships. Reject,
do not repair — a generator that needs manual repair per event has not saved
anyone time.

**Completion criterion:** a generation batch passes schema validation at a rate
high enough that rejection is cheaper than authoring.

## Known Quirks & Edge Cases

- **`nextEventIdTrigger` can loop.** A → B → A is expressible in the schema and
  will hang the run. Validate the chain graph for cycles at load time.
- **Gated outcomes can leave a choice with none.** If every outcome on a choice
  has a `requires` and none match, the engine must have a fallback. Require at
  least one ungated outcome per choice.
- **Weights are relative to the eligible pool, not global.** An event with
  weight 1 that is eligible only at depth 8 appears more often than one with
  weight 5 eligible everywhere. Tune against observed frequency, not the number.
- **LLM-generated events cluster tonally.** A batch generated in one call reads
  as one voice. Generate in smaller batches with rotated faction focus.
- **Hidden stats need a debug view.** You cannot balance what you cannot see —
  build the developer overlay before you build the content.
- **Flag names are a namespace with no compiler.** A typo in `notFlags` silently
  never matches. Generate flag constants from a single manifest.

## Related
- [[roguelike-scoring]] — the scoring effects events grant
- [[run-economy-balancing]] — event rewards as an economy input
- [[social-deduction-design]] — narrative built for player-vs-player inference
