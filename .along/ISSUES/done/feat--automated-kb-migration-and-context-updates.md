---
protocol: along
slug: automated-kb-migration-and-context-updates
type: feat
status: done
completed: 2026-08-31
priority: high
created: 2026-08-31
updated: 2026-08-31
agent: antigravity
tags: [kb]
milestone: v2.1.0-along
blocked_by: []
related: []
---

# Automated KB Migration to docs/ & .archive/, Recursive Monorepo Context Updates & Protocol Modernization

Implement reliable, automatic migration of legacy `.along/KB/` and unmanaged notes to `docs/topic--<slug>.md` and `.archive/`, recursive context traversal in `along_update.py`, purge of obsolete `.along/CONTEXT.md`, and clean script resolution across the along suite.

## Acceptance Criteria
- [x] `scripts/migrate_protocol.py` updated to scaffold directly into `docs/` instead of legacy `.along/KB/`.
- [x] `scripts/migrate_protocol.py` safely executes `along_kb_sync` via proper script resolution, purges `.along/CONTEXT.md`, and cleans up `.along/KB/`.
- [x] `scripts/along_kb_sync.py` maps legacy `01-*.md` files, archives unstructured notes to `.archive/`, compiles clean `docs/topic--*.md`, and purges `.along/KB/` and `.along/CONTEXT.md`.
- [x] `scripts/along_update.py` runs post-update syncs recursively across all discovered agent contexts and detects uninitialized subprojects.
- [x] Added `test_14_legacy_kb_and_context_migration` and `test_15_along_update_multi_context_and_uninit_subprojects`.
- [x] 100% test pass rate across 28 automated tests.
