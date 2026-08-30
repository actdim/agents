# Along (v2.1.1)

A provider-agnostic **agent-context and memory system** for repositories *(formerly `actdim-agents`)* - the `ALONG-PROTOCOL v2.1.1`
plus the skills/commands that scaffold and maintain it. One convention, honored by
**Claude Code**, **Codex**, **OpenCode**, and **Antigravity**.

## Why

AI agents start every session blind. They don't remember the decisions you made last time,
the current state of the work, the open issues, or the project's conventions - so they
re-ask the same questions, contradict earlier choices, and drift. And each tool keeps its
guidance in its own place (`~/.claude`, `~/.codex`, `~/.config/opencode`, `~/.gemini/config`), so nothing is shared.

This system fixes that by giving the **repository** an isolated, durable, human-readable memory
directory (`.along/`) that every agent reads and keeps up to date.

## What it gives

- **Persistent project memory, versioned in the repo** (not locked inside one tool): current
  state, issue board, architectural decisions, Knowledge Base, vision/roadmap, glossary, and a per-session log.
- **One protocol for all four agents** - write conventions once, every tool follows them.
- **Low-friction upkeep** - `along-*` skills/commands scaffold the structure and update it at the end of
  a stage or session (documentation check, session log, context, issues, decisions, history) instead of you doing bookkeeping.
- **Structured Knowledge Base (KB) & LLM-Wiki** - `01-architecture.md`, `02-domain-model.md`, `03-setup-and-workflow.md` maintained in `docs/` with `.archive/` source isolation while keeping `AGENTS.md` lean.
- **Travels with the code** - teammates who clone and CI agents get the same context; there is
  no global state to sync.

## How it works

