---
name: along-decision-sync
description: Record architectural/design decisions into the nearest .along/DECISIONS.md as append-only ADR entries, and mark superseded ones. Use when a non-trivial technical choice was made, or invokes /along-decision-sync.
---

# Along Decision Sync  [v2.1.4]

Maintains append-only Architectural Decision Records (ADRs) in the nearest `.along/DECISIONS.md`.

## Scope & Placement
- Always record ADRs in the **NEAREST** `.along/DECISIONS.md` for the subproject, module, or submodule being architected.
- Root `.along/DECISIONS.md` is reserved for system-wide or cross-package architectural decisions.

## Usage
- Command: `/along-decision-sync`
