---
protocol: along
protocol_version: 2.2.5
slug: link-rewriting-and-integrity-gate
type: feat
status: done
priority: high
created: 2026-08-31
updated: 2026-08-31
completed: 2026-08-31
agent: antigravity
tags: [protocol, kb, links, integrity, migrations]
milestone: v2.0.0-along-transition
blocked_by: []
related: []
---

# Feature: Inbound Link Rewriting, Link Integrity Gate & Header Deduplication

## Summary
Add automated Inbound Link Rewriting and Global Link Integrity Gate across the entire repository hierarchy (including monorepo packages), fix duplicated protocol header comment markers in `AGENTS.md`, and record `protocol_version` metadata in entity front-matter schemas.

## Tasks
- [x] Create implementation plan and obtain approval.
- [x] Fix protocol header de-duplication in `scripts/along_update.py` and `scripts/migrate_protocol.py`.
- [x] Implement `rewrite_inbound_links()` and `validate_repo_link_integrity()` in `scripts/along_kb_sync.py`.
- [x] Update `scripts/migrate_protocol.py` Step 7 to perform inbound link rewriting and integrity verification before deleting legacy folders.
- [x] Update `skills/along-init/protocol.md` and `AGENTS.md` with Stable Entry Point Rule, Monorepo Scope Rule, and Link Integrity Gate in checklist.
- [x] Update `skills/along-kb-sync/SKILL.md`, `skills/along-wrap/SKILL.md`, and `skills/along-update/SKILL.md`.
- [x] Verify test suite and repository link integrity.

