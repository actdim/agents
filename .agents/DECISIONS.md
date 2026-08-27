# Decisions (ADR - append-only)

_One dated entry per architectural decision. Never edit past entries; mark a replaced one "Superseded by #N"._

<!-- Template:
## #001 - <title>
- Date: YYYY-MM-DD
- Status: accepted            (or: superseded by #NNN)
- Context: <why this came up>
- Decision: <what was decided>
- Consequences: <trade-offs / follow-ups>
-->

## #001 - Single-file append-only DECISIONS.md over multi-file MADR/Nygard
- Date: 2026-08-15
- Status: accepted
- Context: In software engineering, Architectural Decision Records (ADRs) are often kept as separate files per decision (e.g. Michael Nygard / MADR format `doc/adr/0001-*.md`). We evaluated whether `.agents/` should store decisions in separate files (like `.agents/ISSUES/`) or in a single file.
- Decision: Keep all architectural decisions in a single append-only `.agents/DECISIONS.md` file rather than individual files.
- Consequences:
  - **Single-shot context load**: Agents read all active constraints on session start in one tool call (< 300 tokens) without traversing or indexing multiple files.
  - **No lifecycle overhead**: Unlike Issues (`open` -> `in-progress` -> `done/`), decisions are immutable and only appended or marked `superseded by #NNN`.

## #002 - Protocol v1.2.0 & Knowledge Base (KB) Architecture Standard
- Date: 2026-08-26
- Status: accepted
- Context: Projects require a structured, persistent Knowledge Base that provides deep architecture, domain model, and workflow guidance without bloating `AGENTS.md` context window.
- Decision: Adopt Knowledge Base (KB) terminology and structure in `.agents/KB/` (`INDEX.md`, `01-architecture.md`, `02-domain-model.md`, `03-setup-and-workflow.md`). `AGENTS.md` remains a compact executive entry point linking to KB articles (`[[.agents/KB/INDEX.md]]`). Human `docs/` and `README.md` are scanned as read-only inputs during `/init-kb` and `/sync-kb`.
- Consequences: `AGENTS.md` stays lean (< 80 lines) while agents and humans have structured access to deep documentation.

## #003 - Code Graph & Hybrid Knowledge Base Search MCP Integration
- Date: 2026-08-26
- Status: accepted
- Context: Agents need lightweight tools to inspect call hierarchies and search project documentation without loading massive raw files.
- Decision: Integrate `code-review-graph` for AST call graph analysis and impact radius, and `wiki-llm` / native hybrid search (`/search-kb`, `/sync-kb`) for document querying. Provide `/check-graph` and `/search-kb` debugging slash commands across all agent tools (Antigravity, Claude Code, Codex, OpenCode).
- Consequences: Agents prioritize MCP graph and hybrid search calls during research and refactoring, saving token overhead.

## #004 - Protocol v1.5.0: Automated Entity Ecosystem & Zero-Friction Intent Recognition
- Date: 2026-08-27
- Status: accepted
- Context: Turning `.agents/` into a complete project tracking and dashboard-ready analytics system requires tracking milestones, risks, spikes, checklists, and completed issue timestamps without forcing the human developer to manually manage project files.
- Decision: Expand `.agents/` entity ecosystem with `MILESTONES/`, `RISKS/`, `SPIKES/`, `CHECKLISTS/`, and standardized YAML front-matter (`completed: YYYY-MM-DD`, `agent`, `tags`). Enforce strict automatic intent recognition heuristics in `AGENTS.md` and mandatory stage wrap-up verification checklists in `wrap-session`. Provide retroactive auto-migration tooling (`migrate_dashboard_metadata.py`) across all installation targets.
- Consequences: Full project visibility and analytics ready for `/repo-dashboard` while maintaining zero human friction during everyday coding.

## #005 - Entity Relationships, Unidirectional Graph Storage & Canonical Slug Invariance
- Date: 2026-08-27
- Status: accepted
- Context: Representing dependencies and associations between issues, risks, and spikes is required for dependency modeling and DAG/timeline visualizations. Using relative file paths breaks references when completed issues move into `done/`. Dual-syncing reciprocal fields (`blocks` vs `blocked_by`, `parent` vs `children`) causes drift by LLM agents.
- Decision:
  1. Store dependencies unidirectionally in YAML front-matter (`blocked_by: []`, `related: []`, `parent: <slug>`). Reverse relationships (`blocks`, `children`) and full DAGs are computed dynamically by graph parsers and dashboard builders.
  2. Reference entities strictly by canonical key (`<type>--<slug>` or `<slug>`), never by physical filesystem path, ensuring links remain valid across moves to `done/`.
  3. Validate DAGs for cyclic dependencies and dangling references in `migrate_protocol.py` and provide a `/update-agents` one-liner skill for automated global and project upgrades.
- Consequences: Eliminates link drift, guarantees graph invariance across entity lifecycles, and enables automated dashboard dependency graphs.

## #006 - Autonomous Multi-Mode Repository Dashboard & Analytics Engine
- Date: 2026-08-27
- Status: accepted
- Context: Developers and agents require instant visibility into `.agents/` entity lifecycles, milestone completion rates, active blockers, and dependency DAGs without manual data compilation or heavy infrastructure.
- Decision:
  1. Implement an autonomous Python script (`scripts/dashboard.py`) using PEP 723 inline dependencies (`# /// script ...`) executable directly via `uv run scripts/dashboard.py`.
  2. Provide 4 decoupled operational modes in a single codebase:
     - **CLI Mode**: Terminal summary with Rich tables and priority breakdowns.
     - **Interactive Web Mode**: Lightweight FastAPI + Uvicorn server hosting a modern single-page dashboard with Cytoscape DAG visualization, search, status filters, and markdown entity drawer.
     - **Static HTML Export**: Self-contained single-file HTML report with embedded JSON dataset for zero-server sharing.
     - **Markdown Dashboard**: GFM report (`.agents/DASHBOARD.md`) with Mermaid status charts and entity links.
  3. Expose the `/repo-dashboard` and `/dashboard` skills across Claude Code, Codex, OpenCode, and Antigravity.
- Consequences: Zero setup cost, instant offline/online dashboard visualization across all execution environments.


