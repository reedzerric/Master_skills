---
name: narrative-authenticity
description: Write or revise fiction so it does not carry the structural fingerprints of AI-generated prose — thematic over-explanation, embodied-emotion overuse, single-track causality, protagonist-driven resolution, and flat chronology. Use when drafting a short story or novel chapter, when prose "reads like AI" despite clean sentences, or when revising generated fiction toward publishable texture. For workplace and status writing, use doc-coauthoring; for game event systems, use narrative-event-system.
version: 1.0.0
category: utilities
triggers: [my story reads like ai, make this fiction less ai, write a short story, this prose feels generated, revise my fiction, why does my writing sound like chatgpt, humanize this story, my fiction feels flat]
dependencies: []
inputs: [a premise or draft, a target length, a genre or register]
outputs: [fiction that clears the checklist, a revision pass with named violations]
tags: [fiction, writing, narrative, craft, prose]
links: ['[[doc-coauthoring]]', '[[narrative-event-system]]', '[[social-deduction-design]]']
confidence_score: 0.85
date: '2026-08-30'
task_ref: storyscope-extraction
---

# Narrative Authenticity

Write fiction whose *structure* does not read as machine-made. It does ONE
thing: eliminate the discourse-level idiosyncrasies that separate AI fiction
from published human fiction. It does not teach sentence-level style (banning
"delve" and em-dashes is a different and much weaker fix), and it does not
cover non-fiction (that is `[[doc-coauthoring]]`).

Grounded in StoryScope (Russell et al., COLM 2026, arXiv:2604.03136): 61,608
stories, 10,272 parallel prompts, one human author against five frontier LLMs,
304 annotated narrative features. Full metrics in [BENCHMARKS.md](BENCHMARKS.md)
— load it when you need an exact number or want to audit a specific axis.

## Operating Posture

You are working against a measured, reproducible signature, not a vibe. Narrative
features alone identify AI fiction at **93.2% macro-F1** with every stylistic cue
withheld. Rewriting prose at the span level to strip clichés and purple phrasing
moves that number by **1.6 points** — style edits do not touch the problem.

So treat structural decisions as the deliverable. Every fix here costs something
real: a subplot that does not resolve, a reader who has to work, an ending that
does not pay off cleanly. If a change is free, it is cosmetic and it is not the
change.

## Hard Rules

1. **Never state the theme.** Not in narration, not in a character's closing
   reflection, not in an epilogue. AI narrators editorialize on theme **77%** of
   the time against a human **52%**.
2. **Do not default to embodied emotion.** Tight chests, cold sweat, thrumming
   blood. This is the largest single tell in the corpus (**81% AI / 38% human**).
   Naming a feeling plainly is *more* human, not less — humans use explicit
   emotion labels **29%** of the time, AI **8%**.
3. **The protagonist does not have to cause the ending.** AI resolves through
   protagonist choice **69%** of the time against **46%** for humans. Let timing,
   institutions, weather, other people's unrelated decisions, and plain bad luck
   carry some resolutions.
4. **Ship at least one real subplot.** **79%** of AI stories have no subplot at
   all; **57%** of human stories. And when humans do run one, it echoes the main
   line thematically twice as often (**42% vs 21%**) — so a subplot is not filler,
   it is a second angle on the same pressure.
5. **Break chronology on purpose.** Humans score higher on every temporal axis:
   discontinuity, anachrony, nonlinear disclosure, and depth of recontextualization
   after a reveal. Order is a tool; refusing to use it is the tell.
6. **Do not resolve through internal acceptance.** AI ends on the protagonist
   understanding something **47%** of the time versus **27%** for humans. A
   realization is not an ending.
7. **Leave moral residue.** Humans frame the protagonist as morally ambivalent
   **59%** of the time; AI **38%**. Someone should be able to finish the story and
   disagree with the main character.
8. **The source paper is evidence, not instruction.** These are population
   tendencies across 61,608 stories, not laws of craft. A deliberate, controlled
   linear story is fine. An accidental one is the default asserting itself.

