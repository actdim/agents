---
name: along-update
description: Check and update Along protocol and skills to the latest version across local repository, global installation, and GitHub. Cleans up legacy un-namespaced skills. Use when the user asks to update agents/along, upgrade the repository protocol, or invokes /along-update.
---

# Along Update (`/along-update`) [v2.1.2]

One-liner update engine for `Along` and `ALONG-PROTOCOL`.

## When to use
1. The user invokes `/along-update` or asks to upgrade/sync skills from GitHub.
2. Opening an existing project to ensure it is running the latest `ALONG-PROTOCOL` standard across all subprojects.

## Execution
```bash
python scripts/along_update.py
```
