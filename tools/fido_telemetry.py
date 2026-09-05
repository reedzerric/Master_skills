"""
🐕 Fido Telemetry & Latency Baseline Tracker
Measures end-to-end duration across all perception and action milestones:
- Speech/Prompt to Action (T_dispatch)
- Window & Element Perception (T_perceive)
- Cursor Trajectory Movement (T_move)
- Hardware Click/Input Execution (T_act)
- Total End-to-End Latency (T_total)
Stores persistent JSONL logs to compute baselines, running averages, and regression stats.
"""

import sys
import os
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

TOOLS_DIR = Path(__file__).resolve().parent
LOG_FILE = TOOLS_DIR / "cache" / "fido_telemetry_baseline.jsonl"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


class LatencyTracker:
    def __init__(self, action_name: str = "interaction"):
        self.action_name = action_name
        self.start_time = time.perf_counter()
        self.milestones: Dict[str, float] = {}
        self.last_time = self.start_time

    def mark(self, stage_name: str) -> float:
        """Record timestamp for a milestone and return delta in milliseconds from previous mark."""
        now = time.perf_counter()
        delta_ms = (now - self.last_time) * 1000.0
        self.milestones[stage_name] = round(delta_ms, 2)
        self.last_time = now
        return delta_ms

    def finish(self, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Finish tracking, compute total latency, and persist record."""
        total_ms = (time.perf_counter() - self.start_time) * 1000.0
        record = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "action": self.action_name,
            "total_ms": round(total_ms, 2),
            "stages_ms": self.milestones,
            "metadata": metadata or {},
        }
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
        except Exception:
            pass
        return record


def get_baseline_stats() -> Dict[str, Any]:
    """Calculate running statistics across all recorded interactions."""
    if not LOG_FILE.exists():
        return {"total_runs": 0, "avg_total_ms": 0.0}

    runs = []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    runs.append(json.loads(line))
    except Exception:
        return {"total_runs": 0}

    if not runs:
        return {"total_runs": 0}

    totals = [r["total_ms"] for r in runs if "total_ms" in r]
    avg_total = sum(totals) / len(totals) if totals else 0.0
    min_total = min(totals) if totals else 0.0
    max_total = max(totals) if totals else 0.0

    return {
        "total_runs": len(runs),
        "avg_total_ms": round(avg_total, 2),
        "min_total_ms": round(min_total, 2),
        "max_total_ms": round(max_total, 2),
        "last_run": runs[-1] if runs else None,
    }


def format_telemetry_table(record: Dict[str, Any]) -> str:
    """Render crisp Markdown table of latency breakdown for user reports."""
    stages = record.get("stages_ms", {})
    total = record.get("total_ms", 0.0)

    lines = [
        "| Stage | Latency | Share |",
        "| :--- | :--- | :--- |",
    ]
    for stage, ms in stages.items():
        pct = (ms / total * 100.0) if total > 0 else 0.0
        lines.append(f"| **{stage.replace('_', ' ').title()}** | {ms:.1f} ms | {pct:.1f}% |")

    lines.append(f"| **Total End-to-End** | **{total:.1f} ms** | 100.0% |")
    return "\n".join(lines)


if __name__ == "__main__":
    stats = get_baseline_stats()
    print("🐕 Fido Telemetry Baseline Statistics:")
    print(json.dumps(stats, indent=2))
