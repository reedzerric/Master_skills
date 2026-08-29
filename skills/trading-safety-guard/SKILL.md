---
name: trading-safety-guard
description: Mandatory persistent safety constraints and execution boundaries for automated trading agents. Enforces per-trade caps, daily volume ceilings, position book deduplication, -10% crash filters, and options bans.
version: 1.0.0
category: core
---


# Trading Safety Guard Skill

This skill defines non-negotiable, persistent execution safety rules for all automated trading processes and agent operations. These constraints survive conversation compaction and must be strictly validated before any order is submitted to a broker.

## 🛑 1. Per-Trade Dollar Cap
- **Hard Maximum Order Size**: No single order may exceed **$15,000.00** (15% single-name equity cap on a $100,000 account) or the strategy-configured `max_position_size_usd`.
- Any order exceeding the notional cap must be immediately rejected by the risk engine.

## 🛑 2. Daily Aggregate Trade-Volume Cap
- **Daily Volume Ceiling**: Total cumulative notional turnover across all orders in a single trading session must not exceed **$100,000.00** (1.0x total account equity).
- Once the daily volume ceiling is reached, the execution engine enters a passive hold state until the next session open.

## 🛑 3. Mandatory Position Book Pre-Check (Anti-Deduplication)
- Before dispatching any order, the agent/bot MUST query the active broker position snapshot and open order list.
- **Rule**: If a long position is already held or a pending buy order is active for symbol `S`, duplicate buy orders for `S` are **STRICTLY PROHIBITED**.

## 🛑 4. -10% Single-Day Crash Circuit Filter
- **Catastrophic Shock Gate**: The bot is strictly forbidden from placing buy orders on any symbol that is down **$\ge 10.0\%$** on the current trading day.
- Catches earnings blowups, fraud halts, and idiosyncratic bankruptcy cascades.

## 🛑 5. Hard Ban on Options & Complex Derivatives
- **Equity-Only Invariant**: The bot is strictly restricted to whole/fractional shares of vetted US large-cap equities and broad index ETFs.
- Orders for options contracts (calls, puts, spreads), futures, OTC pink sheets, or leveraged inverse decay instruments are **HARD BANNED**.
