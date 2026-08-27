---
protocol: along
slug: unified-wrap-lifecycle-and-commit-skills
type: feat
status: done
priority: high
created: 2026-08-27
updated: 2026-08-27
completed: 2026-08-27
agent: antigravity
tags: [skills, lifecycle, along-wrap, along-commit, along-build, along-test, along-dev]
milestone: v2.0.0-along-transition
blocked_by: []
related: [feat--universal-project-version-bumping-and-along-scripts]
---

# Unified `/along-wrap`, Smart `/along-commit`, and Lifecycle Skills Suite (`/along-build`, `/along-test`, `/along-dev`)

## Goal
Consolidate redundant session/stage wrap skills into a single **`/along-wrap`** command, introduce the smart **`/along-commit`** tool for ASCII-safe and issue-linked Conventional Commits, and deploy the non-destructive project lifecycle execution suite (**`/along-build`**, **`/along-test`**, **`/along-dev`**) powered by `.along/scripts/`.

## Accomplishments
1. **Unified `/along-wrap` (`skills/along-wrap/SKILL.md`)**:
   - Merged `along-wrap-session` and `along-wrap-stage` into a single canonical skill and command.
   - Purged legacy separate wrap folders from global registries via installers and updater.
2. **Smart Committer (`scripts/along_commit.py` & `skills/along-commit/SKILL.md`)**:
   - Pre-commit typography clean check.
   - Auto-extracted active issue from `.along/ISSUES.md` and appended issue reference.
   - Formatted Conventional Commits.
3. **Non-Destructive Lifecycle Suite (`scripts/along_exec.py`)**:
   - Implemented `/along-build`, `/along-test`, and `/along-dev` skills with auto-discovery and lazy script synthesis in `.along/scripts/` (`# Status: verified` / `# Status: unconfigured`).
4. **`along-bump-version` Refinement**:
   - Safe disk update by default; commits only when `--commit` (`-c`) is specified.
5. **ADR #010**:
   - Architectural decision logged in `.along/DECISIONS.md`.

