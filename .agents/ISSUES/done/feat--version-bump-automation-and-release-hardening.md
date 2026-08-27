---
slug: feat--version-bump-automation-and-release-hardening
type: feat
status: done
priority: medium
created: 2026-08-26
updated: 2026-08-26
completed: 2026-08-26
agent: git-reconstructed
tags: [git-sync, release, versioning]
milestone: v1.3.0-knowledge-base-and-graph
blocked_by: []
related: []
---

# Version Bump Automation and Release Hardening

Reconstructed from Git commits `20f5d78`, `fdd1957`, `2663434`, `2e25970`, `0f6f101`, and `4a8f968` by `pavel.borodaev`.

## Changes Made
- Created `scripts/bump-version.py` helper script for safe 2-step version synchronization.
- Performed versioning audit and hardened protocol documentation across releases v1.3.1, v1.3.2, and v1.3.3.
- Replaced non-English text strings in skill markdown documentation.
- Configured explicit MCP tool references across all skill definitions.
