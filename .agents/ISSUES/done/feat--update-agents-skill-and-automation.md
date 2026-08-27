---
slug: update-agents-skill-and-automation
type: feat
status: done
priority: high
created: 2026-08-27
updated: 2026-08-27
completed: 2026-08-27
agent: antigravity
tags: [skills, updater, cli]
milestone: v1.5.0-dashboard-and-analytics
blocked_by: []
related: [feat--entity-relationships-and-dependency-graph, feat--project-dashboard-and-analytics-skill]
---

# Feature: `/update-agents` One-Liner Skill & Auto-Update Engine

## Goal
Implement a one-liner skill (`/update-agents`) and cross-platform update engine (`update_agents.py`) that checks protocol versions across the local repository, globally installed agent skills, and GitHub (`https://github.com/actdim/agents.git`), automatically upgrading global skills if outdated and migrating the target project repository.

## Requirements
- Create `scripts/update_agents.py` and `skills/update-agents/update_agents.py`.
- Create skill definition `skills/update-agents/SKILL.md`.
- Implement version comparisons (repo vs global vs remote) with network timeouts and offline fallback.
- Support dev-repo safe mode when executed inside `actdim-agents` repository.
- Ensure strict clean ASCII compliance.
