---
protocol: along
slug: 03-setup-and-workflow
title: Setup, Installation, and Agent Workflow
type: setup-workflow
created: 2026-08-27
updated: 2026-08-28
tags: [setup, install, workflow, lifecycle, cli, slash-commands]
---

# Along Setup, Installation, and Workflow Guide

---

## 1. Installation

Along skills and rules can be installed for any supported AI coding tool:

### Windows (PowerShell / Batch)
```powershell
# Install into all providers (Claude Code, Codex, OpenCode, Antigravity)
powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1 -Target all

# Or install for a specific provider
powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1 -Target antigravity
powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1 -Target claude
```

### Linux / macOS (Bash)
```bash
# Install into all detected host tools
bash install.sh
```

---

## 2. Standard Agent Session Workflow

```text
1. Read Context -> 2. Work & Auto-track -> 3. Quality Gate -> 4. Wrap Session
   (AGENTS.md,         (Create/edit issues     (Tests & lint,     (/along-wrap,
    CONTEXT.md,         as needed in            clean ASCII)       bump version,
    ISSUES.md,          .along/ISSUES/)                            commit & push)
    DECISIONS.md)
```

### Step 1: Session Initialization
At the start of every session, read the nearest context files:
1. `AGENTS.md`: Repository conventions and active protocol.
2. `.along/CONTEXT.md`: Snapshot of active status.
3. `.along/ISSUES.md`: Current issue board.
4. `.along/DECISIONS.md`: Architectural decisions and constraints.

### Step 2: Intent Recognition & Working
- Non-trivial features or bugs trigger automated creation of `.along/ISSUES/<type>--<slug>.md`.
- Library dependencies with AI rules can be scanned via `/along-scan-deps`.

### Step 3: Stage Wrap-up & Release
When wrapping up work:
1. Execute unit tests (`python -m unittest discover -s tests`).
2. Run typography sanitizer (`python scripts/sanitize_typography.py`).
3. Complete entity reconciliation (move finished issues to `done/`).
4. Generate session log in `.along/SESSIONS/`.
5. Bump version via `/along-bump-version` (or `python scripts/along_bump_version.py patch -c`).

---

## 3. Skills Quick Reference

| Skill / Command | Execution Command | Description |
| :--- | :--- | :--- |
| `/along-init` | `along-init` | Scaffolds or refreshes `.along/` and `AGENTS.md`. |
| `/along-dash` | `python scripts/along_dash.py -w` | Launches dynamic FastAPI dashboard on port 8765. |
| `/along-scan-deps` | `python skills/along-scan-deps/along_scan_deps.py` | Scans dependencies for AI guidelines (`AGENTS.md`, `llms.txt`). |
| `/along-bump-version` | `python scripts/along_bump_version.py patch` | Increments version across manifests and files. |
| `/along-commit` | `python skills/along-commit/along_commit.py` | ASCII sanitizer, pre-commit test gate, and conventional committer. |
| `/along-sync-kb` | `along-sync-kb` | Synchronizes Knowledge Base articles and topic index. |
