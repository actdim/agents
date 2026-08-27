---
protocol: along
slug: universal-project-version-bumping-and-along-scripts
type: feat
status: done
priority: high
created: 2026-08-27
updated: 2026-08-27
completed: 2026-08-27
agent: antigravity
tags: [release, version-bumping, scripts, automation, along-scripts]
milestone: v2.0.0-along-transition
blocked_by: []
related: [feat--bump-version-skill-and-typography-sanitizer]
---

# Universal Project Version Bumping & Repository Scripts Ecosystem (`.along/scripts/`)

## Goal
Transform `/along-bump-version` into a universal, multi-stack release engine that can increment versions and execute release lifecycles in ANY project (Node/TS, Python, Rust, .NET, Go, or custom). Establish the `.along/scripts/` directory convention for project-specific automation scripts, with auto-detection, script synthesis, and graceful interactive fallbacks.

## Accomplishments
1. **Universal Release Engine (`scripts/along_bump_version.py`)**:
   - Executes custom `.along/scripts/bump_version.py` if present.
   - Auto-detects Node.js (`package.json`, `package-lock.json`), Python (`pyproject.toml`), Rust (`Cargo.toml`), and generic `VERSION` files.
   - Auto-synthesizes `.along/scripts/bump_version.py` on first run for transparent project-specific maintenance.
   - Supports `actdim/along` development mode for protocol sync.
   - Provides clear diagnostic templates when custom stacks cannot be determined.
2. **Directory Standard (`.along/scripts/`)**:
   - Formally designated `.along/scripts/` for repository-tailored helper executables and release hooks.
3. **Skill & ADR #009**:
   - Updated `skills/along-bump-version/SKILL.md` with multi-stack usage.
   - Documented architectural decision in `.along/DECISIONS.md`.

