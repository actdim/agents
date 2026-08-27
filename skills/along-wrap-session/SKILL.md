---
name: along-wrap-session
description: Wrap up the current coding session by updating the repo's .along/ state - write a session log file, refresh CONTEXT, update the ISSUES board (moving completed issues to ISSUES/done/), append a HISTORY line, and record any decisions/glossary terms. Use when the user ends a session, says to wrap up / save context / log the session, or invokes /along-wrap-session.
---

# Along Wrap Session (`/along-wrap-session`) [v2.0.1]

Mandatory session finalization protocol.

## Execution Checklist
1. **Verification & Tests**: Run automated unit tests / linting / builds with quiet flags.
2. **Code Review & Blast Radius Assessment**:
   - Inspect git diff for unintended side effects, unhandled nulls/errors, and edge cases.
   - Evaluate systemic blast radius on callers/dependents using `code-review-graph` or AST analysis.
   - Verify compliance with architectural decisions in `.along/DECISIONS.md`.
3. **Entity Reconciliation**: Move completed issues to `.along/ISSUES/done/` with `status: done`, `completed: YYYY-MM-DD`, and `protocol: along`.
4. **Milestone Tracking**: Update `.along/MILESTONES/` progress percentages.
5. **Session Log**: Write `.along/SESSIONS/<YYYY>/<YYYY-MM-DD>--<slug>.md` with `protocol: along` and a concise Code Review & Impact summary.
6. **CONTEXT Snapshot**: Rewrite `.along/CONTEXT.md` (< 20 lines).
7. **ISSUES Board**: Update `.along/ISSUES.md`.
8. **HISTORY**: Append one line to `.along/HISTORY.md`.
9. **Compaction Prompt**: Advise user to run `/compact`.
