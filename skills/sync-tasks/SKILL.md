---
name: sync-tasks
description: Reconcile the nearest .agents/ task board (TASKS.md) and per-task files (TASKS/<slug>.md) with the actual current work — create/update task files with status, keep the board accurate, and move completed tasks to TASKS/done/. Use when the user wants to capture or describe a task, update task status, groom the backlog, or invokes /sync-tasks. Requires an .agents/ structure (created by init-agents).
---

# sync-tasks

Maintain the task board and per-task files. Operate on the NEAREST `.agents/` for the folder you're working in (walk UP the tree; fall back to a higher-level one). If none exists anywhere up the tree, tell the user to run `init-agents` first and stop.

## Do
1. Determine the current work from the conversation, `git status --short` / the diff, and any slug/description the user passed as an argument. Get today's date via `date +%F`.
2. For each distinct piece of work, ensure a task file `.agents/TASKS/<slug>.md` exists (`<slug>` = lowercase kebab-case, 2–5 words; the slug IS the id). Front-matter + body:
   ```
   ---
   slug: <slug>
   status: open            # open | in-progress | blocked | done
   created: <YYYY-MM-DD>
   updated: <YYYY-MM-DD>
   ---
   # <Title>
   Goal / acceptance criteria / steps / links to sessions & decisions (by slug / #N).
   ```
3. Update `status` and `updated` to match reality. When a task is DONE, MOVE its file to `.agents/TASKS/done/<slug>.md`.
4. Update the board `.agents/TASKS.md` so every task file has a line under **Active** or **Done**, with the right glyph (`[ ]` open, `[~]` in-progress, `[!]` blocked, `[x]` done) and a relative link to its file. Keep the board compact.

## Rules
- Reference tasks by slug, never by path. Filenames stay stable; the only move is open → `TASKS/done/`.
- Never write secrets / credentials / tokens / keys.
- Do not `git add` / commit unless the user asks.

## Report
List the task files created / updated / moved and the board changes.
