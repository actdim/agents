---
name: along-wrap-session
description: Wrap up the current coding session by updating the repo's .along/ state - write a session log file, refresh CONTEXT, update the ISSUES board (moving completed issues to ISSUES/done/), append a HISTORY line, and record any decisions/glossary terms. Use when the user ends a session, says to wrap up / save context / log the session, or invokes /along-wrap-session.
---

# Along Wrap Session (`/along-wrap-session`) [v2.0.0]

Mandatory session finalization protocol.

## Execution Checklist
1. Run automated tests / linting / builds with quiet flags.
2. Reconcile entities: move completed issues to `.along/ISSUES/done/` with `status: done`, `completed: YYYY-MM-DD`, and `protocol: along`.
3. Update `.along/MILESTONES/` progress percentages.
4. Write `.along/SESSIONS/<YYYY>/<YYYY-MM-DD>--<slug>.md` with `protocol: along`.
5. Rewrite `.along/CONTEXT.md` (< 20 lines).
6. Update `.along/ISSUES.md`.
7. Append one line to `.along/HISTORY.md`.
8. Advise user to run `/compact`.
