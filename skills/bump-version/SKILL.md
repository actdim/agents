---
name: bump-version
version: "1.5.5"
description: Increment repository version (patch by default), sanitize typography, execute wrap-session reconciliation, deploy global installation, and create a release git commit. Use when finalizing work or when the user invokes /bump-version.
---

# Bump Version & Release (`/bump-version`) [v1.5.5]

Automate the atomic patch bump, session finalization, global installation sync, and Git commit.

---

## 🎯 When to Use

1. The user asks to bump version, finalize changes, and commit (e.g., "bump patch", "увеличь версию и сделай коммит", `/bump-version`).
2. Completing a batch of features or fixes that should be released under a new patch version.

---

## 🛠️ Execution Workflow

### Step 1: Sanitize Typography & Invisible Characters
Ensure zero non-ASCII typographic pollutants (em-dashes, en-dashes, curly quotes, invisible spaces) exist in code or docs:
```bash
python scripts/sanitize_typography.py .
```

### Step 2: Session & Board Reconciliation
1. Verify that all finished issues are moved to `.agents/ISSUES/done/`.
2. Ensure `.agents/SESSIONS/<YYYY>/` log file reflects the latest work.
3. Refresh `.agents/ISSUES.md`, `.agents/HISTORY.md`, and `.agents/CONTEXT.md`.

### Step 3: Increment Version
Run the automated multi-file version synchronization helper:
```bash
python scripts/bump-version.py patch
```
*(Or pass `minor`, `major`, or a specific version like `1.5.3` if requested by user).*

### Step 4: Re-deploy Global Installations
Synchronize updated skills and rules across all global agent directories:
- **Windows**:
  ```powershell
  powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1 -Target all
  ```
- **Linux / macOS**:
  ```bash
  bash install.sh
  ```

### Step 5: Atomic Git Commit
Stage all modifications and create a structured conventional commit:
```bash
git add -A
git commit -m "bump(version): vX.Y.Z - <summary of changes>"
```
