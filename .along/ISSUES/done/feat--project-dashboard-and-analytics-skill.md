---
protocol: along
slug: project-dashboard-and-analytics-skill
type: feat
status: done
priority: high
created: 2026-08-27
updated: 2026-08-27
completed: 2026-08-27
agent: antigravity
tags: [dashboard]
milestone: v1.5.0-dashboard-and-analytics
blocked_by: []
related: []
---

# Project Dashboard & Repository Analytics Skill (`/along-dash`)

## Goal
Implement a provider-agnostic executive analytics skill (`/along-dash`) in the system that analyzes any repository following the `ALONG-PROTOCOL` (`.along/` structure, git history, KB, ADRs) and generates an executive visual dashboard & analytics report.

## Key Capabilities

### 1. Unified State & Progress Analytics
- **Issue & Feature Tracker**: Parse `.along/ISSUES/` and `.along/ISSUES.md` to compute completion rates, status breakdown (`open`, `in-progress`, `blocked`, `done`), priority matrices, and issue type distributions (`feat`, `bug`, `debt`, `task`, `docs`).
- **Feature Accomplishments List**: Highlight recently completed features with links to issue frontmatter & session logs.

### 2. Session & Decision Timeline
- **Session History**: Aggregate `.along/SESSIONS/` and `.along/HISTORY.md` into a timeline of milestones, stages, and agent session activity.
- **Architectural Decisions (ADRs)**: Extract active ADRs from `.along/DECISIONS.md` showing architectural evolution over time.

### 3. Repository & Knowledge Health
- **Knowledge Base Coverage**: Inspect `.along/KB/` for article completeness (`INDEX.md`, `01-architecture.md`, `02-domain-model.md`, `03-setup-and-workflow.md`).
- **Context Bloat Inspection**: Monitor token footprint of `.along/CONTEXT.md` and `.along/ISSUES.md`.

### 4. Multi-Format Output Modes
- **Interactive Generative UI / Web Server**: FastAPI server and SPA UI with search, filters, entity detail drawer, and Cytoscape DAG graph.
- **Standalone Static HTML Export**: Self-contained single-file HTML report with embedded JSON dataset (`.along/dashboard.html`).
- **Markdown Dashboard Report**: GitHub Flavored Markdown with Mermaid diagrams and file links (`.along/DASHBOARD.md`).
- **CLI Terminal Summary**: Lightweight text/ASCII summary with Rich tables for fast console inspection.

## Acceptance Criteria
- [x] Skill specification and folder structure defined under `skills/along-dash/`.
- [x] Data extraction script/helper for parsing `.along/` YAML frontmatter and markdown (`scripts/along_dash.py`).
- [x] Interactive UI template for visual rendering and DAG dependency visualization.
- [x] Markdown dashboard generator supporting Mermaid charts and file links.
- [x] Static HTML single-file report exporter.
- [x] Integration with `install.ps1` / `install.sh` for global/local skill installation.

