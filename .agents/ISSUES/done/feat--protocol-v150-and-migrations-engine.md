---
slug: feat--protocol-v150-and-migrations-engine
type: feat
status: done
priority: critical
created: 2026-08-27
updated: 2026-08-27
completed: 2026-08-27
agent: antigravity
tags: [protocol, migration, rules, sync-history]
milestone: v1.5.0-dashboard-and-analytics
---

# Protocol v1.5.0 and Versioned Migration Engine

Implemented in commits `aa44ba7` and `044cb40` by `pavel.borodaev` and `antigravity`.

## Changes Made
- Upgraded protocol to v1.5.0 with full entity metadata ecosystem (`MILESTONES`, `RISKS`, `SPIKES`, `CHECKLISTS`, `SESSIONS`).
- Implemented versioned migration engine `skills/init-agents/migrate_protocol.py` with automatic entity synthesis and typography sanitization.
- Created Language Rule Packs in `rules/` (C#, TypeScript, JavaScript, Python, Rust).
- Built `/sync-history` skill and `analyze_git_history.py` for automated Git reconciliation.
- Added ADR #004 in `.agents/DECISIONS.md` and migration guide in `docs/MIGRATIONS.md`.
