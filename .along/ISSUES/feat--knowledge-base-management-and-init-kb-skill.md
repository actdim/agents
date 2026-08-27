---
protocol: along
slug: knowledge-base-management-and-init-kb-skill
type: feat
status: open
priority: high
created: 2026-08-26
updated: 2026-08-26
agent: antigravity
tags: [kb]
milestone: v1.5.0-dashboard-and-analytics
blocked_by: []
related: []
---

# Knowledge Base Management Standards & `/along-init-kb` Skill

## Goal
Establish clear guidelines in the `AGENTS.md` protocol for creating and maintaining a structured, human- and agent-readable **Knowledge Base (KB)** (`.along/KB/` or `docs/`), and implement the **`/along-init-kb`** skill to bootstrap or refresh the Knowledge Base from existing `README.md`, `AGENTS.md`, and codebase structure.

## Proposed Integration Details

### 1. Knowledge Base Guidelines in `AGENTS.md` Protocol
- Define standard KB structure in `.along/KB/`:
  - `INDEX.md` (Central entry point and cross-linked topic map)
  - `01-architecture.md` (System components, flows, and boundaries)
  - `02-domain-model.md` (Domain concepts, terms, and data schemas)
  - `03-setup-and-workflow.md` (Build, run, test instructions, and dev workflows)
- Enforce KB maintenance rules: whenever non-trivial features or architecture changes are implemented, agents must update the corresponding KB article in `.along/KB/`.

### 2. Standalone Skill: `/along-init-kb` (`skills/along-init-kb/SKILL.md`)
- Command `/along-init-kb`: Scans existing `README.md`, `AGENTS.md`, and codebase.
- Bootstraps `.along/KB/` with structured articles (`INDEX.md`, `01-architecture.md`, `02-domain-model.md`, `03-setup-and-workflow.md`).
- Automatically cross-links terms and syncs with `/along-sync-kb`.

## Acceptance Criteria
- [ ] Protocol updated with Knowledge Base management guidelines.
- [ ] `/along-init-kb` skill created in `skills/along-init-kb/SKILL.md`.
- [ ] Skill deployed globally via `install.ps1`.