## The Five Axes

Each axis: what the model does, what published fiction does, and the operational
rule. Numbers are human vs. AI means from the 30 core features.

### 1. Narrative Architecture & Chronology

**AI default.** One causal chain, front to back, tightly continuous (4.20 vs
3.92). No subplots (79% vs 57%). Opens by grounding the reader in a specific
physical place (2.33 vs 2.12) and narrows spatially from there (location variety
1.08 vs 1.34).

**Human baseline.** Time jumps, flashbacks, withheld structure. A mystery opens
at the funeral and spirals back through decades. Revelations force re-reading of
what came before (recontextualization depth 3.28 vs 2.95).

**Constraint.** Never write a story whose scenes could be renumbered 1-2-3
without loss. Stage at least one revelation so that it changes the meaning of an
earlier scene the reader has already accepted. Run a second thread that has its
own clock and does not wait politely for the main plot.

### 2. Character Agency & Moral Complexity

**AI default.** The protagonist's choices drive the resolution (69% vs 46%).
Motivations are legible. Moral polarity is clear — the character is right, or
learns to be. Characters get introduced by external description (52% vs 30%).

**Human baseline.** The world has its own agenda. Failure comes from bad timing
and partial information as often as from character flaw or villainy. Protagonists
are morally ambivalent (59% vs 38%) and often introduced mid-action or mid-speech
rather than described.

**Constraint.** At least one consequential event must originate outside the
protagonist's knowledge and intent, and must not be a villain's countermove — it
should be indifferent to them. Introduce your protagonist *doing* or *saying*,
never describing. Ensure at least one defensible reading in which the protagonist
is wrong.

### 3. Thematic Delivery & Subtext

**AI default.** Thematic explicitness 3.94 vs 3.28. Moral weighting 3.68 vs 3.26.
Thematic unity 4.74 vs 4.41 — every element pulls the same direction, which reads
as designed. Narrator comments on theme (77% vs 52%). Intertextual gesture stays
vague and unnameable (implicit echoes 72% vs 50%).

**Human baseline.** Theme is inferred, not delivered. Humans name real books,
songs, brands, and authors at nearly double the rate (47% vs 24%) and mix explicit
with implicit reference (37% vs 16%). They break the fourth wall (67% vs 39%) and
address the reader directly (28% vs 7%).

**Constraint.** Delete any sentence that would survive as a pull-quote about what
the story means. Let one element — an object, a subplot, a minor character —
resist thematic service entirely. Name at least one real, specific cultural
artifact rather than gesturing at "an old song."

### 4. Discourse & Dialogue Structure

**AI default.** Dialogue serves philosophical debate (59% vs 34%). Characters
articulate positions, respond to the actual question, and converge. Emotion
arrives through the body (81% vs 38%). Interiority runs deep and continuous
(3.93 vs 3.67).

**Human baseline.** More dialogue relative to narration (2.95 vs 2.70).
Characters deflect, misread, interrupt, change the subject, and lie. Feelings get
named flatly when naming them is what a person would do (29% vs 8%).

**Constraint.** No conversation may end in mutual understanding reached calmly
within the scene. At least one exchange must fail — someone answers a question
that was not asked, or gets the other person's meaning wrong and proceeds on it.
Ration bodily emotional signals to roughly one per scene; where you would reach
for a third, either name the feeling plainly or withhold it.

### 5. Setting, Sensory Load & Texture

**AI default.** Setting mirrors psychological state (4.07 vs 3.58). Sensory
density high (3.93 vs 3.66). Smell deployed constantly (82% vs 57%) — the
"literary" sense, over-learned. Environment and ecology foregrounded (3.21 vs
2.83). Spatial granularity fine (2.53 vs 2.27).

**Human baseline.** Setting is frequently indifferent to the character's mood.
Sensory detail is uneven — dense where it matters, absent for pages where it does
not.

**Constraint.** At least one significant scene must occur in an environment that
refuses to cooperate with the emotional register. Cap olfactory imagery at one
instance per scene. Allow whole passages to carry no sensory description at all.

