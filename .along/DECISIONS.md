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
- Context: In software engineering, Architectural Decision Records (ADRs) are often kept as separate files per decision (e.g. Michael Nygard / MADR format `doc/adr/0001-*.md`). We evaluated whether `.along/` should store decisions in separate files (like `.along/ISSUES/`) or in a single file.
- Decision: Keep all architectural decisions in a single append-only `.along/DECISIONS.md` file rather than individual files.
- Consequences:
  - **Single-shot context load**: Agents read all active constraints on session start in one tool call (< 300 tokens) without traversing or indexing multiple files.
  - **No lifecycle overhead**: Unlike Issues (`open` -> `in-progress` -> `done/`), decisions are immutable and only appended or marked `superseded by #NNN`.

## #002 - Protocol v1.2.0 & Knowledge Base (KB) Architecture Standard
- Date: 2026-08-26
- Status: accepted
- Context: Projects require a structured, persistent Knowledge Base that provides deep architecture, domain model, and workflow guidance without bloating `AGENTS.md` context window.
- Decision: Adopt Knowledge Base (KB) terminology and structure in `.along/KB/` (`INDEX.md`, `01-architecture.md`, `02-domain-model.md`, `03-setup-and-workflow.md`). `AGENTS.md` remains a compact executive entry point linking to KB articles (`[[.along/KB/INDEX.md]]`). Human `docs/` and `README.md` are scanned as read-only inputs during `/along-init-kb` and `/along-sync-kb`.
- Consequences: `AGENTS.md` stays lean (< 80 lines) while agents and humans have structured access to deep documentation.

## #003 - Code Graph & Hybrid Knowledge Base Search MCP Integration
- Date: 2026-08-26
- Status: accepted
- Context: Agents need lightweight tools to inspect call hierarchies and search project documentation without loading massive raw files.
- Decision: Integrate `code-review-graph` for AST call graph analysis and impact radius, and `wiki-llm` / native hybrid search (`/along-search-kb`, `/along-sync-kb`) for document querying. Provide `/along-check-graph` and `/along-search-kb` debugging slash commands across all agent tools (Antigravity, Claude Code, Codex, OpenCode).
- Consequences: Agents prioritize MCP graph and hybrid search calls during research and refactoring, saving token overhead.

## #004 - Protocol v1.5.0: Automated Entity Ecosystem & Zero-Friction Intent Recognition
- Date: 2026-08-27
- Status: accepted
- Context: Turning agent tracking into a complete project tracking and dashboard-ready analytics system requires tracking milestones, risks, spikes, checklists, and completed issue timestamps without forcing the human developer to manually manage project files.
- Decision: Expand entity ecosystem with `MILESTONES/`, `RISKS/`, `SPIKES/`, `CHECKLISTS/`, and standardized YAML front-matter (`completed: YYYY-MM-DD`, `agent`, `tags`). Enforce strict automatic intent recognition heuristics in `AGENTS.md` and mandatory stage wrap-up verification checklists in `along-wrap-session`. Provide retroactive auto-migration tooling (`migrate_protocol.py`) across all installation targets.
- Consequences: Full project visibility and analytics ready for `/along-dash` while maintaining zero human friction during everyday coding.

## #005 - Entity Relationships, Unidirectional Graph Storage & Canonical Slug Invariance
- Date: 2026-08-27
- Status: accepted
- Context: Representing dependencies and associations between issues, risks, and spikes is required for dependency modeling and DAG/timeline visualizations. Using relative file paths breaks references when completed issues move into `done/`. Dual-syncing reciprocal fields (`blocks` vs `blocked_by`, `parent` vs `children`) causes drift by LLM agents.
- Decision:
  1. Store dependencies unidirectionally in YAML front-matter (`blocked_by: []`, `related: []`, `parent: <slug>`). Reverse relationships (`blocks`, `children`) and full DAGs are computed dynamically by graph parsers and dashboard builders.
  2. Reference entities strictly by canonical key (`<type>--<slug>` or `<slug>`), never by physical filesystem path, ensuring links remain valid across moves to `done/`.
  3. Validate DAGs for cyclic dependencies and dangling references in `migrate_protocol.py` and provide a `/along-update` one-liner skill for automated global and project upgrades.
- Consequences: Eliminates link drift, guarantees graph invariance across entity lifecycles, and enables automated dashboard dependency graphs.

## #006 - Autonomous Multi-Mode Repository Dashboard & Analytics Engine
- Date: 2026-08-27
- Status: accepted
- Context: Developers and agents require instant visibility into entity lifecycles, milestone completion rates, active blockers, and dependency DAGs without manual data compilation or heavy infrastructure.
- Decision:
  1. Implement an autonomous Python script (`scripts/along_dash.py`) using PEP 723 inline dependencies (`# /// script ...`) executable directly via `uv run scripts/along_dash.py`.
  2. Provide 4 decoupled operational modes in a single codebase: CLI Mode, Interactive Web Mode, Static HTML Export, and Markdown Dashboard Report (`.along/DASHBOARD.md`).
  3. Expose the `/along-dash` skill across Claude Code, Codex, OpenCode, and Antigravity.
