---
name: along-history-sync
description: Reconstruct and reconcile .along/ project history (ISSUES, MILESTONES, SESSIONS) from Git commits, tags, and PRs. Use when initializing on an existing git repo or when invoking /along-history-sync (aliases: /history-sync, /along-sync-history).
---

# Along History Sync (`/along-history-sync`, `/history-sync`) [v2.1.1]

Analyzes Git commits, tags, and PRs to synthesize missing `.along/` entities (`ISSUES/done/`, `MILESTONES/`, `SESSIONS/`, `HISTORY.md`) with `protocol: along`.

## Scope & Placement
- Reconciles Git history in the **NEAREST** `.along/` directory for the active repository or Git submodule.

## Usage
- Command: `/along-history-sync` (aliases: `/history-sync`, `/along-sync-history`)
