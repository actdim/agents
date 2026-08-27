# actdim-agents (v1.5.6)

A provider-agnostic **agent-context system** for repositories - the `ACTDIM-AGENTS-PROTOCOL v1.5.6`
plus the skills/commands that scaffold and maintain it. One convention, honored by
**Claude Code**, **Codex**, **OpenCode**, and **Antigravity**.

## Why

AI agents start every session blind. They don't remember the decisions you made last time,
the current state of the work, the open issues, or the project's conventions - so they
re-ask the same questions, contradict earlier choices, and drift. And each tool keeps its
guidance in its own place (`~/.claude`, `~/.codex`, `~/.config/opencode`, `~/.gemini/config`), so nothing is shared.

This system fixes that by giving the **repository** a small, durable, human-readable memory
that every agent reads and keeps up to date.

## What it gives

- **Persistent project memory, versioned in the repo** (not locked inside one tool): current
  state, issue board, architectural decisions, Knowledge Base, vision/roadmap, glossary, and a per-session log.
- **One protocol for all four agents** - write conventions once, every tool follows them.
- **Low-friction upkeep** - skills/commands scaffold the structure and update it at the end of
  a stage or session (documentation check, session log, context, issues, decisions, history) instead of you doing bookkeeping.
- **Structured Knowledge Base (KB)** - `01-architecture.md`, `02-domain-model.md`, `03-setup-and-workflow.md` maintained in `.agents/KB/` while keeping `AGENTS.md` lean.
- **Travels with the code** - teammates who clone and CI agents get the same context; there is
  no global state to sync.

## How it works

- Every folder can carry an **`AGENTS.md`** (the protocol + that folder's specifics) and an
  **`.agents/`** directory (its state). Nearest wins; higher levels add broader context.
- Agents read it **natively**:
  - Claude Code reads `CLAUDE.md`, which imports `AGENTS.md`.
  - Codex reads `AGENTS.md`.
  - OpenCode reads `AGENTS.md` (and falls back to `~/.claude/CLAUDE.md`).
  - Antigravity reads `AGENTS.md` (or `GEMINI.md`).
- The FULL protocol text is stamped **once** at the architecture root; nested folders get a
  short **REF** block pointing up to it - no duplication.
- `.agents/` holds:
  - `CONTEXT.md` - short "you are here" snapshot of the current state (read every session).
  - `ISSUES.md` + `ISSUES/<type>--<slug>.md` (+ `ISSUES/done/`) - a compact issue board (`## Active`, `## Backlog`, `## Done`) and one file per typed issue (YAML front-matter: `slug`, `type`, `status`, `priority`, `created`, `updated`). Supported types: `feat`, `bug`, `debt`, `task`, `docs`.
  - `DECISIONS.md` - append-only ADR log (never rewritten; superseded, not deleted). Kept in a single file rather than multi-file MADR/Nygard format so agents can load all active architectural constraints in a single read at session start.
  - `KB/` - structured Knowledge Base articles (`INDEX.md`, `01-architecture.md`, `02-domain-model.md`, `03-setup-and-workflow.md`).
  - `VISION.md` - scope, non-goals, roadmap.
  - `GLOSSARY.md` - domain terms.
  - `HISTORY.md` + `SESSIONS/<year>/<date>--<slug>.md` - an index and one log per session (YAML front-matter: date, agent, branch, commit, summary).

### Skills / commands (v1.5.6)

| Skill | Purpose |
|-------|---------|
| `init-agents`  | Scaffold/refresh `AGENTS.md` + `CLAUDE.md` + `.agents/` in a folder. |
| `update-agents`| One-liner update of repository context and global skills from GitHub (`/update-agents`). |
| `init-kb`      | Bootstrap or refresh structured Knowledge Base articles in `.agents/KB/` from `README.md`, `AGENTS.md`, and `docs/`. |
| `search-kb`    | Query project Knowledge Base (`.agents/`, `docs/`, `wiki/`, `README.md`) using hybrid search (`/search-kb`). |
| `search-wiki`  | Alias for `/search-kb`. |
| `sync-kb`      | Reconcile and update Knowledge Base hybrid search indexes (`/sync-kb`). |
| `sync-wiki`    | Alias for `/sync-kb`. |
| `check-graph`  | Inspect `code-review-graph` status, impact radius (blast radius), and architecture flows (`/check-graph`). |
| `sync-history` | Reconstruct and reconcile `.agents/` milestones, issues, and sessions from Git commits (`/sync-history`). |
| `bump-version` | Auto-increment version, sanitize typography, deploy global installs, and commit (`/bump-version`). |
| `wrap-session` | End-of-stage/session update: documentation check, session log, context, issues, decisions, history. |
| `wrap-stage`   | Alias for `wrap-session` focused on completing a work stage / milestone phase. |
| `sync-context` | Refresh just the nearest `.agents/CONTEXT.md`. |
| `sync-issues`  | Reconcile the issue board + per-issue `<type>--<slug>.md` files with the actual work. |
| `sync-tasks`   | Backward-compatible alias for `sync-issues`. |
| `sync-decisions` | Append architectural decisions as ADR entries; mark superseded ones. |

## Provider support

| Provider     | Reads the protocol via              | Skills installed as                                  |
|--------------|-------------------------------------|------------------------------------------------------|
| Claude Code  | `CLAUDE.md` -> imports `AGENTS.md`   | `~/.claude/skills/<name>/SKILL.md` (copied verbatim) |
| Codex        | `AGENTS.md` (native)                | `~/.codex/skills/<name>/SKILL.md` (copied verbatim)  |
| OpenCode     | `AGENTS.md` (native, + `CLAUDE.md`) | `~/.config/opencode/commands/<name>.md` (generated)  |
| Antigravity  | `AGENTS.md` / `GEMINI.md` (native)  | `~/.gemini/config/skills/<name>/SKILL.md` (copied verbatim) |

## MCP Integration (`code-review-graph` & `wiki-llm`)

`actdim-agents` automatically configures and integrates code analysis and hybrid search MCP servers across all supported providers (Claude Code, Codex, OpenCode, Antigravity).

- **`code-review-graph`**: Automatic code analysis and call graph tracing (`build_or_update_graph_tool`, `get_impact_radius_tool`, `get_architecture_overview_tool`, `list_flows_tool`).
- **`wiki-llm` / Knowledge Base Search**: Hybrid semantic documentation search across `.agents/`, `docs/`, `wiki/`, `README.md`.

## Install

### Option A: Clone & Install (Recommended)

**Windows (PowerShell):**
```powershell
git clone https://github.com/actdim/actdim-agents.git
cd actdim-agents
powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1 -Target all
```

**Linux / macOS (Bash):**
```bash
git clone https://github.com/actdim/actdim-agents.git
cd actdim-agents
bash install.sh --target=all
```

### Option B: One-Liner Quick Install

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/actdim/actdim-agents/main/install.ps1 | iex
```

**Linux / macOS (Bash):**
```bash
curl -fsSL https://raw.githubusercontent.com/actdim/actdim-agents/main/install.sh | bash
```