- Every folder can carry an **`AGENTS.md`** (the protocol + that folder's specifics) and an
  isolated **`.along/`** directory (its state). Nearest wins; higher levels add broader context.
- Agents read it **natively**:
  - Claude Code reads `CLAUDE.md`, which imports `AGENTS.md`.
  - Codex reads `AGENTS.md`.
  - OpenCode reads `AGENTS.md` (and falls back to `~/.claude/CLAUDE.md`).
  - Antigravity reads `AGENTS.md` (or `GEMINI.md`).
- The FULL protocol text is stamped **once** at the architecture root; nested folders get a
  short **REF** block pointing up to it - no duplication.
- `.along/` holds:
  - `CONTEXT.md` - short "you are here" snapshot of the current state (read every session).
  - `ISSUES.md` + `ISSUES/<type>--<slug>.md` (+ `ISSUES/done/`) - a compact issue board (`## Active`, `## Backlog`, `## Done`) and one file per typed issue (YAML front-matter: `protocol: along`, `slug`, `type`, `status`, `priority`, `created`, `updated`). Supported types: `feat`, `bug`, `debt`, `task`, `docs`.
  - `DECISIONS.md` - append-only ADR log (never rewritten; superseded, not deleted). Kept in a single file rather than multi-file MADR/Nygard format so agents can load all active architectural constraints in a single read at session start.
  - `VISION.md` - scope, non-goals, roadmap.
  - `GLOSSARY.md` - domain terms.
- `docs/` holds the active Knowledge Base (`INDEX.md`, `01-architecture.md`, `02-domain-model.md`, `03-setup-and-workflow.md`, `topic--*.md`), while raw unmanaged sources are safely archived in `.archive/`.

---

## Skills Quick Reference (Singular Domain-First)

| Skill / Command | Purpose |
| :--- | :--- |
| `along-init` (`/along-init`) | Scaffold/refresh `AGENTS.md` + `CLAUDE.md` + `.along/` in a folder. |
| `along-update` (`/along-update`) | One-liner update of repository context, protocol, and global skills from GitHub. |
| `along-dash` (`/along-dash`) | Launch the Along executive dashboard, inspect DAG dependencies, or export reports. |
| `along-wrap` (`/along-wrap`) | Unified end-of-stage/session update: code review, session log, context, issues, history. |
| `along-commit` (`/along-commit`) | Smart pre-commit ASCII check and Conventional Commit linked to active issue. |
| `along-build` (`/along-build`) | Project build lifecycle hook via `.along/scripts/build.py` or auto-detected runner. |
| `along-test` (`/along-test`) | Automated tests with quiet flags via `.along/scripts/test.py` or auto-detected runner. |
| `along-dev` (`/along-dev`) | Development / debugging server via `.along/scripts/dev.py` or auto-detected runner. |
| `along-kb-sync` (`/along-kb-sync`) | Synchronize, compile, and reconcile the Knowledge Base in `docs/` using LLM-Wiki pipeline. |
| `along-kb-search` (`/along-kb-search`) | Fast targeted structured retrieval across `docs/` and project documentation. |
| `along-issue-sync` (`/along-issue-sync`) | Reconcile the issue board + per-issue `<type>--<slug>.md` files with the actual work. |
| `along-context-sync` (`/along-context-sync`) | Refresh just the nearest `.along/CONTEXT.md`. |
| `along-decision-sync` (`/along-decision-sync`) | Append architectural decisions as ADR entries; mark superseded ones. |
| `along-history-sync` (`/along-history-sync`) | Reconstruct and reconcile `.along/` milestones, issues, and sessions from Git commits. |
| `along-graph-check` (`/along-graph-check`) | Inspect `code-review-graph` status, impact radius (blast radius), and architecture flows. |
| `along-dep-scan` (`/along-dep-scan`) | Scan declared dependencies for AI instructions and register in `docs/dependencies.md`. |
| `along-version-bump` (`/along-version-bump`) | Multi-stack version bump (Node, Python, Rust, .NET, or .along/scripts/bump_version.py). |

### Deployment Best Practices (Why no `along-deploy`?)

`Along` intentionally does **not** provide an `along-deploy` skill. In modern software engineering, production deployment is a security-critical operation that should not be executed ad-hoc by local agents. Following industry best practices, deployments should be handled by automated **CI/CD pipelines** (e.g., GitHub Actions, GitLab CI, ArgoCD) triggered by version release tags (`git push --tags` or `/along-version-bump -cp`) or release webhooks. If a repository requires a custom local deploy script, it can be placed in `.along/scripts/deploy.py` and executed via `python scripts/along_exec.py deploy`.

---

## Executive Dashboard (`/along-dash`)

`along` includes a multi-mode dashboard engine (`scripts/along_dash.py`) for visual project analytics and DAG dependency tracking:

```text
+-------------------------------------------------------------------+
| Along Dashboard (along)                                           |
| Scanned 2026-08-27 20:41:45 | Root: D:\Src\my\actdim\public\along |
+-------------------------------------------------------------------+
                        Executive Summary                         
+----------------------------------------------------------------+
| Metric               |   Value | Details                       |
|----------------------+---------+-------------------------------|
| Total Issues         |      18 | Done: 14 (77.8%)              |
| In-Progress / Open   |   0 / 4 | Active backlog                |
| Blocked Issues       |       0 | None                          |
| Active Risks         |       0 | Critical/High: 0              |
| Milestones & Sprints |       4 | Tracked targets               |
| Sessions & ADRs      |   8 / 7 | Recorded progress             |
| KB Articles          |       4 | Knowledge base docs           |
| Context Hygiene      | 9 lines | CONTEXT.md (<20 lines target) |
+----------------------------------------------------------------+
```

### Dashboard Modes & Features
- **Interactive Local Web Dashboard**: `uv run scripts/along_dash.py --web` (FastAPI backend + Reactive Web UI at `http://127.0.0.1:8765`).
  - **Dynamic Knowledge Base Search**: Fast hybrid search modal across KB articles, issues, ADR decisions, and sessions.
  - **OpenAPI & Swagger Documentation**: Auto-generated interactive API docs at `http://127.0.0.1:8765/docs`.
  - **Cytoscape DAG Graph**: Interactive dependency graph with cycle detection and status indicators.
  - **Live Auto-Refresh**: Server-Sent Events (SSE) broadcasting file changes in real-time.
- **CLI Terminal Summary**: `uv run scripts/along_dash.py --cli`
- **Static Standalone HTML Export**: `uv run scripts/along_dash.py --export .along/dashboard.html`
- **Markdown Dashboard Report**: `uv run scripts/along_dash.py --markdown` (`.along/DASHBOARD.md`)

---

## Provider Support

| Provider | Reads the protocol via | Skills installed as |
| :--- | :--- | :--- |
| Claude Code | `CLAUDE.md` -> imports `AGENTS.md` | `~/.claude/skills/<name>/SKILL.md` |
| Codex | `AGENTS.md` (native) | `~/.codex/skills/<name>/SKILL.md` |
| OpenCode | `AGENTS.md` (native, + `CLAUDE.md`) | `~/.config/opencode/commands/<name>.md` |
| Antigravity | `AGENTS.md` / `GEMINI.md` (native) | `~/.gemini/config/skills/<name>/SKILL.md` |

## MCP Integration (`code-review-graph` & `wiki-llm`)

`along` automatically configures and integrates code analysis and hybrid search MCP servers across all supported providers (Claude Code, Codex, OpenCode, Antigravity).

- **`code-review-graph`**: Automatic code analysis and call graph tracing (`build_or_update_graph_tool`, `get_impact_radius_tool`, `get_architecture_overview_tool`, `list_flows_tool`).
- **`wiki-llm` / Knowledge Base Search**: Hybrid semantic documentation search across `.along/`, `docs/`, `wiki/`, `README.md`.

## Install

### Option A: Clone & Install (Recommended)

**Windows (PowerShell):**
```powershell
git clone https://github.com/actdim/along.git
cd along
powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1 -Target all
```

**Linux / macOS (Bash):**
```bash
git clone https://github.com/actdim/along.git
cd along
bash install.sh --target=all
```

### Option B: One-Liner Quick Install

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/actdim/along/main/install.ps1 | iex
```

**Linux / macOS (Bash):**
```bash
curl -fsSL https://raw.githubusercontent.com/actdim/along/main/install.sh | bash
```
