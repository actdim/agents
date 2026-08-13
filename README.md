# actdim-agents

A provider-agnostic **agent-context system** for repositories — the `ACTDIM-AGENTS-PROTOCOL`
plus the skills/commands that scaffold and maintain it. One convention, honored by
**Claude Code**, **Codex**, **OpenCode**, and **Antigravity**.

## Why

AI agents start every session blind. They don't remember the decisions you made last time,
the current state of the work, the open issues, or the project's conventions — so they
re-ask the same questions, contradict earlier choices, and drift. And each tool keeps its
guidance in its own place (`~/.claude`, `~/.codex`, `~/.config/opencode`, `~/.gemini/config`), so nothing is shared.

This system fixes that by giving the **repository** a small, durable, human-readable memory
that every agent reads and keeps up to date.

## What it gives

- **Persistent project memory, versioned in the repo** (not locked inside one tool): current
  state, issue board, architectural decisions, vision/roadmap, glossary, and a per-session log.
- **One protocol for all four agents** — write conventions once, every tool follows them.
- **Low-friction upkeep** — skills/commands scaffold the structure and update it at the end of
  a stage or session (documentation check, session log, context, issues, decisions, history) instead of you doing bookkeeping.
- **Travels with the code** — teammates who clone and CI agents get the same context; there is
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
  short **REF** block pointing up to it — no duplication.
- `.agents/` holds:
  - `CONTEXT.md` — short "you are here" snapshot of the current state (read every session).
  - `ISSUES.md` + `ISSUES/<type>--<slug>.md` (+ `ISSUES/done/`) — a compact issue board (`## Active`, `## Backlog`, `## Done`) and one file per typed issue (YAML front-matter: `slug`, `type`, `status`, `priority`, `created`, `updated`). Supported types: `feat`, `bug`, `debt`, `task`, `docs`.
  - `DECISIONS.md` — append-only ADR log (never rewritten; superseded, not deleted).
  - `VISION.md` — scope, non-goals, roadmap.
  - `GLOSSARY.md` — domain terms.
  - `HISTORY.md` + `SESSIONS/<year>/<date>--<slug>.md` — an index and one log per session (YAML front-matter: date, agent, branch, commit, summary).
- **Session & Stage lifecycle:** at the start, the agent reads `AGENTS.md` + `.agents/{CONTEXT,ISSUES,DECISIONS}`;
  it works; at the end of a stage or session, it:
  1. Checks if documentation/`README.md`/`AGENTS.md` needs updating.
  2. Logs the session in `SESSIONS/`.
  3. Refreshes `CONTEXT.md`.
  4. Updates `ISSUES.md` (moves done issues to `ISSUES/done/`).
  5. Appends `HISTORY.md` line and records any decisions — all kept compact and secret-free.

### Skills / commands

| Skill | Purpose |
|-------|---------|
| `init-agents`  | Scaffold/refresh `AGENTS.md` + `CLAUDE.md` + `.agents/` in a folder (auto-migrates legacy `TASKS` to `ISSUES`; FULL vs REF auto-detected). |
| `wrap-session` | End-of-stage/session update: documentation check, session log, context, issues, decisions, history. |
| `wrap-stage`   | Alias for `wrap-session` focused on completing a work stage / milestone phase. |
| `sync-context` | Refresh just the nearest `.agents/CONTEXT.md`. |
| `sync-issues`  | Reconcile the issue board + per-issue `<type>--<slug>.md` files with the actual work. |
| `sync-tasks`   | Backward-compatible alias for `sync-issues`. |
| `sync-decisions` | Append architectural decisions as ADR entries; mark superseded ones. |

## Provider support

| Provider     | Reads the protocol via              | Skills installed as                                  |
|--------------|-------------------------------------|------------------------------------------------------|
| Claude Code  | `CLAUDE.md` → imports `AGENTS.md`   | `~/.claude/skills/<name>/SKILL.md` (copied verbatim) |
| Codex        | `AGENTS.md` (native)                | `~/.codex/skills/<name>/SKILL.md` (copied verbatim)  |
| OpenCode     | `AGENTS.md` (native, + `CLAUDE.md`) | `~/.config/opencode/commands/<name>.md` (generated)  |
| Antigravity  | `AGENTS.md` / `GEMINI.md` (native)  | `~/.gemini/config/skills/<name>/SKILL.md` (copied verbatim) |

