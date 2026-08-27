# Protocol & Repository Migrations Guide

This guide documents the versioned migration pipeline for the `ALONG-PROTOCOL` (`.along/`).

---

## Overview

When updating `along` or running `/along-init` / `/along-update`, the migration engine (`scripts/migrate_protocol.py`) inspects the target repository's current structure and protocol version, executing sequential, non-destructive migration steps to bring it up to the latest standard without losing any human-written content.

---

## Version Migration Pipeline

```mermaid
flowchart TD
    A["Legacy Repo (v1.0)"] -->|Step 1: Tasks to Issues| B["v1.1.0 (ISSUES structure)"]
    B -->|Step 2: Scaffolding KB & Graph| C["v1.3.0 (Knowledge Base & Graph)"]
    C -->|Step 3: Entity Ecosystem & Retro-Synthesis| D["v1.5.0 (Automated Milestones, Risks, Checklists)"]
    D -->|Step 4: Transition to Along & .along/| E["v2.0.0 (Along Ecosystem & protocol: along)"]
```

### 1. `v1.0.0` -> `v1.1.0` (Tasks to Issues)
- **Problem**: Earlier versions used `TASKS.md` and `.agents/TASKS/`.
- **Migration Action**:
  - Renames `TASKS.md` -> `ISSUES.md` and replaces `TASKS` glyphs.
  - Renames `TASKS/` -> `ISSUES/`.
  - Enforces kebab-case `<type>--<slug>.md` naming for all issue files.

### 2. `v1.1.0` -> `v1.3.0` (Knowledge Base & Code Graph)
- **Problem**: Projects lacked structured architecture and domain model documentation.
- **Migration Action**:
  - Scaffolds `.agents/KB/` (`INDEX.md`, `01-architecture.md`, `02-domain-model.md`, `03-setup-and-workflow.md`).
  - Creates `.code-review-graph-ignore` with standard excludes (`node_modules/`, `dist/`, `build/`, `SESSIONS/`).

### 3. `v1.3.3` -> `v1.5.0` (Automated Entity Ecosystem & Retro-Synthesis)
- **Problem**: Missing unified tracking entities (`MILESTONES`, `RISKS`, `SPIKES`, `CHECKLISTS`) and structured metadata (`completed: YYYY-MM-DD`, `milestone: <slug>`) needed for visual dashboards.
- **Migration Action**:
  - **Directory Scaffolding**: Creates `.agents/MILESTONES/`, `.agents/RISKS/`, `.agents/SPIKES/`, `.agents/CHECKLISTS/`, `.agents/KB/`, and `.agents/ISSUES/done/`.
  - **Retroactive Milestone Synthesis**:
    - Analyzes past `SESSIONS/`, `HISTORY.md`, and `ISSUES/done/` to synthesize completed milestone(s) (e.g. `v1.3.0-knowledge-base-and-graph.md`) with `status: completed`, `progress_pct: 100`.
    - Synthesizes an active milestone for open issues (e.g. `v1.5.0-dashboard-and-analytics.md`) with `status: in-progress`.
  - **Checklists Synthesis**: Scaffolds reusable QA quality gates in `.agents/CHECKLISTS/` (`stage-completion.md`, `pre-commit.md`).
  - **Front-Matter Enrichment**:
    - Sets `completed: YYYY-MM-DD` for all closed issues.
    - Links every issue to its corresponding `milestone: <slug>`.
  - **Typography Sanitation (Banning Em-Dashes)**:
    - Automatically scans all `.md` files in `.agents/` and replaces non-standard em-dashes (U+2014) with standard ASCII hyphens (`-`).
    - Standardizes quotes and clean UTF-8 encoding across all documentation.

### 4. `v1.5.7` -> `v2.0.0` (Transition to Along Ecosystem & `.along/` Directory)
- **Problem**: `.agents/` directory is generic and susceptible to collisions with unrelated third-party tools; skills lacked clear namespacing in global agent environments.
- **Migration Action**:
  - **Directory Migration (`.agents/` -> `.along/`)**:
    - Filters and moves verified Along protocol files (`CONTEXT.md`, `ISSUES.md`, `DECISIONS.md`, `HISTORY.md`, `GLOSSARY.md`, `VISION.md`, `ISSUES/`, `MILESTONES/`, `RISKS/`, `SPIKES/`, `CHECKLISTS/`, `SESSIONS/`, `KB/`) to `.along/`.
    - If `.agents/` contains only Along files, `.agents/` is removed; if foreign files exist, they remain untouched.
  - **Protocol Flag Injection**:
    - Injects `protocol: along` into YAML front-matter of all entity markdown files.
  - **Marker Updates**:
    - Replaces `<!-- BEGIN ACTDIM-AGENTS-PROTOCOL ... -->` with `<!-- BEGIN ALONG-PROTOCOL ... -->` in `AGENTS.md`.
  - **Config & Cache Relocation**:
    - Moves `~/.config/opencode/actdim-agents/` to `~/.config/opencode/actdim-along/`.
    - Moves `~/.cache/actdim-agents/` to `~/.cache/actdim-along/`.
  - **Global Skills Cleanup**:
    - Purges obsolete un-namespaced skill directories from global agent environments (`~/.claude/skills/`, `~/.gemini/antigravity/skills/`, OpenCode, Codex) and installs the new `along-*` suite.

---

## How Migrations are Executed

### 1. Automatic Execution (Zero-Friction)
- **During Installation**: Running `install.ps1` (or `install.sh`) automatically runs `migrate_protocol.py` on the current repository.
- **During Project Initialization / Refresh**: Invoking `/along-init` or `/along-update` runs the migration engine against the target folder automatically.

### 2. Manual CLI Invocation
To migrate any repository explicitly:
```bash
# Windows / Linux / macOS
python scripts/migrate_protocol.py /path/to/target/repo
```
