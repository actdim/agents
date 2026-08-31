---
protocol: along
slug: concurrency-projections-and-context-deprecation
type: feat
status: done
completed: 2026-08-31
priority: high
created: 2026-08-31
updated: 2026-08-31
agent: antigravity
tags: [protocol, concurrency, git, adr, memory]
milestone: v2.2.0-along
blocked_by: []
related: []
---

# Multi-Branch Concurrency, Projections, Context Deprecation & ADR Migration

## Summary
Implements Along Protocol v2.2.0 architectural upgrades:
1. Eliminated git merge conflicts by classifying `ISSUES.md` and `docs/INDEX.md` as Derived Projections with zero-manual-merge rule.
2. Added `.gitattributes` configuring `merge=union` for append-only files (`HISTORY.md`, `DECISIONS.md`).
3. Completely deprecated and removed `CONTEXT.md` as an obsolete global state bottleneck.
4. Migrated all 15 past ADRs in `DECISIONS.md` to decentralized slug format `ADR-YYYY-MM-DD--<slug>`.
5. Enforced Mandatory Issue Anchoring in `AGENTS.md` before making source code edits.

## Acceptance Criteria
- [x] `.gitattributes` created with `merge=union` for `HISTORY.md` and `DECISIONS.md`.
- [x] `CONTEXT.md` removed from repo, startup reading list, and wrap checklist.
- [x] All 15 ADRs in `DECISIONS.md` converted to `ADR-YYYY-MM-DD--<slug>`.
- [x] `along_exec.py` updated with `status`, `doctor`, `issue sync`, and slug-based `decision create`.
- [x] All 25 unit tests verified passing.

