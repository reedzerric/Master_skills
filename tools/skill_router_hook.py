"""UserPromptSubmit hook: route a prompt to Master Skills via the trigger index.

Reads the Claude Code hook payload on stdin, scores the prompt against every
phrase in `skills_manifest.json`'s `trigger_index`, and emits pointers to the
best-matching skills as injected context.

Deterministic and cheap: the harness runs this before the model sees the turn,
so a matching skill is surfaced whether or not the model would have thought to
look. Injects nothing when nothing matches — silence is the common case and
noise on every prompt would be worse than no hook at all.

Never fails loudly. Any error exits 0 with no output; a broken router must not
break the session.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MANIFEST = Path(__file__).resolve().parent.parent / "skills_manifest.json"

#: Minimum fraction of a trigger's content tokens that must appear in the prompt.
#: 0.6 means a 3-token trigger needs 2, a 4-token trigger needs 3, and a 2-token
#: trigger needs both. Lower admits noise; higher misses paraphrases.
THRESHOLD = 0.6

#: Never inject more than this many skills, however many match.
MAX_SKILLS = 3

#: Dropped before scoring — present in most prompts, so they carry no signal.
STOPWORDS = frozenset("""
a an the is are was were be been being am do does did doing have has had
my me i we our you your it its this that these those to for of in on at by
with from about as and or but if then than so how what why when where which
can could should would will shall may might must need want get got make
please help hey ok okay
""".split())

_WORD = re.compile(r"[a-z0-9+.#-]+")


def tokens(text: str) -> set[str]:
    """Lowercase content tokens, stopwords removed."""
    return {w for w in _WORD.findall(text.lower()) if w not in STOPWORDS}


def score_triggers(prompt_tokens: set[str], trigger_index: dict) -> dict[str, float]:
    """Best trigger score per skill name."""
    best: dict[str, float] = {}
    for phrase, skills in trigger_index.items():
        content = tokens(phrase)
        if not content:
            continue
        hit = len(content & prompt_tokens) / len(content)
        if hit < THRESHOLD:
            continue
        for skill in skills:
            if hit > best.get(skill, 0.0):
                best[skill] = hit
    return best


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    prompt = (payload or {}).get("prompt") or ""
    if not prompt.strip():
        return

    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception:
        return

    prompt_tokens = tokens(prompt)
    if not prompt_tokens:
        return

    scored = score_triggers(prompt_tokens, manifest.get("trigger_index", {}))
    if not scored:
        return

    by_name = {s["name"]: s for s in manifest.get("skills", [])}
    # Rank by trigger score, then prefer the more specific (longer) description.
    ranked = sorted(
        (n for n in scored if n in by_name),
        key=lambda n: (-scored[n], -len(by_name[n].get("description", ""))),
    )[:MAX_SKILLS]
    if not ranked:
        return

    root = MANIFEST.parent
    lines = [
        "Master Skills matched this prompt. Read the relevant file(s) below "
        "before answering, and prefer their standards over training defaults:",
        "",
    ]
    # Deliberately not surfacing `dependencies`: the graph currently contains
    # cycles and several nonsense edges (postgresql-elite -> rust-elite), so a
    # "load first" note would be misleading on every prompt. Restore once the
    # dependency lists have been audited.
    for name in ranked:
        lines.append(f"- `{name}` — {root / by_name[name]['path']}")
    lines.append("")
    lines.append(
        "If a skill turns out not to apply, ignore it and say nothing about it."
    )

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "\n".join(lines),
        },
        "suppressOutput": True,
    }))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
