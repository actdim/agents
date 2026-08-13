---
name: init-agents
description: Scaffold or refresh the provider-agnostic agent-context structure in a repository — root AGENTS.md (with a managed block carrying the agent-context protocol), a CLAUDE.md that imports it, and the .agents/ directory (CONTEXT, TASKS + TASKS/, DECISIONS, VISION, GLOSSARY, HISTORY, SESSIONS). Use when the user wants to set up agent context/instructions for a project, initialize the agent structure, or invokes /init-agents. Idempotent — re-running refreshes only the managed protocol block and never overwrites existing dynamic state files.
---

# init-agents

Scaffold (or refresh) the agent-context structure for a project. Codex, OpenCode, and Antigravity (read `AGENTS.md` natively) as well as Claude Code (reads `CLAUDE.md`, which imports `AGENTS.md`) will then pick it up. There is intentionally NO global config — this skill is the single source of truth and stamps everything into the repo.


**Preferred execution:** run the deterministic helper `bash "<this skill's folder>/init-agents.sh" [TARGET_DIR]` — it does ALL the mechanical work below exactly and idempotently (FULL vs REF detection via walk-up, `.agents/` skeletons, the `CLAUDE.md` pointer, and moving a folder-own `VISION.md` into `.agents/` with the source deleted). It runs under Git Bash on Windows. After it finishes, do ONLY the judgment parts the script cannot: relocate any legacy hand-written `AGENTS.md`/`CLAUDE.md` content into `## Project specifics`, and fill in specifics. The step-by-step spec below is what the script implements — follow it by hand only if you cannot run the script.

## Target directory (`<root>`)
Resolve the target directory deterministically, in this priority:
1. If the user named a directory (in chat) or passed one as an argument to the command — use that exactly.
2. Otherwise determine the repository root: run `git rev-parse --show-toplevel` and use its output.
3. If that fails (not a git repo), use the current working directory.
Do NOT infer the target from whichever file is open in the editor. State the resolved `<root>` to the user before scaffolding. Never scaffold into a subfolder's own copy of the shared state.

