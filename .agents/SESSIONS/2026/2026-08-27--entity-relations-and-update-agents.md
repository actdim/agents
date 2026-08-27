---
date: 2026-08-27
slug: entity-relations-and-update-agents
agent: antigravity
branch: main
commit: pending
summary: Implemented entity relationship metadata (blocked_by, related, parent), DAG validation & cycle detection, and automated /update-agents skill.
milestone: v1.5.0-dashboard-and-analytics
issues_advanced: []
issues_completed: [feat--entity-relationships-and-dependency-graph, feat--update-agents-skill-and-automation]
decisions: [ADR-2026-08-27-entity-relationships-and-unidirectional-storage]
risks_logged: []
spikes_conducted: []
---

# Session: Entity Relationships & /update-agents Skill

## Summary
- Introduced structured metadata fields (`blocked_by`, `related`, `parent`) for issues and entities in `ACTDIM-AGENTS-PROTOCOL`.
- Established canonical slug linking invariant (ensuring links survive moves into `done/`).
- Added graph validation and DFS cycle detection on `blocked_by` DAG to `migrate_protocol.py`.
- Developed `/update-agents` one-liner skill and `scripts/update_agents.py` CLI engine for 3-way version detection (repo vs global vs remote git) and automated global/repo upgrades.
- Integrated `update-agents` into `install.ps1`, `install.sh`, `scripts/bump-version.py`, `README.md`, and `AGENTS.md`.

## Files Touched
- `AGENTS.md`
- `README.md`
- `install.ps1`
- `install.sh`
- `scripts/bump-version.py`
- `scripts/migrate_protocol.py`
- `scripts/update_agents.py`
- `skills/init-agents/SKILL.md`
- `skills/init-agents/protocol.md`
- `skills/init-agents/migrate_protocol.py`
- `skills/sync-issues/SKILL.md`
- `skills/update-agents/SKILL.md`
- `skills/update-agents/update_agents.py`
- `.agents/ISSUES.md`
- `.agents/ISSUES/done/feat--entity-relationships-and-dependency-graph.md`
- `.agents/ISSUES/done/feat--update-agents-skill-and-automation.md`

