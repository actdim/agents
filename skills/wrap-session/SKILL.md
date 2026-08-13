---
name: wrap-session
description: Wrap up the current coding session by updating the repo's .agents/ state — write a session log file, refresh CONTEXT, update the ISSUES board (moving completed issues to ISSUES/done/), append a HISTORY line, and record any decisions/glossary terms. Use when the user ends a session, says to wrap up / save context / log the session, or invokes /wrap-session. Requires the .agents/ structure to exist (created by init-agents).
---

# wrap-session (and /wrap-stage)

Perform the end-of-stage or end-of-session update defined by the repo's agent context protocol. Operate on the NEAREST `.agents/` for the folder you're working in (walk UP the tree; fall back to a higher-level one). If no `.agents/` exists anywhere up the tree, tell the user to run `init-agents` first and stop.

## Stage Completion Triggers
Recognize that a **Stage** is complete when:
1. **Issue Acceptance Met**: An active Issue (`.agents/ISSUES/<type>--<slug>.md`) acceptance criteria and verification pass.
2. **Plan Milestone Reached**: A distinct phase of an implementation plan agreed with the user is complete.
3. **Explicit Request**: The user invokes `/wrap-session`, `/wrap-stage`, or asks to checkpoint.

## Gather header facts (via the Bash tool)
- Date: `date +%F` and year `date +%Y`.
- Branch: `git rev-parse --abbrev-ref HEAD`.
- Commit: `git rev-parse --short HEAD`.
- Working tree (for your own summary): `git status --short`.
- Agent identity = your tool + model (e.g. "Claude Code / claude-opus-4-8"). If the user passed a slug or one-line summary hint when invoking, use it for the slug/summary.

## Update, in this order
1. **Documentation Check** — Check if `README.md`, `AGENTS.md` (project conventions), or project documentation need updates following the completed stage/task. Update them or prompt the user with required doc changes.
2. **Session log** — write a NEW file `.agents/SESSIONS/<YYYY>/<YYYY-MM-DD>--<short-slug>.md`
   (`<short-slug>` = lowercase kebab-case, 2–5 words describing the work; if the file already exists, suffix `-02`, `-03`…). Create the year folder if missing. Start with YAML front-matter, then the body:
   ```
   ---
   date: <YYYY-MM-DD>
   slug: <short-slug>
   agent: <tool / model>          # e.g. Claude Code / claude-opus-4-8
   branch: <branch>
   commit: <short-hash>
   summary: <one-line summary>
   ---
   # <Title>

   What changed this session and why; files touched; decisions made (by slug / #N);
   issues advanced (by slug); known gaps / follow-ups.
   ```
3. **CONTEXT** — rewrite `.agents/CONTEXT.md` to the NEW current state. Keep it SHORT — a snapshot, not a log; push detail into the session file. If it has grown past ~1 screen, compress it.
4. **ISSUES** — update `.agents/ISSUES.md` and the relevant `.agents/ISSUES/<type>--<slug>.md`: mark progress; for any completed issue MOVE its file to `.agents/ISSUES/done/<type>--<slug>.md` and update the board line. Add newly discovered issues (new file + board line). Keep the board lean.
5. **DECISIONS** — if any non-trivial architectural/design decision was made this session, APPEND a dated entry to `.agents/DECISIONS.md` (never edit past entries; mark a replaced one "Superseded by #N").
6. **GLOSSARY** — if any domain term was introduced/clarified, add it to `.agents/GLOSSARY.md`.
7. **HISTORY** — APPEND one line to `.agents/HISTORY.md`:
   `<YYYY-MM-DD> — <short-slug> — <agent> — <one-line summary> — <relative link to the session file>`.
8. **VISION** — update `.agents/VISION.md` ONLY if scope/roadmap actually changed.

## Rules
- Filenames Windows-safe: `YYYY-MM-DD`, no `:`, date first. Reference issues by slug, not path.
- Keep `CONTEXT.md` and `ISSUES.md` compact.

- NEVER write secrets/credentials/tokens into these files.
- Do not `git add`/commit unless the user asks.

## Report
Print a concise list of exactly which files you wrote/updated/moved.
