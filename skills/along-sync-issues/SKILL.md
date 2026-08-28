---
name: along-sync-issues
description: Reconcile the nearest .along/ issue board (ISSUES.md) and per-issue files (ISSUES/<type>--<slug>.md) for the target subproject/area - create/update issue files with status/priority and protocol: along in the nearest .along/, keep the board accurate, and move completed issues to ISSUES/done/. Use when invoking /along-sync-issues.
---

# Along Sync Issues (`/along-sync-issues`) [v2.0.10]

Maintains `.along/ISSUES.md` and `.along/ISSUES/<type>--<slug>.md` files with strict YAML front-matter (`protocol: along`).
