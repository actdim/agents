---
name: along-bump-version
description: Increment repository version (patch by default), sanitize typography, execute wrap-session reconciliation, deploy global installation, and create a release git commit. Use when finalizing work or when the user invokes /along-bump-version.
---

# Along Bump Version (`/along-bump-version`) [v2.0.1]

Automates version bumping, clean ASCII typography verification, global installation deployment, and release git commit.

## Usage
```bash
python scripts/bump-version.py patch
python scripts/bump-version.py minor
python scripts/bump-version.py major
```