Claude, Codex & Antigravity share the identical `SKILL.md` format, so the skill folders are copied as-is.
OpenCode uses flat `commands/*.md` with different front-matter, so those are **generated from the
same `SKILL.md` bodies** at install time; `init-agents`' helper files (`protocol.md`, `init-agents.sh`)
are placed in `~/.config/opencode/actdim-agents/`. Either way the instruction text has a single source.

### How each tool resolves the files

**Inheritance is automatic — a nested folder does NOT need to reference the level above.** All four
tools walk UP the directory tree from the working directory and concatenate what they find, so
instructions written once at the root apply to every folder beneath it.

| Tool | File it looks for | Resolution |
|------|-------------------|------------|
| Claude Code | **`CLAUDE.md` only** (never `AGENTS.md`) | Every `CLAUDE.md` from the filesystem root down to the cwd is concatenated; the nearest is read last. |
| Codex | `AGENTS.md` | `~/.codex/AGENTS.md` → git root → down to the cwd, joined root-first; files closer to the cwd override earlier guidance. One file per directory; `AGENTS.override.md` is checked first. |
| OpenCode | `AGENTS.md` | Walks up from the cwd, then `~/.config/opencode/AGENTS.md`, then falls back to `~/.claude/CLAUDE.md`. |
| Antigravity | `AGENTS.md` / `GEMINI.md` | Walks up from the cwd to the repo root (`AGENTS.md`, `GEMINI.md`, `.agents/rules/*.md`), plus `~/.gemini/config/`. |

Consequences worth knowing:

- **A subfolder's `CLAUDE.md` is required for Claude Code** — not for inheritance, but because Claude
  never reads `AGENTS.md`. Without it, that folder's own `AGENTS.md` specifics are invisible to Claude
  (Codex, OpenCode, and Antigravity find them by themselves). This is why `init-agents` writes the `@AGENTS.md`
  pointer in every folder it scaffolds.
- **The REF block in nested `AGENTS.md` files is optional.** Inheritance already works without it; it
  exists only as a signpost for a reader — or an agent — handed that folder in isolation (a narrow
  subagent, a partial checkout), and to note that the folder keeps its own `.agents/`.
- **Claude loads nested files lazily** — a subfolder's `CLAUDE.md` enters context only when Claude
  reads a file in that subfolder, and after `/compact` only the root one is re-injected. Keep
  long-lived rules (code style, conventions) at the **root**, where they always load.
- **Codex caps the merged docs** at `project_doc_max_bytes` (32 KiB default) and stops accumulating
  past it — a reason to keep per-folder specifics lean.

Sources: [Claude Code memory](https://code.claude.com/docs/en/memory) ·
[Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) ·
[OpenCode rules](https://opencode.ai/docs/rules/)

## Layout

```
actdim-agents/
  install.ps1 / install.bat     # Windows installer
  install.sh                    # Linux / macOS installer
  skills/
    init-agents/                # SKILL.md + protocol.md + init-agents.sh
    wrap-session/               # SKILL.md
    sync-context/               # SKILL.md
    sync-issues/                # SKILL.md
    sync-tasks/                 # SKILL.md (alias)
    sync-decisions/             # SKILL.md
```

The authoritative protocol text is `skills/init-agents/protocol.md`.

## Install

Targets: `claude`, `codex`, `opencode`, `antigravity`, `both` (claude+codex), `all` (default).

**Windows:**
```
install.bat                     # all (copy); re-run after `git pull` to update
install.bat -Target antigravity # one provider
install.bat -Symlink            # symlink skill folders (claude/codex/antigravity); needs admin / Developer Mode
```

**Linux / macOS:**
```
bash install.sh                 # all (copy)
bash install.sh --target=antigravity # one provider
bash install.sh --symlink       # symlink skill folders (claude/codex/antigravity)
```

## Use

- In a repo (or subfolder) run `/init-agents` (or `bash skills/init-agents/init-agents.sh <dir>`)
  to scaffold `AGENTS.md` + `CLAUDE.md` + `.agents/`.
- Work as usual; use `/wrap-session` at the end of a stage or session (or `/sync-context` / `/sync-issues` for focused updates).


