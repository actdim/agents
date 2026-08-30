---
protocol: along
slug: 03-setup-and-workflow
title: Setup, Installation & Agent Workflows
type: setup-workflow
created: 2026-08-30
updated: 2026-08-30
tags: [setup, workflow, installation, lifecycle, quality-gates]
---

# Setup, Installation & Agent Workflows

Instructions for installing Along, configuring host AI providers, and following the standard session lifecycle.

---

## 1. Installation

Along provides automated installer scripts for all major operating systems:

### Windows (PowerShell)
\\powershell
powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1 -Target all
\
### Linux / macOS (Bash)
\\ash
bash install.sh --target=all
\
### Targets
- claude: Installs to ~/.claude/skills/
- codex: Installs to ~/.codex/skills/
- opencode: Generates commands in ~/.config/opencode/commands/
- antigravity: Installs to ~/.gemini/config/skills/
- all (default): Installs and configures all four host environments simultaneously.

---

## 2. Standard Session Lifecycle (Execute in Order)

1. **Session Start**: Read nearest AGENTS.md, .along/CONTEXT.md, .along/ISSUES.md, and .along/DECISIONS.md.
2. **Active Work & KB Search**: Search docs/ using along-kb-search before loading large files. Track work in .along/ISSUES/<type>--<slug>.md.
3. **Verification**: Run automated unit tests with quiet flags (along-test) and inspect blast radius with code-review-graph.
4. **Session Wrap**: Close completed issues (move to ISSUES/done/), compile docs/ with along-kb-sync, write SESSIONS/ log, and update CONTEXT.md.
5. **Version Bump & Release**: Run along-version-bump patch -cp to increment version, verify pre-commit test gates, and create release commit.
