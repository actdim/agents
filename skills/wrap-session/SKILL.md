---
name: wrap-session
description: Wrap up the current coding session by updating the repo's .agents/ state - write a session log file, refresh CONTEXT, update the ISSUES board (moving completed issues to ISSUES/done/), append a HISTORY line, and record any decisions/glossary terms. Use when the user ends a session, says to wrap up / save context / log the session, or invokes /wrap-session. Requires the .agents/ structure to exist (created by init-agents).
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

## Mandatory Stage & Session Wrap-up Checklist (Execute in exact order)
Agents MUST execute the following verification steps:

1. **Verification & Tests** - Run unit tests, linters, or build commands with quiet flags (`pytest -q`, `dotnet test -v q`, `npm test --silent`). Ensure no broken builds or lint errors remain.
2. **Entity & Issue Reconciliation**:
   - **Issues**: For completed issues, set `status: done` and `completed: <YYYY-MM-DD>` in their YAML front-matter, and MOVE the file to `.agents/ISSUES/done/<type>--<slug>.md`.
   - **Milestones**: If working towards a milestone, update progress in `.agents/MILESTONES/<slug>.md`.
   - **Risks**: Mark resolved risks as `status: resolved` / `mitigated` in `.agents/RISKS/<slug>.md`.
   - **Spikes**: Conclude active spikes in `.agents/SPIKES/<slug>.md` and link resulting ADRs.
3. **Documentation Check** - Check if `README.md`, `AGENTS.md` (project specifics), or `.agents/KB/` need updates following the completed task.
4. **Session log** - write a NEW file `.agents/SESSIONS/<YYYY>/<YYYY-MM-DD>--<short-slug>.md`
   (`<short-slug>` = lowercase kebab-case, 2-5 words describing the work; if the file already exists, suffix `-02`, `-03`...). Create the year folder if missing. Start with YAML front-matter:
   ```yaml
   ---
   date: <YYYY-MM-DD>
   slug: <short-slug>
   agent: <tool / model>          # e.g. Gemini 3.7 Flash / Antigravity
   branch: <branch>
   commit: <short-hash>
   summary: <one-line summary>
   milestone: <optional-milestone-slug>
   issues_advanced: [<issue-slug-1>, <issue-slug-2>]
   issues_completed: [<completed-slug>]
   decisions: ["#001", "#002"]
   risks_logged: [<risk-slug>]
   spikes_conducted: [<spike-slug>]
   ---
   # <Title>

   What changed this session and why; files touched; decisions made (by slug / #N);
   issues advanced (by slug); known gaps / follow-ups.
   ```
5. **CONTEXT** - rewrite `.agents/CONTEXT.md` to the NEW current state. Keep it SHORT - a snapshot (< 20 lines), not a log; push detail into the session file.
6. **ISSUES** - update `.agents/ISSUES.md` (keep active list lean, reflect done items).
7. **DECISIONS** - if any non-trivial architectural/design decision was made this session, APPEND a dated entry to `.agents/DECISIONS.md`.
8. **GLOSSARY** - if any domain term was introduced/clarified, add it to `.agents/GLOSSARY.md`.
9. **HISTORY** - APPEND one line to `.agents/HISTORY.md`:
   `<YYYY-MM-DD> - <short-slug> - <agent> - <one-line summary> - <relative link to the session file>`.
10. **VISION** - update `.agents/VISION.md` ONLY if scope/roadmap actually changed.

## Rules
- Filenames Windows-safe: `YYYY-MM-DD`, no `:`, date first. Reference issues by slug, not path.
- Keep `CONTEXT.md` and `ISSUES.md` compact.

- NEVER write secrets/credentials/tokens into these files.
- Do not `git add`/commit unless the user asks.

## Report
1. Print a concise list of exactly which files you wrote/updated/moved.
2. Prompt the user to compact their session context:
   > 💡 **Context Tip**: Stage/Session state is safely committed to `.agents/`. If continuing in the same chat, run `/compact` (or start a fresh session) to free up token budget.