## Idempotency & merge policy
Re-running this skill MUST be safe — never destroy existing work. Before writing anything, READ every one of these files that already exists, so you merge against their real content.
- `.agents/` state files (`CONTEXT.md`, `TASKS.md`, `TASKS/*`, `DECISIONS.md`, `VISION.md`, `GLOSSARY.md`, `HISTORY.md`, `SESSIONS/*`): if the file already exists, LEAVE IT EXACTLY AS IS — do not rewrite, reformat, reorder, or "upgrade" it. Only CREATE the ones that are missing (from the skeletons in Step 3).
- `AGENTS.md` and `CLAUDE.md`: MERGE, never overwrite. Regenerate ONLY the skill-managed parts (the protocol block / the import line); preserve ALL pre-existing hand-written content verbatim — just re-lay-it-out into the new-standard structure. Take the file's current content as the base and fold the skill's parts into it.
- Importing a doc into `.agents/` (e.g. a folder's own `VISION.md`) is a MOVE, not a copy: copy the content into the `.agents/` file, then DELETE the source. This is allowed — the content is preserved in its new home, so the deletion removes only a stale duplicate, it does not destroy work.

## Step 1 — `<root>/AGENTS.md` (managed protocol block)
The protocol lives inside `AGENTS.md` (so Codex reads it natively), in a managed block fenced by marker comments. To avoid duplicating the whole protocol in every nested folder, there are TWO variants — the FULL protocol is written only ONCE (at the architecture root) and nested folders carry a short REF that points up to it.

Choose the variant by walking UP the tree: from `<root>`'s PARENT upward, find the nearest ancestor folder whose `AGENTS.md` contains a FULL block (its BEGIN marker starts with `<!-- BEGIN ACTDIM-AGENTS-PROTOCOL root`).
- If NONE is found → `<root>` IS the architecture root. Use the **FULL** block: BEGIN marker `<!-- BEGIN ACTDIM-AGENTS-PROTOCOL root (managed by init-agents — do not edit by hand) -->`, then the PROTOCOL TEXT below, then `<!-- END ACTDIM-AGENTS-PROTOCOL -->`.
- If one is found at ancestor `A` → `<root>` is NESTED. Do NOT repeat the protocol; use a short **REF** block pointing to `A` (relative path):
  ```
  <!-- BEGIN ACTDIM-AGENTS-PROTOCOL ref=<relpath from <root> to A/AGENTS.md> (managed by init-agents — do not edit by hand) -->
  This folder belongs to a repository that uses the init-agents structure. The full working
  guidance + agent-context protocol live once in the nearest ancestor `AGENTS.md`
  (`<relpath>`) — read it there. This folder keeps its OWN `.agents/` state; use the nearest one.
  Only this folder's specifics follow.
  <!-- END ACTDIM-AGENTS-PROTOCOL -->
  ```

Behaviour (whichever variant you chose):
- If `AGENTS.md` does NOT exist: create it as the chosen managed block, a blank line, then a `## Project specifics` stub:
  ```
  ## Project specifics

  <!-- Fill in: what this project is, how to build / test / run, architecture map, project-specific conventions. -->
  ```
- If `AGENTS.md` EXISTS and already has the markers: replace ONLY the text between them with the chosen block; never touch anything outside. (If an ancestor gained a FULL block since the last run, this correctly downgrades a FULL block to a REF block — that is expected.)
- If `AGENTS.md` EXISTS but has NO markers (legacy / hand-written file): MIGRATE it — put the chosen managed block at the TOP, then the pre-existing content below it UNCHANGED (under a `## Project specifics` heading if it isn't already under one). Do not delete, reword, or reorder the pre-existing content.

The PROTOCOL TEXT to place between the markers is the canonical file **`protocol.md`** (same folder as this skill) — that is the single source of truth; stamp its contents verbatim. The copy reproduced below is for reference only and must be kept identical to `protocol.md`:

---
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

## Stage Completion Triggers
A **Stage** (or milestone phase) is a meaningful, verified unit of work. An agent MUST recognize that a Stage is complete when:
1. **Issue Acceptance Met**: An active Issue (`.agents/ISSUES/<type>--<slug>.md`) has satisfied its acceptance criteria and passes verification.
2. **Plan Milestone Reached**: A distinct phase of an implementation plan agreed with the user is complete.
3. **Explicit Request**: The user asks to wrap up, checkpoint, or complete the current stage.

## Stage & Session Wrap-up Protocol (Update in order)
When a Stage or session completes, perform the following steps:
1. **Documentation & Protocol Check** — Review if `README.md`, `AGENTS.md` (project conventions), or project guides need updates following the completed stage/task. Update them or report required doc updates.
2. **Session log** — Write a new session file `.agents/SESSIONS/<YYYY>/<YYYY-MM-DD>--<short-slug>.md` (slug 2–5 words; if it exists, suffix `-02`…). Begin with YAML front-matter (`date`, `slug`, `agent` = tool/model, `branch`, `commit`, `summary`), then a body: what changed & why, files touched, decisions (by slug/#N), issues advanced, gaps/follow-ups.
3. **CONTEXT** — Rewrite `.agents/CONTEXT.md` to the new state — a SHORT snapshot, not a log; history goes to the session file.
4. **ISSUES** — Update `.agents/ISSUES.md` (+ move any completed issue to `ISSUES/done/`).
5. **HISTORY** — Append one line to `.agents/HISTORY.md`: `<YYYY-MM-DD> — <slug> — <agent> — <summary> — <link>`.
6. **VISION** — Touch `.agents/VISION.md` only if scope/roadmap changed.

## Rules
- Windows-safe filenames: dates `YYYY-MM-DD` (no `:`), date first. Issue files keep a stable `<type>--<slug>.md` name; the only move is open → `ISSUES/done/`.
- Keep `CONTEXT.md` and `ISSUES.md` compact — they cost context every session.
- Never write secrets/credentials/tokens/keys into these files; they are committed.
---

## Step 2 — `<root>/CLAUDE.md`
The import line (so Claude Code inlines the protocol) is:
```
See @AGENTS.md for project instructions and guidance.
```
- If `CLAUDE.md` does NOT exist: create it containing exactly that line.
- If `CLAUDE.md` EXISTS: leave all its content verbatim; only ensure the `@AGENTS.md` import line is present. If it is missing, PREPEND it (as the first line, followed by a blank line) so it is imported. If it is already present, make NO changes to the file.

## Step 3 — `.agents/` skeletons (create ONLY IF MISSING; never overwrite existing state)
Determine the current year via `date +%Y` and today's date via `date +%F`.

- `.agents/CONTEXT.md`:
  ```
  # Context

  _Current-state snapshot. Keep SHORT; history goes to SESSIONS/._

  - Status: initialized (no work recorded yet).
  ```
- `.agents/ISSUES.md`:
  ```
  # Issues   (glyphs: [ ] open  [~] in-progress  [!] blocked  [x] done)

  ## Active

  ## Backlog

  ## Done (recent)
  ```
- `.agents/ISSUES/.gitkeep` and `.agents/ISSUES/done/.gitkeep` (empty).
- `.agents/DECISIONS.md`:
  ```
  # Decisions (ADR — append-only)

  _One dated entry per architectural decision. Never edit past entries; mark a replaced one "Superseded by #N"._

  <!-- Template:
  ## #001 — <title>
  - Date: YYYY-MM-DD
  - Status: accepted            (or: superseded by #NNN)
  - Context: <why this came up>
  - Decision: <what was decided>
  - Consequences: <trade-offs / follow-ups>
  -->
  ```
- `.agents/VISION.md` — a VISION belongs to the folder it sits in; there is no "global" vision and you never hoist one up a level. If `.agents/VISION.md` does NOT already exist:
  - If `<root>/VISION.md` exists (a vision sitting DIRECTLY in this folder): MOVE it into `.agents/VISION.md` — copy the content across (preserve the wording as-is; keep the standard `# Vision` heading), then DELETE the source `<root>/VISION.md`. It is a move, not a copy: the content now lives in `.agents/VISION.md`, so a leftover original would just be a stale duplicate. Report the move. A `VISION.md` in a SUBFOLDER belongs to that subfolder — leave it for when init-agents runs there; never pull it up.
  - Otherwise create `.agents/VISION.md` from this skeleton:
    ```
    # Vision

    _North star: scope, boundaries, non-goals, roadmap. Evolves slowly; slims as features ship._

    ## Scope

    ## Non-goals

    ## Roadmap
    ```
  - (If `.agents/VISION.md` ALREADY exists, per the merge policy leave it as-is.)
- `.agents/GLOSSARY.md`:
  ```
  # Glossary

  _Domain terms. Add a term when you introduce or clarify it._

  <!-- - **Term** — definition. -->
  ```
- `.agents/HISTORY.md`:
  ```
  # History

  _Index of sessions (newest last). One line per session:_
  _`<YYYY-MM-DD> — <slug> — <agent> — <summary> — <relative link>`_
  ```
- `.agents/SESSIONS/<current-year>/.gitkeep` (empty).

## Step 4 — Report
Print a concise summary: which files were CREATED, which had the managed block UPDATED/MERGED (FULL vs REF), which existing state files were LEFT UNTOUCHED, and any docs MOVED into `.agents/` (e.g. `VISION.md`) with their source paths noting the source was deleted. Do not run `git add`/commit unless the user asks.
