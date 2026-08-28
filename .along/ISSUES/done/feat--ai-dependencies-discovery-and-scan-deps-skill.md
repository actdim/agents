---
protocol: along
slug: ai-dependencies-discovery-and-scan-deps-skill
type: feat
status: done
priority: medium
created: 2026-08-27
updated: 2026-08-28
completed: 2026-08-28
agent: antigravity
tags: [skills, dependencies, kb, discovery]
milestone: v1.3.0-knowledge-base-and-graph
blocked_by: []
related: []
---

# Feature: AI Dependencies Discovery and along-scan-deps Skill

## Goal
Implement a provider-agnostic scanner and skill `along-scan-deps` (`/along-scan-deps`) that inspects declared dependencies (Node/pnpm/npm, Python, Rust/Cargo), identifies library AI guidelines (`AGENTS.md`, `CLAUDE.md`, `llms.txt`, `package.json` metadata), and builds an idempotent reference catalog in `.along/KB/dependencies.md`.

## Accomplishments
1. **Engine Implementation**: Created `skills/along-scan-deps/along_scan_deps.py` supporting Node (`package.json`), Python (`pyproject.toml`, `requirements.txt`), and Rust (`Cargo.toml`).
2. **Skill Definition**: Created `skills/along-scan-deps/SKILL.md` with CLI options (`--check`, `--json`, `--quiet`, `--root`).
3. **Idempotent Registry**: Generates `.along/KB/dependencies.md` and links it in `.along/KB/INDEX.md`. Automatically purges stale dependencies when re-run.
4. **Installer Integration**: Updated `install.ps1`, `install.sh`, and `install.bat` to package `along_scan_deps.py` for OpenCode and other providers.
5. **Automated Testing**: Created and passed unit test suite in `tests/test_scan_deps.py`.

