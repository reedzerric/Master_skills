---
name: frequency-analysis-simulation
description: Analyze historical draw or event data with pandas — parse delimited value columns into lists, build frequency counts, score combinations by rarity, and simulate outcomes — while stating plainly where the statistics do and do not support inference. Use when doing frequency analysis on lottery, dice, or sampled event data, or when a "pick the best numbers" request needs an honest answer alongside the code. For production data pipelines, use python-elite and the database skills.
version: 1.0.0
category: utilities
triggers: [frequency analysis, lottery numbers, pandas value counts, rareness score, monte carlo, simulation, historical draw data, probability exercise]
dependencies: [python-elite]
inputs: [a CSV or dataframe of historical draws, a scoring definition]
outputs: [frequency tables, scored combinations, a simulation result with caveats]
tags: [utilities, pandas, statistics, simulation, probability, data-analysis]
links: ["[[python-elite]]", "[[bigquery-elite]]"]
confidence_score: 0.9
date: 2026-08-15
task_ref: skill-consolidation
---

# Frequency Analysis & Simulation

Do the pandas work correctly and describe what it means honestly. It does ONE
thing: frequency analysis and simulation over historical draw-style data. It does
not build production pipelines (that is `[[python-elite]]` plus the database
skills), and it does not do inferential modeling.

## Operating Posture

You are a statistician who will write the code the user asked for *and* tell them
what it can support. Frequency analysis over independent events is a legitimate
and interesting exercise; presenting it as predictive is not. Both halves are
part of the deliverable — do the analysis well, and state the limit plainly once,
without moralizing.

## Hard Rules

1. **State independence once, up front, in the code.** Independent draws mean
   past frequencies carry no predictive information about future ones. Put it in
   the module docstring where anyone reading the code sees it.
2. **Never present a frequency ranking as a prediction.** "Historically least
   drawn" is a fact. "Most likely next" is not, and the two are one careless
   sentence apart.
3. **Guard every division.** Frequency denominators are zero for anything never
   observed. `1 / (count + 1)` is the standard fix and must be applied
   consistently.
4. **Never silently swallow a parse failure.** Returning an empty DataFrame from
   a bare `except Exception` turns a data bug into a wrong answer.
5. **Distinguish simulated data from real data in the code.** A mock CSV inline
   in the module is fine for an exercise, and dangerous if the caller thinks it
   is live. Name it `MOCK_` and say so.
6. **Never make this a gambling recommender.** Analysis and simulation are fine;
   staking advice is out of scope.

## Workflow

### Phase 1 — Parse

Delimited values inside a single column are the recurring shape of this data.
Split them into real lists before anything else.

```python
"""Frequency analysis over historical draws.

Draws are independent events: past results carry no information about future
ones. Anything below describes what *has* happened, never what will.
"""

import io

import pandas as pd


def load_draws(csv_text: str) -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(csv_text))
    df.columns = ["date", "numbers", "bonus", "multiplier"]
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
    df["numbers"] = (
        df["numbers"].str.split()          # split() handles runs of whitespace
        .apply(lambda parts: [int(p) for p in parts])
    )
    return df
```

Use bare `.str.split()` rather than `.str.split(" ")` — the latter produces empty
strings on double spaces, and `int("")` raises.

**Completion criterion:** every row's `numbers` is a list of ints of the expected
length. Assert it rather than assuming it.

### Phase 2 — Count

`explode` turns the list column into one row per value, which `value_counts`
then handles directly.

```python
def frequencies(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    main_counts = df["numbers"].explode().value_counts()
    bonus_counts = df["bonus"].value_counts()
    return main_counts, bonus_counts
```

**Completion criterion:** counts sum to `len(df) * numbers_per_draw`.

### Phase 3 — Score combinations

A rareness score is the sum of inverse frequencies — lower means the constituent
values have appeared more often historically.

```python
def rareness_score(
    main: list[int],
    bonus: int,
    main_counts: pd.Series,
    bonus_counts: pd.Series,
) -> float:
    """Sum of inverse historical frequencies. Descriptive, not predictive.

    Higher score = constituent values appeared less often in the sample.
    This says nothing about the next draw.
    """
    score = sum(1 / (main_counts.get(n, 0) + 1) for n in main)
    score += 1 / (bonus_counts.get(bonus, 0) + 1)
    return score
```

Note the docstring does the honest work, so callers reading only the function
signature still get the caveat.

**Completion criterion:** the score is finite for every input, including values
never observed.

### Phase 4 — Simulate

Where the exercise gets genuinely informative: generate many random draws and
show that the frequency spread in a finite sample looks exactly like the spread
in the historical data. That is the actual lesson.

```python
import numpy as np


def simulate(n_draws: int, pool: int = 69, pick: int = 5, seed: int = 0) -> pd.Series:
    rng = np.random.default_rng(seed)
    draws = [rng.choice(np.arange(1, pool + 1), size=pick, replace=False)
             for _ in range(n_draws)]
    return pd.Series(np.concatenate(draws)).value_counts()
```

Compare the min/max spread of `simulate(len(df))` against the real data. They
will be comparable — which is the point.

**Completion criterion:** the simulated spread is of the same order as the
observed spread, demonstrating that observed "hot" and "cold" numbers are
sampling noise.

### Phase 5 — Report

Present frequency tables and scores as descriptive statistics. If asked which
numbers to pick, answer directly: every combination has identical probability;
choosing rarely-picked numbers does not change odds of winning but does reduce
the chance of splitting a prize. That second clause is the only genuinely useful
result in the whole analysis.

**Completion criterion:** the report contains no forward-looking claim about
individual numbers.

## Known Quirks & Edge Cases

- **`.str.split(" ")` breaks on double spaces**, producing `''` entries that
  crash `int()`. Bare `.str.split()` splits on any whitespace run.
- **`value_counts()` omits never-observed values entirely** — they are absent,
  not zero. `.get(n, 0)` handles it; `[n]` raises `KeyError`.
- **`explode` on an empty list produces a `NaN` row**, silently skewing counts.
  Filter empty lists first.
- **A bare `except Exception: return pd.DataFrame()` is the worst failure mode
  here** — downstream code sees an empty frame, computes nothing, and reports
  success. Let parse errors raise.
- **Historical draw data changes format mid-series.** Ball pool sizes get
  expanded; the same CSV can contain draws under different rules. Check the
  observed max against the expected pool before pooling counts across years.
- **`np.random.default_rng(seed)` is reproducible; `random.choice` in a loop is
  not** without explicit seeding. Use the generator API for anything you want to
  re-run.

## Related
- [[python-elite]] — the toolchain and typing standards for this code
- [[bigquery-elite]] — when the draw history outgrows a DataFrame
