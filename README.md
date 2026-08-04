# actdim-agents

A provider-agnostic **agent-context system** for repositories — the `ACTDIM-AGENTS-PROTOCOL`
plus the skills/commands that scaffold and maintain it. One convention, honored by
**Claude Code**, **Codex**, and **OpenCode**.

## Why

AI agents start every session blind. They don't remember the decisions you made last time,
the current state of the work, the open tasks, or the project's conventions — so they
re-ask the same questions, contradict earlier choices, and drift. And each tool keeps its
guidance in its own place (`~/.claude`, `~/.codex`, `~/.config/opencode`), so nothing is shared.

This system fixes that by giving the **repository** a small, durable, human-readable memory
that every agent reads and keeps up to date.

## What it gives

- **Persistent project memory, versioned in the repo** (not locked inside one tool): current
  state, task board, architectural decisions, vision/roadmap, glossary, and a per-session log.
- **One protocol for all three agents** — write conventions once, every tool follows them.
- **Low-friction upkeep** — skills/commands scaffold the structure and update it at the end of
  a session (session log, context, tasks, decisions, history) instead of you doing bookkeeping.
- **Travels with the code** — teammates who clone and CI agents get the same context; there is
  no global state to sync.

## How it works

- Every folder can carry an **`AGENTS.md`** (the protocol + that folder's specifics) and an
  **`.agents/`** directory (its state). Nearest wins; higher levels add broader context.
- Agents read it **natively**:
  - Claude Code reads `CLAUDE.md`, which imports `AGENTS.md`.
  - Codex reads `AGENTS.md`.
  - OpenCode reads `AGENTS.md` (and falls back to `~/.claude/CLAUDE.md`).
- The FULL protocol text is stamped **once** at the architecture root; nested folders get a
  short **REF** block pointing up to it — no duplication.
- `.agents/` holds:
  - `CONTEXT.md` — short "you are here" snapshot of the current state (read every session).
  - `TASKS.md` + `TASKS/<slug>.md` (+ `TASKS/done/`) — a compact board and one file per task (YAML front-matter: status, dates).
  - `DECISIONS.md` — append-only ADR log (never rewritten; superseded, not deleted).
  - `VISION.md` — scope, non-goals, roadmap.
  - `GLOSSARY.md` — domain terms.
  - `HISTORY.md` + `SESSIONS/<year>/<date>--<slug>.md` — an index and one log per session (YAML front-matter: date, agent, branch, commit, summary).
- **Session lifecycle:** at the start, the agent reads `AGENTS.md` + `.agents/{CONTEXT,TASKS,DECISIONS}`;
  it works; at the end it logs the session, refreshes `CONTEXT`, updates `TASKS`, appends `HISTORY`,
  and records any decisions — all kept compact, and never containing secrets.

### Skills / commands

| Skill | Purpose |
|-------|---------|
| `init-agents`  | Scaffold/refresh `AGENTS.md` + `CLAUDE.md` + `.agents/` in a folder (FULL vs REF auto-detected; a folder-own `VISION.md` is moved into `.agents/`). |
| `wrap-session` | End-of-session update: session log, context, tasks, decisions, history. |
| `sync-context` | Refresh just the nearest `.agents/CONTEXT.md`. |
| `sync-tasks`   | Reconcile the task board + per-task files with the actual work. |
| `sync-decisions` | Append architectural decisions as ADR entries; mark superseded ones. |

## Provider support

| Provider     | Reads the protocol via              | Skills installed as                                  |
|--------------|-------------------------------------|------------------------------------------------------|
| Claude Code  | `CLAUDE.md` → imports `AGENTS.md`   | `~/.claude/skills/<name>/SKILL.md` (copied verbatim) |
| Codex        | `AGENTS.md` (native)                | `~/.codex/skills/<name>/SKILL.md` (copied verbatim)  |
| OpenCode     | `AGENTS.md` (native, + `CLAUDE.md`) | `~/.config/opencode/commands/<name>.md` (generated)  |

Claude & Codex share the identical `SKILL.md` format, so the skill folders are copied as-is.
OpenCode uses flat `commands/*.md` with different front-matter, so those are **generated from the
same `SKILL.md` bodies** at install time; `init-agents`' helper files (`protocol.md`, `init-agents.sh`)
are placed in `~/.config/opencode/actdim-agents/`. Either way the instruction text has a single source.

## Layout

```
actdim-agents/
  install.ps1 / install.bat     # Windows installer
  install.sh                    # Linux / macOS installer
  skills/
    init-agents/                # SKILL.md + protocol.md + init-agents.sh
    wrap-session/               # SKILL.md
    sync-context/               # SKILL.md
    sync-tasks/                 # SKILL.md
    sync-decisions/             # SKILL.md
```

The authoritative protocol text is `skills/init-agents/protocol.md`.

## Install

Targets: `claude`, `codex`, `opencode`, `both` (claude+codex), `all` (default).

**Windows:**
```
install.bat                     # all (copy); re-run after `git pull` to update
install.bat -Target opencode    # one provider
install.bat -Symlink            # symlink skill folders (claude/codex); needs admin / Developer Mode
```

**Linux / macOS:**
```
bash install.sh                 # all (copy)
bash install.sh --target=codex  # one provider
bash install.sh --symlink       # symlink skill folders (claude/codex)
```

## Use

- In a repo (or subfolder) run `/init-agents` (or `bash skills/init-agents/init-agents.sh <dir>`)
  to scaffold `AGENTS.md` + `CLAUDE.md` + `.agents/`.
- Work as usual; use `/wrap-session` at the end (or `/sync-context` / `/sync-tasks` for focused updates).
