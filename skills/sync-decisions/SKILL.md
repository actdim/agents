---
name: sync-decisions
description: Record architectural/design decisions into the nearest .agents/DECISIONS.md as append-only ADR entries, and mark superseded ones. Use when a non-trivial technical choice was made or discussed, when the user says to log/record a decision or an ADR, or invokes /sync-decisions. Requires an .agents/ structure (created by init-agents).
---

# sync-decisions

Maintain `DECISIONS.md`. Operate on the NEAREST `.agents/` for the folder you're working in (walk UP the tree; fall back to a higher-level one). If none exists anywhere up the tree, tell the user to run `init-agents` first and stop.

## Do
1. Read the current `.agents/DECISIONS.md` — both to find the next entry number and to see what was already decided (never restate or contradict an existing entry).
2. Identify the decisions worth recording from this session's work/conversation (plus any the user named as an argument). A decision qualifies when it **constrains future work**: an API shape or contract, an ownership/lifetime model, a naming convention, a technology/library choice, a deliberate trade-off. Skip routine implementation details and bug fixes — those belong in the session log.
3. APPEND one entry per decision (get today's date via `date +%F`), numbered sequentially:
   ```
   ## #NNN — <title>
   - Date: <YYYY-MM-DD>
   - Status: accepted
   - Context: <what forced the choice — the problem, constraints, alternatives considered>
   - Decision: <what was chosen, stated so it can be followed>
   - Consequences: <trade-offs accepted, what this obliges callers/future work to do, follow-ups>
   ```
4. If a new decision REPLACES an older one: leave the old entry's text intact and only change its `Status:` to `superseded by #NNN`; the new entry should reference the one it replaces. Never edit, renumber, reorder, or delete past entries — this file is append-only.
5. Cross-reference where useful: issue slugs and session files that carry the work out.

## Rules
- Capture the *why*, not a diff — an entry must still make sense a year later, without the chat.
- One decision per entry; keep each entry tight (a few lines per field).
- Never write secrets / credentials / tokens / keys.
- Do not `git add` / commit unless the user asks.

## Report
List the entry numbers and titles you appended, plus any entries you marked superseded.
