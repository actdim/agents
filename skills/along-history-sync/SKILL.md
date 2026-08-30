---
name: along-history-sync
description: Reconstruct and reconcile .along/ project history (ISSUES, MILESTONES, SESSIONS) from Git commits, tags, and PRs. Use when initializing on an existing git repo or when the user invokes /along-sync-history.
---

# Along Sync History (`/along-sync-history`) [v2.1.1]

Analyzes Git commits, tags, and PRs to synthesize missing `.along/` entities (`ISSUES/done/`, `MILESTONES/`, `SESSIONS/`, `HISTORY.md`) with `protocol: along`.
