---
name: sync-issues
description: Reconcile the nearest .agents/ issue board (ISSUES.md) and per-issue files (ISSUES/<type>--<slug>.md) with the actual current work — create/update issue files with status/priority, keep the board accurate, and move completed issues to ISSUES/done/. Use when the user wants to capture or describe an issue/bug/feature/debt item, update issue status, groom the backlog, or invokes /sync-issues. Requires an .agents/ structure (created by init-agents).
---

# sync-issues

Maintain the issue board and per-issue files. Operate on the NEAREST `.agents/` for the folder you're working in (walk UP the tree; fall back to a higher-level one). If none exists anywhere up the tree, tell the user to run `init-agents` first and stop.

## Do
1. Determine the current work from the conversation, `git status --short` / the diff, and any slug/description/type the user passed as an argument. Get today's date via `date +%F`.
2. For each distinct issue, ensure a file `.agents/ISSUES/<type>--<slug>.md` exists:
   - `<type>`: `feat` (feature) | `bug` (bug fix) | `debt` (tech debt / refactoring) | `task` (general task) | `docs` (documentation).
   - `<slug>`: lowercase kebab-case, 2–5 words.
   - Front-matter + body:
     ```yaml
     ---
     slug: <slug>
     type: <feat | bug | debt | task | docs>
     status: open            # open | in-progress | blocked | done
     priority: medium        # critical | high | medium | low
     created: <YYYY-MM-DD>
     updated: <YYYY-MM-DD>
     ---
     # <Title>
     Goal / acceptance criteria / steps / links to sessions & decisions (by slug / #N).
     ```
3. Update `status` and `updated` to match reality. When an issue is DONE, MOVE its file to `.agents/ISSUES/done/<type>--<slug>.md`.
4. Update the board `.agents/ISSUES.md` so every issue file has a line under **Active**, **Backlog**, or **Done (recent)**, with the right glyph (`[ ]` open, `[~]` in-progress, `[!]` blocked, `[x]` done), type tag, and relative link:
   - Example line: `- [~] (feat) [add-user-login](file://.agents/ISSUES/feat--add-user-login.md)`

## Rules
- Reference issues by slug/file, keep filenames as `<type>--<slug>.md`. The only move is open → `ISSUES/done/`.
- Never write secrets / credentials / tokens / keys.
- Do not `git add` / commit unless the user asks.

## Report
List the issue files created / updated / moved and the board changes.
