# Context Snapshot (2026-08-31)

## Repository State
- **Along Protocol**: `v2.1.5`
- **Active Area**: Deterministic CLI entity management, multi-agent blackboard memory, and PowerShell escaping resilience.
- **Key Modules**: `scripts/along_exec.py`, `.along/`, `skills/along-team/`, `skills/along-wrap/`, `tests/`.

## Current Status
- Added native CLI entity management (`issue`, `session`, `decision`, `scratch`) to `scripts/along_exec.py`.
- Enforced deterministic command execution rule in `AGENTS.md` to prevent PowerShell escaping errors.
- Codified Session-Scoped Blackboard layout and lifecycle (`.along/.session/<slug>/`) with automated GC in `along-wrap`.
- Enforced strict 4-part role contracts and 5-point Reviewer rubric in `skills/along-team/SKILL.md`.
- All 18 automated tests passing (`python -m unittest discover tests -v`).

