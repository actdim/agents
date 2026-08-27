---
name: along-wrap
description: Wrap up the current coding session or completed work stage by updating the repo's .along/ state - execute code review checklist, write a session log file, refresh CONTEXT.md, move completed issues to ISSUES/done/, append a HISTORY line, and record decisions/glossary terms. Use when ending work, wrapping up, or when invoking /along-wrap, /along-wrap-session, or /along-wrap-stage.
---

# Along Wrap (`/along-wrap`) [v2.0.8]

Universal finalization and memory synchronization protocol for sessions, tasks, and milestone stages.

---

## When to Use
- The user or agent completes a feature, bugfix, stage, or ends a work session (triggers: "wrap up", "заверши сессию", "закрой этап", `/along-wrap`, `/along-wrap-session`, `/along-wrap-stage`).
- An active issue acceptance criteria have been verified and ready to close.

---

## Mandatory Execution Checklist (Execute in Exact Order)

1. [ ] **Verification & Tests**: Run automated unit tests / linting / builds with quiet flags (`/along-test` or `/along-build`).
2. [ ] **Code Review & Blast Radius Assessment**:
   - Inspect `git diff` for unintended side effects, unhandled nulls/errors, and edge cases.
   - Evaluate systemic blast radius on callers/dependents using `code-review-graph` (`get_impact_radius_tool`, `get_affected_flows_tool`) or AST analysis.
   - Verify compliance with architectural decisions in `.along/DECISIONS.md`.
3. [ ] **Entity Reconciliation**:
   - Set `status: done` and `completed: YYYY-MM-DD` for finished issues; MOVE to `.along/ISSUES/done/<type>--<slug>.md`.
   - Update related `.along/MILESTONES/` progress percentages.
   - Resolve mitigated `.along/RISKS/` (`status: resolved` / `mitigated`).
   - Conclude active `.along/SPIKES/` and log any resulting ADR in `.along/DECISIONS.md`.
4. [ ] **Documentation Check**: Update `README.md`, `AGENTS.md` (project specifics), or `.along/KB/` if code interfaces or architecture changed.
5. [ ] **Session Log**: Write `.along/SESSIONS/<YYYY>/<YYYY-MM-DD>--<short-slug>.md` with complete front-matter (`protocol: along`, `issues_advanced`, `issues_completed`, `decisions`, `risks_logged`, `spikes_conducted`) and a concise Code Review & Impact summary.
6. [ ] **CONTEXT Snapshot**: Rewrite `.along/CONTEXT.md` to a short "you are here" snapshot (< 20 lines).
7. [ ] **ISSUES Board**: Update `.along/ISSUES.md` (keep active list lean, reflect done items).
8. [ ] **HISTORY**: Append one line to `.along/HISTORY.md`: `<YYYY-MM-DD> - <slug> - <agent> - <summary> - <link>`.
9. [ ] **Compaction Prompt**: Advise user to run `/compact` to free up token budget.

