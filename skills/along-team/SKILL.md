---
name: along-team
description: Execute software development tasks via sequential multi-agent protocol (Supervisor -> Research -> Architect -> Living Plan -> Step Loops [Implement -> Review/Test -> Reassess]). Supports autonomous execution, /goal integration, and adaptive complexity routing.
---

# Along Team (`/along-team`) [v2.1.6]

Universal sequential multi-agent development protocol and state machine for complex engineering tasks.

---

## Core Philosophy

> **Plan globally, execute locally, verify after every step, replan whenever reality differs from the plan.**

The protocol replaces unstructured multi-agent chat and parallel swarms with a **deterministic sequential state machine**.

---

## When to Use & Triggers

- **Explicit Skill Invocation**: `/along-team <issue-slug>` or `/along-team` with a task description.
- **Autonomous Goal Trigger**: Whenever `/goal` is invoked in Antigravity or high-autonomy mode is requested for feature implementation.
- **Natural Language Triggers**: "Execute issue via team", "Run multi-agent pipeline", "Implement with agent team".

---

## Adaptive Complexity Routing (T-Shirt Sizing)

Before spawning subagents, the **Supervisor** evaluates task complexity to prevent token explosion:

| Size | Scope & Characteristics | Execution Path |
| :--- | :--- | :--- |
| **`S-Size`** | 1-2 files, clear scope, no architectural unknowns. | **Fast-Path**: Single-agent direct execution + automated tests. Zero subagents spawned. |
| **`M-Size`** | 3-5 files, isolated module/route, clear interface. | **Fast Loop**: Scout (`research`) -> Implementer (`self`) -> Reviewer (`self`) in one pass. |
| **`L / XL-Size`** | Cross-module impact, core refactoring, protocol migration, architectural unknowns. | **Full Protocol**: Complete sequential state machine with Step-by-Step Living Plan and Reassess loops. |

---

## Role Definitions & Primitives

All roles map to standard built-in agent primitives:

### 1. Supervisor (Lead Agent / Orchestrator)
- **Role**: State management, task decomposition, acceptance criteria enforcement, routing.
- **Execution**: Runs in parent agent context. Never becomes the low-level code implementer in L/XL tasks.

### 2. Researcher (Scout)
- **Question**: *What facts, dependencies, and constraints do we need to know?*
- **Execution**: `invoke_subagent` with `TypeName: "research"`, `enable_write_tools: false`.
- **Output**: Compact Markdown report (Facts, Dependencies, Constraints, Risks, Unknowns).

### 3. Architect
- **Question**: *How to structure the solution given known facts?*
- **Execution**: Supervisor runs architect mode to construct/update the **Living Plan**.
- **Output**: Ordered sequence of small, verifiable steps with explicit acceptance criteria per step.

### 4. Implementer (Worker)
- **Question**: *How to execute the current step?*
- **Execution**: `invoke_subagent` with `TypeName: "self"`, `Role: "Implementer"`, `Workspace: "branch"` or `"inherit"`.
- **Output**: Code changes, local unit tests, and brief summary of touched files.

### 5. Reviewer (Gatekeeper: Tester + Critic + Judge)
- **Question**: *Is the current step good enough to proceed?*
- **Execution**: `invoke_subagent` with `TypeName: "self"`, `Role: "Code Reviewer"`.
- **Scope**: Runs automated test runner (`along-test`), inspects `git diff`, checks blast radius (`code-review-graph`), enforces `.along/DECISIONS.md` and clean ASCII rules.
- **Output**: `PASS` or `FAIL` with actionable issue list.

---

## Sequential State Machine

```text
TASK / GOAL
    |
    v
[Phase 0: Analyze] ------------> S-Size? --> [Direct Fast-Path] --> [Wrap]
    | (L / XL-Size)
    v
[Phase 1: Research] (invoke_subagent: research)
    |
    v
[Phase 2: Architect] (Produce Living Plan)
    |
    v
+----------------------------------------+
| Phase 3: Execute Step N (Implementer)  |
|                   |                    |
|                   v                    |
| Phase 4: Review Step N  (Reviewer)     |
|                   |                    |
|                   v                    |
| Phase 5: Reassess       (Supervisor)   |
+-------------------+--------------------+
                    |
         +----------+----------+
         v                     v
      [PASS]                 [FAIL]
         |                     |
   More steps?                 +-- Implementation flaw? --> Retry Implementer (max 2)
   +-----+-----+               +-- Architecture flaw?   --> Update Living Plan
  YES          NO              +-- Missing knowledge?   --> Trigger Researcher
   |           |
   v           v
[Step N+1]  [Phase 7: Finish & Wrap via along-wrap]
```

---

## Mandatory Execution Protocol (Step-by-Step)

### Phase 0: Analyze (Supervisor)
1. Read target `.along/ISSUES/<type>--<slug>.md` (or user prompt) and `.along/DECISIONS.md`.
2. Extract scope, constraints, and verifiable acceptance criteria.
3. Classify task size (`S`, `M`, or `L/XL`). Announce routing decision in chat.

### Phase 1: Research (Scout)
1. Launch read-only research subagent:
```json
{
  "Subagents": [
    {
      "TypeName": "research",
      "Role": "Codebase Scout",
      "Prompt": "Investigate files and dependencies for the task. Output only: 1) Relevant files and symbols, 2) Existing patterns, 3) Constraints/Risks, 4) Unknowns."
    }
  ]
}
```
2. Ingest findings. If critical unknowns remain, resolve before planning.

### Phase 2: Architecture & Living Plan (Architect)
1. Formulate a **Living Plan** with 2 to 5 ordered steps.
2. Each step must define:
   - Target files/symbols.
   - Expected behavior.
   - Verifiable acceptance criteria.

### Phase 3 to 5: Step Loop (Step N)
For each step in the Living Plan:
1. **Implement**: Invoke worker subagent (`self`) with step instructions and relevant context.
2. **Review**: Invoke reviewer subagent (`self` with `Role: "Code Reviewer"`) to run tests and audit diff.
3. **Reassess**: Supervisor inspects reviewer verdict:
   - If `PASS`: advance to Step N+1.
   - If `FAIL` (Implementation): send feedback to Implementer (maximum 2 retries before escalating to human).
   - If `FAIL` (Architecture/Unknowns): adjust Living Plan or spawn targeted Researcher.

### Phase 6: Autonomous Goal Completion (`/goal` Mode)
When running in `/goal` mode:
- The state machine runs continuously across all steps without prompting for intermediate approvals.
- Halts only when:
  1. All acceptance criteria pass and tests are green.
  2. Max retry limit is exceeded on a blocking flaw.

### Phase 7: Finish & Reconcile
1. Merge branch workspace changes (if isolated).
2. Execute `/along-wrap` checklist:
   - Run full test suite (`/along-test`).
   - Move issue to `.along/ISSUES/done/`.
   - Update `CONTEXT.md` and `ISSUES.md`.
   - Record session log in `.along/SESSIONS/`.
3. Present a single concise completion summary to the user.

