# StoryScope Benchmarks

Reference tables for [`narrative-authenticity`](SKILL.md). Load when you need an
exact figure, want to audit one axis, or are deciding how hard to push a
constraint.

**Source.** Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer,
John Wieting. *StoryScope: Investigating idiosyncrasies in AI fiction.*
COLM 2026. arXiv:2604.03136v6. CC0. University of Maryland / Google DeepMind.

**Corpus.** 10,272 human stories from Books3, each mirrored by five LLMs
(Claude Sonnet 4.6, GPT-5.4, Gemini 3 Flash, DeepSeek V3.2, Kimi K2.5) writing to
a reverse-engineered prompt from the same premise. 61,608 stories, mean 4,753
words. 304 narrative features per story, grounded in the NarraBench taxonomy.
Feature assignment by Gemini 3 Flash (Krippendorff's α = 0.90 over 5 runs; human
validation Cohen's κ = 0.84 on 240 items).

---

## Why structure, not style

| Feature set | n | Macro-F1 | AUPRC |
| :--- | ---: | ---: | ---: |
| Narrative + Style | 304 | 96.0 | .982 |
| **Narrative only** | 257 | **93.2** | .959 |
| Core + Fingerprint | 101 | 91.1 | .934 |
| Style only | 39 | 85.8 | .867 |
| Core only | 30 | 84.8 | .828 |

Narrative features alone retain **over 97%** of the full model's performance with
every stylistic signal withheld.

**The finding that matters for revision:** stories run through LAMP span-level
rewriting — which strips cliché, purple prose and redundant exposition using
few-shot examples from professional writers — were still detected at **93.9%**
macro-F1, down just **1.6 points** from 95.5% unedited. Surface editing does not
move structure.

Six-way authorship attribution reaches 68.4% macro-F1 on narrative features alone
(16.7% chance). Human is the most separable source at 88.5% F1.

---

## Table 16 — all 30 core features

Human vs. AI means. `s` = 1–5 Likert (mean). `o` = ordinal (mean over integer
codes). `→` = prevalence % of that option. Gap = Human − AI; negative means
AI-elevated. AI column averages all five models.

### AI-elevated — thematic over-determination

| Feature | Human | AI | Gap |
| :--- | ---: | ---: | ---: |
| Thematic Explicitness & Moralizing `s` | 3.28 | 3.94 | −0.65 |
| Moral / Philosophical Weighting `s` | 3.26 | 3.68 | −0.42 |
| Thematic Unity `s` | 4.41 | 4.74 | −0.33 |
| Narratorial Thematic Commentary → yes | 52% | 77% | −25 |
| Dialogue Function → philosophical debate | 34% | 59% | −25 |
| Reference Explicitness → implicit echoes | 50% | 72% | −22 |

### AI-elevated — sensory and embodied performativity

| Feature | Human | AI | Gap |
| :--- | ---: | ---: | ---: |
| **Emotional Expression → embodied** | **38%** | **81%** | **−42** |
| Setting as Psychological Mirror `s` | 3.58 | 4.07 | −0.49 |
| Environmental & Ecological Emphasis `s` | 2.83 | 3.21 | −0.38 |
| Sensory Modalities → olfactory | 57% | 82% | −26 |
| Sensory Density `s` | 3.66 | 3.93 | −0.26 |
| Depth of Interior Access `s` | 3.67 | 3.93 | −0.26 |

Emotional Expression → embodied is the **largest single gap among all 30 core
features**.

### AI-elevated — structural streamlining

| Feature | Human | AI | Gap |
| :--- | ---: | ---: | ---: |
| Causal Chain Continuity `s` | 3.92 | 4.20 | −0.28 |
| Spatial Granularity `o` | 2.27 | 2.53 | −0.26 |
| Agency in Resolution → protagonist choice | 46% | 69% | −23 |
| Character Introduction → external description | 30% | 52% | −22 |
| Subplot Integration → no subplots | 57% | 79% | −22 |
| Pre-Threat Character Investment `s` | 2.76 | 2.99 | −0.23 |
| Resolution Mode → internal understanding | 27% | 47% | −21 |
| Opening Spatial Grounding `o` | 2.12 | 2.33 | −0.20 |

### Human-elevated — intertextual richness

| Feature | Human | AI | Gap |
| :--- | ---: | ---: | ---: |
| Intertextual Strategy → explicit named reference | 47% | 24% | +23 |
| Reference Explicitness → balanced mix | 37% | 16% | +21 |

### Human-elevated — reader engagement

| Feature | Human | AI | Gap |
| :--- | ---: | ---: | ---: |
| Fourth-Wall Permeability `o` | 0.67 | 0.39 | +0.28 |
| Direct Reader Address `o` | 0.28 | 0.07 | +0.21 |

Reported in the paper's prose as 67% vs 39% and 28% vs 7% respectively.

### Human-elevated — temporal complexity

| Feature | Human | AI | Gap |
| :--- | ---: | ---: | ---: |
| Depth of Recontextualization After Surprise `s` | 3.28 | 2.95 | +0.34 |
| Chronological Discontinuity `s` | 2.40 | 2.12 | +0.28 |
| Nonlinear Framing for Delayed Disclosure `s` | 1.96 | 1.68 | +0.28 |
| Anachrony Intensity `s` | 2.58 | 2.31 | +0.27 |

### Human-elevated — narrative diversity

| Feature | Human | AI | Gap |
| :--- | ---: | ---: | ---: |
| Location Variety Scope `o` | 1.34 | 1.08 | +0.26 |
| Dialogue-to-Narration Proportion `s` | 2.95 | 2.70 | +0.24 |
| Subplot Integration → thematically parallel | 42% | 21% | +22 |
| Moral Polarity → ambivalent / mixed | 59% | 38% | +21 |
| Emotional Expression → explicit labels | 29% | 8% | +21 |

---

## Rarity and clustering

Originality is operationalized as statistical rarity in feature space — mean
Euclidean distance to a story's 25 nearest neighbours.

| Measure | Human | AI |
| :--- | ---: | ---: |
| Mean rarity percentile (Cohen's d = 0.83) | 0.71 | 0.49 |
| Share of stories in corpus-wide rarest 10% | 24.7% | 7.1% |
| Share in rarest 1% | 3.0% | 0.6% |
| Ranked rarest of the six versions of a prompt | 57.8% | — |

Chance for that last row is 16.7%.

**The five AI models occupy one shared region.** Mean human–AI centroid distance
is **1.6×** the mean AI–AI distance (6.6 vs 4.3). The *closest* human–AI centroid
pair is farther apart than the *most distant* AI–AI pair (6.2 vs 6.0) — human
stories are not a broader version of the AI cluster, they are elsewhere. Human
dispersion is 22% greater (33.2 vs 27.4). Every one of the six most-confused
source pairs in six-way attribution is AI↔AI.

**Implication for revision.** Hitting every constraint in this skill identically
produces a new tight cluster. Dispersion is the actual target.

---

## Per-model fingerprints

Each model diverges from the other four on a distinctive feature set. Fingerprint
counts: Human 32, Claude 26, GPT 11, Gemini 11, DeepSeek 7, Kimi 3.

**Claude** — the most distinctive AI profile. Defined by restraint: event
intensity escalates less than any other source; narrative voice the most uniform.
Reverent and continuist toward literary tradition, extending conventions rather
than subverting them (62% vs 39–56% elsewhere). Favours epilogues, avoids dream
sequences, prefers quiet endings to avalanche endings.

**GPT** — socially oriented. Gossip and rumour as plot mechanism (64% vs 44–55%).
Frames stories as reflections on events years or decades past. Ensemble-heavy
social networks at human levels. Subverts expectations more than other AI (41% vs
27–36%) and leaves reconciliations ambiguous.

**Gemini** — the tidiest endings, extended denouements, bleakest settings (88%
tagged bleak and oppressive).

**DeepSeek** — front-loads crucial context that other sources withhold.

**Kimi** — fewest fingerprints, lowest attribution F1. Sits at the generic centre
of the AI distribution with no distinctive choices.

Per-class F1, narrative-only six-way model: Human 88.5, Claude 78.1, GPT 72.2,
Gemini 59.5, DeepSeek 57.4, Kimi 55.0.

---

## Caveats worth carrying

- **Human baseline is Books3** — published short fiction, literary and genre
  pooled. Not a universal standard; a thriller's causal continuity legitimately
  runs above the human mean.
- **Features were assigned by an LLM.** Reliability is high (κ = 0.84 against
  human annotators on 240 items) but it is a model reading models.
- **These are means over 61,608 stories.** No individual choice is wrong. Human
  thematic explicitness averages 3.28, not 0.
- **The prompts were reverse-engineered** from the human stories by Gemini 2.5
  Flash, so AI stories were written to a compressed premise while the human
  original was written freely. Some structural richness gap may follow from that
  asymmetry rather than from authorship.