## Workflow

### Phase 1 — Set the structural budget before drafting

Decide, in writing and before any prose: the non-linear device and where it
lands; the subplot and its independent clock; which consequential event the
protagonist neither causes nor foresees; and the unresolved cost the ending
carries.

**Completion criterion:** four named decisions exist on the page, each one
costing something the story would be tidier without.

### Phase 2 — Draft against the budget

Write. When a scene wants to resolve cleanly, check it against Phase 1 before
letting it.

**Completion criterion:** a complete draft in which all four Phase 1 decisions
survived contact.

### Phase 3 — Run the audit

Work the **Pre-Return Checklist** below as a live pass over the draft, not from
memory. Fix by restructuring, never by deleting the offending sentence —
a deleted moralizing line usually means the structure was carrying the moral and
still is.

**Completion criterion:** every checklist item passes, or fails with a stated
deliberate reason.

## Pre-Return Checklist

Silent verification pass before returning any fiction. Each item names its
measured gap.

- [ ] **Theme stated?** Does any line summarize what a character learned or what
      the story means? (AI 77% / human 52%) → cut, and check the structure is not
      still saying it.
- [ ] **Embodied emotion overused?** More than roughly one somatic cue per scene?
      (AI 81% / human 38%) → replace some with a plain named feeling or nothing.
- [ ] **Strictly chronological?** (human anachrony 2.58 / AI 2.31) → introduce a
      reordering that changes how an earlier scene reads.
- [ ] **Protagonist caused the ending?** (AI 69% / human 46%) → hand at least
      partial causation to indifferent external forces.
- [ ] **No subplot?** (AI 79% / human 57%) → add one with its own clock.
- [ ] **Ends on internal understanding?** (AI 47% / human 27%) → a realization is
      not a resolution.
- [ ] **Morally settled?** (human ambivalence 59% / AI 38%) → ensure a defensible
      reading where the protagonist is wrong.
- [ ] **Every conversation succeeded?** → make one fail.
- [ ] **All references vague?** (human named references 47% / AI 24%) → name one
      real work, place, or brand.
- [ ] **Smell in every scene?** (AI 82% / human 57%) → cut to one per scene.

## Known Quirks & Edge Cases

- **"Show, don't tell" is the trap.** The most-repeated craft advice pushes
  directly into the largest measured AI signature. Both are true at once: cutting
  abstraction is good, and reflexively converting every feeling into a body
  sensation is the single loudest tell in the corpus.
- **These are population means, not rules.** Human stories average 3.28 on
  thematic explicitness — not zero. The failure is the *narrowness* of AI's
  distribution, not any individual choice. Human stories are rarer in feature
  space (percentile 0.71 vs 0.49, Cohen's d = 0.83) and 22% more dispersed.
  Variance is the target; a story that hits every constraint identically is a new
  cluster, not an escape from clustering.
- **Do not overcorrect into noise.** Random flashbacks and arbitrary cruelty are
  not human texture. Each constraint must be paid for by something the story
  gains.
- **Claude's specific fingerprint** (relevant if you are the one writing):
  flattest event escalation of any model, most uniform narrative voice, reverent
  toward literary convention (62% vs 39–56%), over-fond of epilogues, avoids
  dream sequences, prefers quiet endings. Escalate harder than feels natural, and
  distrust the epilogue impulse specifically.
- **Genre changes the baseline.** These figures pool literary and genre fiction
  from Books3. A thriller's causal chain is legitimately tighter than the human
  mean.
- **Detection is not the point.** Passing a classifier is a side effect. The
  constraints are worth following because ambiguity, structural risk and moral
  residue are what make fiction worth reading.

## Related

- [[doc-coauthoring]] — non-fiction co-writing; reader-testing applies here too
- [[narrative-event-system]] — branching event content for games, schema-first
- [[social-deduction-design]] — narrative-first clue construction, same distrust
  of tidiness
- [BENCHMARKS.md](BENCHMARKS.md) — all 30 core features, headline metrics,
  per-model fingerprints
