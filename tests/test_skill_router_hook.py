"""Tests for the UserPromptSubmit skill-routing hook.

This hook runs on every prompt in every project, so a silent break is expensive
and invisible. These tests cover the two failure modes that matter: routing the
wrong way (noise injected, or a real match missed), and crashing the turn.

The subprocess tests exercise the script exactly as settings.json invokes it.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "tools" / "skill_router_hook.py"


def run_hook(payload, cwd=None):
    """Invoke the hook as the harness does; return (returncode, parsed|None)."""
    proc = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload) if payload is not None else "",
        capture_output=True,
        text=True,
        cwd=str(cwd or ROOT),
    )
    out = proc.stdout.strip()
    return proc.returncode, (json.loads(out) if out else None)


def context_of(parsed):
    return parsed["hookSpecificOutput"]["additionalContext"]


def skills_in(parsed):
    """Skill names from the injected pointer lines."""
    return [
        line.split("`")[1]
        for line in context_of(parsed).splitlines()
        if line.startswith("- `")
    ]


# --- routing: real prompts must hit the right skill ------------------------

@pytest.mark.parametrize(
    "prompt,expected",
    [
        ("my postgres query is slow, which index should i add", "postgresql-elite"),
        ("my docker image is too big", "docker-elite"),
        ("my mock is not working in pytest", "pytest-elite"),
        ("we have a production incident", "sre-incident-protocol"),
        ("write a commit message for this", "git-ops-elite"),
        ("help me write a short story", "narrative-authenticity"),
    ],
)
def test_expected_skill_is_routed(prompt, expected):
    code, parsed = run_hook({"prompt": prompt})
    assert code == 0
    assert parsed is not None, f"no match for {prompt!r}"
    assert expected in skills_in(parsed)


# --- silence: noise must not be injected -----------------------------------

@pytest.mark.parametrize(
    "prompt",
    [
        "what is the weather today",
        "yes",
        "add two numbers in javascript",
        "thanks, that worked",
        "",
        "   ",
    ],
)
def test_unrelated_prompts_inject_nothing(prompt):
    code, parsed = run_hook({"prompt": prompt})
    assert code == 0
    assert parsed is None, f"unexpected injection for {prompt!r}"


# --- failing open: a broken router must never break the turn ---------------

@pytest.mark.parametrize(
    "stdin_text",
    ["", "not json at all", "[]", "null", '{"no_prompt_key": 1}'],
)
def test_malformed_input_exits_clean(stdin_text):
    proc = subprocess.run(
        [sys.executable, str(HOOK)],
        input=stdin_text,
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert proc.returncode == 0
    assert proc.stdout.strip() == ""


def test_works_from_any_working_directory(tmp_path):
    """settings.json is global, so the hook runs from arbitrary cwd."""
    code, parsed = run_hook({"prompt": "my docker image is too big"}, cwd=tmp_path)
    assert code == 0
    assert parsed is not None
    assert "docker-elite" in skills_in(parsed)


# --- output contract -------------------------------------------------------

def test_output_shape_and_encoding():
    # Binary mode on purpose: the ASCII assertion below inspects raw bytes.
    proc = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps({"prompt": "my postgres query is slow"}).encode(),
        capture_output=True,
        cwd=str(ROOT),
    )
    raw = proc.stdout.strip()
    assert all(b < 128 for b in raw), "output must be ASCII-safe for cp1252 consoles"

    parsed = json.loads(raw)
    hso = parsed["hookSpecificOutput"]
    assert hso["hookEventName"] == "UserPromptSubmit"
    assert isinstance(hso["additionalContext"], str)
    assert parsed["suppressOutput"] is True


def test_pointer_paths_exist_on_disk():
    code, parsed = run_hook({"prompt": "my postgres query is slow"})
    assert parsed is not None
    for line in context_of(parsed).splitlines():
        if line.startswith("- `"):
            path = Path(line.split("—", 1)[1].strip())
            assert path.is_file(), f"routed to a path that does not exist: {path}"


# --- trace file ------------------------------------------------------------

def _run_with_trace(tmp_path, prompt, create_log):
    """Run the hook with HOME redirected so the real trace file is untouched."""
    import os

    env = dict(os.environ, HOME=str(tmp_path), USERPROFILE=str(tmp_path))
    log = tmp_path / ".claude" / "skill-router.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    if create_log:
        log.touch()
    proc = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps({"prompt": prompt}),
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        env=env,
    )
    assert proc.returncode == 0
    return log


def test_trace_is_off_unless_the_log_file_exists(tmp_path):
    """The hook must never create files on its own."""
    log = _run_with_trace(tmp_path, "my docker image is too big", create_log=False)
    assert not log.exists()


def test_trace_records_both_hits_and_misses(tmp_path):
    """A miss must be logged too, or it cannot be told from a hook that never ran."""
    log = _run_with_trace(tmp_path, "my docker image is too big", create_log=True)
    assert "docker-elite" in log.read_text(encoding="utf-8")

    log = _run_with_trace(tmp_path, "what is the weather today", create_log=True)
    lines = [l for l in log.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert any("\t-\t" in l for l in lines), "a miss must still leave a trace line"


def test_never_exceeds_max_skills():
    """A prompt stuffed with trigger words must still stay bounded."""
    from importlib import util

    spec = util.spec_from_file_location("skill_router_hook", HOOK)
    mod = util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    manifest = json.loads((ROOT / "skills_manifest.json").read_text(encoding="utf-8"))
    every_trigger = " ".join(manifest["trigger_index"])
    code, parsed = run_hook({"prompt": every_trigger})
    assert code == 0
    assert parsed is not None
    assert len(skills_in(parsed)) <= mod.MAX_SKILLS
