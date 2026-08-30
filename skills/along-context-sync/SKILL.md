---
name: along-context-sync
description: Refresh the nearest .along/CONTEXT.md into a short, accurate current-state snapshot ("you are here"). Use when updating/saving context or when invoking /along-context-sync (aliases: /context-sync, /along-sync-context).
---

# Along Context Sync (`/along-context-sync`, `/context-sync`) [v2.1.1]

Keeps the nearest `.along/CONTEXT.md` compact (< 20 lines) and strictly focused on current focus, active issues, and immediate next steps.

## Scope & Placement
- Always update `.along/CONTEXT.md` in the **NEAREST** component/submodule/subproject directory corresponding to the active work.
- In multi-package or submodule repositories, never default context updates to the workspace root if the work was performed in a specific subproject.

## Usage
- Command: `/along-context-sync` (aliases: `/context-sync`, `/along-sync-context`)
