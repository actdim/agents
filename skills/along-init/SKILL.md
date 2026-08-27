---
name: along-init
description: Scaffold or refresh the provider-agnostic agent-context structure in a repository - root AGENTS.md (with a managed block carrying the ALONG-PROTOCOL v2.0.8), a CLAUDE.md that imports it, and the .along/ directory (CONTEXT, ISSUES + ISSUES/, DECISIONS, VISION, GLOSSARY, HISTORY, SESSIONS, KB). Use when the user wants to set up agent context/instructions for a project, initialize the agent structure, or invokes /along-init. Idempotent - re-running refreshes only the managed protocol block and never overwrites existing dynamic state files.
---

# Along Init (`/along-init`) [v2.0.8]

Scaffold or refresh the provider-agnostic agent-context structure in a repository - root `AGENTS.md` (with a managed block carrying the `ALONG-PROTOCOL v2.0.8`), a `CLAUDE.md` that imports it, and the `.along/` directory (`CONTEXT.md`, `ISSUES.md` + `ISSUES/`, `DECISIONS.md`, `VISION.md`, `GLOSSARY.md`, `HISTORY.md`, `SESSIONS/`, `KB/`).

## When to use
- The user wants to set up agent context or instructions for a project (`/along-init`, "set up agent context", "initialize along").
- The user wants to refresh the managed protocol block in an existing repository's `AGENTS.md` without losing project-specific conventions.
- Migrating an existing `.agents/` structure to the isolated `.along/` standard.

## Execution Steps

### Step 1: Managed Protocol Block in `AGENTS.md`
- Locate the target repository root.
- If `AGENTS.md` does not exist: create it with the full managed protocol block (`protocol.md`) and a default `## Project specifics` section.
- If `AGENTS.md` already exists: update only the managed block between `<!-- BEGIN ALONG-PROTOCOL ... -->` and `<!-- END ALONG-PROTOCOL -->`, preserving all human-written content outside the markers.
- If legacy `<!-- BEGIN ACTDIM-AGENTS-PROTOCOL ... -->` markers are detected, replace them cleanly with the new ALONG-PROTOCOL markers.

### Step 2: `CLAUDE.md` Import Link
- Ensure `CLAUDE.md` contains the line:
  ```markdown
  See @AGENTS.md for project instructions and guidance.
  ```

### Step 3: Scaffold `.along/` Directory Skeleton (Create only if missing)
Create the directory structure if missing:
- `.along/CONTEXT.md`: Short current snapshot (< 20 lines).
- `.along/ISSUES.md` + `.along/ISSUES/` + `.along/ISSUES/done/`: Issue tracking board and typed issue files (`protocol: along`).
- `.along/DECISIONS.md`: Append-only ADR log.
- `.along/KB/`: Knowledge base articles (`INDEX.md`, `01-architecture.md`, `02-domain-model.md`, `03-setup-and-workflow.md`).
- `.along/MILESTONES/`: Milestone tracking files.
- `.along/RISKS/`: Risk & blocker registry.
- `.along/SPIKES/`: R&D experiment logs.
- `.along/CHECKLISTS/`: Standard verification checklists (`pre-commit.md`, `stage-completion.md`).
- `.along/VISION.md`, `.along/GLOSSARY.md`, `.along/HISTORY.md`, `.along/SESSIONS/<YYYY>/`.

### Step 4: Run Protocol Migration
Execute the migration engine against the target folder to validate front-matter and migrate any legacy `.agents/` content:
```bash
python scripts/migrate_protocol.py <target_root>
```
