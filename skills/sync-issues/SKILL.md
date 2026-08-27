---
name: sync-issues
description: Reconcile the nearest .agents/ issue board (ISSUES.md) and per-issue files (ISSUES/<type>--<slug>.md) for the target subproject/area - create/update issue files with status/priority in the nearest .agents/, keep the board accurate, and move completed issues to ISSUES/done/. Use when the user wants to capture or describe an issue/bug/feature/debt item, update issue status, groom the backlog, or invokes /sync-issues. Requires an .agents/ structure (created by init-agents).
---

# sync-issues

Maintain the issue board and per-issue files.

**Targeting Rule**: Operate on the NEAREST `.agents/` folder corresponding to the specific subproject/area affected by the issue. If working in a subfolder or creating an issue for a subproject that carries its own `.agents/` directory, create/update the issue inside THAT subfolder's `.agents/ISSUES/` (and its `.agents/ISSUES.md`), NOT in the root `.agents/`. Only repository-wide / cross-project issues belong in the root `.agents/`. If no `.agents/` exists anywhere up the tree for the target area, tell the user to run `init-agents` first and stop.

## Do
1. Identify the target folder for the issue (the specific subproject or area being changed). Locate its NEAREST `.agents/` directory.
2. Determine the current work from the conversation, `git status --short` / the diff, and any slug/description/type the user passed as an argument. Get today's date via `date +%F`.
3. For each distinct issue, ensure a file `.agents/ISSUES/<type>--<slug>.md` exists inside that NEAREST `.agents/`:
   - `<type>`: `feat` (feature) | `bug` (bug fix) | `debt` (tech debt / refactoring) | `task` (general task) | `docs` (documentation).
   - `<slug>`: lowercase kebab-case, 2-5 words.
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
4. Update `status` and `updated` to match reality. When an issue is DONE, MOVE its file to `.agents/ISSUES/done/<type>--<slug>.md` within that same nearest `.agents/`.
5. Update the board `.agents/ISSUES.md` in that nearest `.agents/` so every issue file has a line under **Active**, **Backlog**, or **Done (recent)**, with the right glyph (`[ ]` open, `[~]` in-progress, `[!]` blocked, `[x]` done), type tag, and relative link:
   - Example line: `- [~] (feat) [add-user-login](file://.agents/ISSUES/feat--add-user-login.md)`

## Rules
- Always create and maintain issue files in the NEAREST `.agents/` directory for the subproject/area affected. Never dump subproject issues into the root `.agents/` if a subfolder `.agents/` exists.
- Reference issues by slug/file, keep filenames as `<type>--<slug>.md`. The only move is open → `ISSUES/done/`.
- Never write secrets / credentials / tokens / keys.
- Do not `git add` / commit unless the user asks.

## Report
List the issue files created / updated / moved, the board changes, and the target `.agents/` path used.
