# Context Snapshot (2026-08-31)

## Repository State
- **Along Protocol**: `v2.1.3`
- **Active Area**: Skills audit, lifecycle hooks standardization, and deterministic agent execution.
- **Key Modules**: `.along/scripts/`, `scripts/`, `skills/`, `dashboard/`, `package.json`.

## Current Status
- Standardized project lifecycle hooks in `.along/scripts/` (`test.py`, `dev.py`, `build.py`).
- Eliminated test discovery crashes on `dashboard.api` by isolating imports.
- Synchronized script duplicates across `scripts/` and `skills/` (`along_version_bump.py`, `along_update.py`).
- Declared explicit deterministic lifecycle commands in `package.json`, `AGENTS.md`, and `SKILL.md` manifests.
- All 15 unit tests passing (`python .along/scripts/test.py` or `python -m unittest discover tests -q`).

