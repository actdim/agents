<!-- BEGIN ACTDIM-AGENTS-PROTOCOL root (managed by init-agents — do not edit by hand) -->
# ACTDIM-AGENTS-PROTOCOL

This repo carries its own agent context, provider-agnostically. Follow it every session, whatever tool you are.

## Scope & precedence
- Any folder may carry its own `AGENTS.md` + `.agents/`; they apply to that folder and everything under it. Use the NEAREST ones for the area you're working in; higher-level ones add broader context. On conflict, the more specific wins.
- Global/user config still applies as defaults (Claude auto-loads `~/.claude/CLAUDE.md`, Codex `~/.codex/AGENTS.md`, Antigravity `~/.gemini/config/GEMINI.md`). Precedence: nearest > higher-level > global.

## At session start — read these yourself (they are NOT auto-loaded)
Use the NEAREST `.agents/` for the area you're working in (fall back to a higher-level one if the folder has none):
1. `AGENTS.md` (nearest) — conventions to follow.
2. `.agents/CONTEXT.md` — current state.
3. `.agents/ISSUES.md` — active issue board.
4. `.agents/DECISIONS.md` — don't contradict.
Also, when relevant: `.agents/VISION.md`, `.agents/GLOSSARY.md`, and the `.agents/ISSUES/<type>--<slug>.md` you'll work on. These reflect the state WHEN WRITTEN — verify any named file/API/flag against the real code first.

## Issues
- One file per issue, formatted as `.agents/ISSUES/<type>--<slug>.md` (slug = lowercase kebab-case, 2–5 words).
- Supported types (`<type>`): `feat` (feature), `bug` (bug fix), `debt` (tech debt / refactoring), `task` (general task), `docs` (documentation).
- Issue YAML front-matter: `slug`, `type`, `status` (`open` | `in-progress` | `blocked` | `done`), `priority` (`critical` | `high` | `medium` | `low`), `created`, `updated`.
- `.agents/ISSUES.md` is the compact board read every session (`## Active`, `## Backlog`, `## Done (recent)`).
- On completion, MOVE the file to `.agents/ISSUES/done/<type>--<slug>.md` and update the board.

## While working
- Follow the conventions in `AGENTS.md`.
- `DECISIONS.md` is APPEND-ONLY: add a new dated entry per non-trivial architectural decision; never edit past ones — mark a replaced one "Superseded by #N".
- Add any new/clarified domain term to `.agents/GLOSSARY.md`.
- Keep the issue you touch current (its `status`/`updated` + board line); new work found = a new issue file.

## When you finish a stage/session — update, in order
1. New session file `.agents/SESSIONS/<YYYY>/<YYYY-MM-DD>--<short-slug>.md` (slug 2–5 words; if it exists, suffix `-02`…). Begin with YAML front-matter (`date`, `slug`, `agent` = tool/model, `branch`, `commit`, `summary`), then a body: what changed & why, files touched, decisions (by slug/#N), issues advanced, gaps/follow-ups.
2. Rewrite `.agents/CONTEXT.md` to the new state — a SHORT snapshot, not a log; history goes to the session file.
3. Update `.agents/ISSUES.md` (+ move any done issue to `ISSUES/done/`).
4. Append one line to `.agents/HISTORY.md`: `<YYYY-MM-DD> — <slug> — <agent> — <summary> — <link>`.
Touch `.agents/VISION.md` only if scope/roadmap changed.

## Rules
- Windows-safe filenames: dates `YYYY-MM-DD` (no `:`), date first. Issue files keep a stable `<type>--<slug>.md` name; the only move is open → `ISSUES/done/`.
- Keep `CONTEXT.md` and `ISSUES.md` compact — they cost context every session.
- Never write secrets/credentials/tokens/keys into these files; they are committed.

<!-- END ACTDIM-AGENTS-PROTOCOL -->

## Project specifics

This repository is `actdim-agents` — the provider-agnostic agent-context protocol and skills suite for Claude Code, Codex, OpenCode, and Antigravity.

- **Skills Source**: `skills/` (`init-agents`, `wrap-session`, `sync-context`, `sync-issues`, `sync-decisions`, `sync-tasks`).
- **Install Commands**:
  - Windows: `powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1 -Target all` (or `install.bat`).
  - Linux / macOS: `bash install.sh`.

