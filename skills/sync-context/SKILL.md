---
name: sync-context
description: Refresh the nearest .agents/CONTEXT.md into a short, accurate current-state snapshot ("you are here"). Use when the user wants to update / save / maintain context, checkpoint state mid-session, or invokes /sync-context. Keeps CONTEXT compact and pushes history into session logs. Requires an .agents/ structure (created by init-agents).
---

# sync-context

Maintain `CONTEXT.md`. Operate on the NEAREST `.agents/` for the folder you're working in (walk UP the tree; fall back to a higher-level one). If none exists anywhere up the tree, tell the user to run `init-agents` first and stop.

## Do
1. Read the current `.agents/CONTEXT.md`.
2. Rewrite it to reflect the CURRENT state of the project: where things stand right now, what is in flight, important gotchas/constraints discovered, and the immediate next step. It is a SNAPSHOT of the present truth, NOT a changelog.
3. Keep it SHORT — about one screen at most. Anything that is history (what happened, step by step) belongs in a session log, not here; if CONTEXT has accumulated log-like detail, compress it out.
4. Do not reproduce the issue board — you may reference active issues by slug, but the issue list lives in `ISSUES.md`.

## Rules
- Verify claims against the actual code/repo before writing them — CONTEXT must be true NOW.
- Never write secrets / credentials / tokens / keys.
- Do not `git add` / commit unless the user asks.

## Report
State the path you rewrote and a one-line summary of the new current state.