- Consequences: Zero setup cost, instant offline/online dashboard visualization across all execution environments.

## #007 - Along v2.0.0: Rebranding, Isolated .along/ Directory, along-* Skill Prefixes, and protocol: along Metadata
- Date: 2026-08-27
- Status: accepted
- Context: The generic `.along/` folder was prone to collision with third-party tools, and generic un-namespaced skills (like `dashboard`, `bump-version`, `sync-context`) collided in global agent environments (`~/.claude/skills/`, `~/.gemini/config/skills/`).
- Decision:
  1. Transition the product and protocol to **Along (`actdim-along`)** and **`ALONG-PROTOCOL v2.0.0`**.
  2. Store all project tracking and memory in an isolated **`.along/`** directory in target repositories.
  3. Require **`protocol: along`** in the YAML front-matter of all entity markdown files.
  4. Prefix all skills and slash commands with **`along-*`** (`along-init`, `along-update`, `along-dash`, `along-wrap-session`, etc.) and purge legacy un-namespaced skills during installation and update.
  5. Upgrade migration engine (`scripts/migrate_protocol.py`) to seamlessly detect legacy `.along/`, inject `protocol: along`, relocate files to `.along/`, and clean up empty `.along/` directories without touching foreign files.
- Consequences: Total isolation from third-party tools, zero namespace collision in global skill registries, backward-compatible automated migration path for existing projects.

## #008 - Mandatory Agentic Code Review & Blast Radius Impact Assessment Gate
- Date: 2026-08-27
- Status: accepted
- Context: Unchecked AI code modifications often introduce regression risks, silent broken callers, edge-case crashes, or unhandled nulls that accumulate unnoticed until runtime.
- Decision:
  1. Formalize a mandatory **Code Review & Blast Radius Assessment** gate in the ALONG-PROTOCOL and session wrap-up checklist.
  2. Mandate agents to inspect their own git diffs and trace blast radius across dependent modules using `code-review-graph` MCP tools (`build_or_update_graph_tool`, `get_impact_radius_tool`, `get_affected_flows_tool`) or AST analysis.
  3. Require verification of ADR conformance in `.along/DECISIONS.md`, null-safety, and edge-case handling.
  4. Document the code review findings and impact summary in the session log (`.along/SESSIONS/`).
- Consequences: Significantly reduced regression rate, improved long-term architectural health, and explicit accountability for multi-module impact.

## #009 - Universal Project Version Bumping & Repository Scripts Ecosystem (.along/scripts/)
- Date: 2026-08-27
- Status: accepted
- Context: `along-bump-version` was initially hardcoded for `actdim/along` internal development, failing when executed in external consumer repositories (Node, Python, Rust, .NET).
- Decision:
  1. Transform `/along-bump-version` (`along_bump_version.py`) into a universal release engine.
  2. Establish `.along/scripts/` convention in project memory directories for repo-tailored automation scripts.
  3. Support execution of custom `.along/scripts/bump_version.py` hooks with fallback to automatic stack detection (Node `package.json`, Python `pyproject.toml`, Rust `Cargo.toml`, .NET `*.csproj`, Along dev).
  4. Auto-synthesize `.along/scripts/bump_version.py` on first run for detected stacks, with diagnostic templates for custom environments.
- Consequences: Every project adopting Along gains automated, stack-agnostic version bumping and release orchestration out-of-the-box.

## #010 - Unified /along-wrap, Smart /along-commit, and Lifecycle Execution Suite (/along-build, /along-test, /along-dev)
- Date: 2026-08-27
- Status: accepted
- Context: Separate `along-wrap-session` and `along-wrap-stage` skills created redundant duplication and prompt bloat. Developers also needed safe pre-commit ASCII checks, automated Conventional Commit formatting, and project lifecycle runners (`build`, `test`, `dev`).
- Decision:
  1. Consolidate `along-wrap-session` and `along-wrap-stage` into a single canonical skill: **`/along-wrap`**.
  2. Implement **`/along-commit`** (`scripts/along_commit.py`) to enforce pre-commit typography checks, auto-link active `.along/` issues, and format Conventional Commits.
  3. Deploy non-destructive lifecycle suite (**`/along-build`**, **`/along-test`**, **`/along-dev`** via `scripts/along_exec.py`), utilizing `.along/scripts/` with `# Status: verified` vs `# Status: unconfigured` markers.
  4. Refine `along-bump-version` to update files on disk by default, committing only when `--commit` is explicitly passed.
- Consequences: Reduced skill token footprint, unified wrap mental model, and robust development lifecycle automation.
