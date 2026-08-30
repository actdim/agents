---
protocol: along
date: 2026-08-30
slug: multi-agent-development-protocol-and-team-skill
agent: antigravity
branch: main
commit: pending
summary: Implemented Sequential Multi-Agent Development Protocol with Living Plan and bounded feedback loops, created along-team skill, integrated /goal autonomous mode, and added ADR #013
milestone: v2.1.0-along
issues_advanced: []
issues_completed: [feat--agentic-goals-and-mandatory-checklists]
decisions: ["#013"]
risks_logged: []
spikes_conducted: []
---

# Work Session: Sequential Multi-Agent Development Protocol & Along Team Skill

## Goal & Objectives
Design and implement a deterministic sequential multi-agent development protocol for complex software tasks, replace unstructured chat/swarm patterns with a verified state machine, introduce the canonical `/along-team` skill, integrate with autonomous `/goal` execution, and prevent token explosion via adaptive complexity routing.

## Completed Work

### 1. Sequential Multi-Agent Protocol Specification
- Formalized 5 core role primitives without role inflation:
  - **Supervisor**: Orchestration, task decomposition, acceptance criteria enforcement.
  - **Researcher (Scout)**: Read-only codebase and dependency discovery via `invoke_subagent` (`TypeName: "research"`, `enable_write_tools: false`).
  - **Architect**: Dynamic Living Plan formulation (2 to 5 verifiable steps).
  - **Implementer (Worker)**: Code changes in isolated workspace branch via `invoke_subagent` (`TypeName: "self"`).
  - **Reviewer (Tester + Critic + Judge)**: Unified test runner, diff audit, blast radius check, and ADR compliance.
- Established sequential state machine: `Phase 0: Analyze -> Phase 1: Research -> Phase 2: Architect (Living Plan) -> Phase 3-5: Step Loops (Implement -> Review -> Reassess) -> Phase 6: Goal Mode -> Phase 7: Wrap`.
- Implemented targeted feedback loops with a strict retry limit (maximum 2 retries per step) before escalating to human review.

### 2. Adaptive Complexity Routing (T-Shirt Sizing)
- **`S-Size`** (1-2 files, clear scope): Fast-Path single-agent execution without subagent spawning.
- **`M-Size`** (isolated module): Fast loop (Scout -> Worker -> Reviewer in one pass).
- **`L / XL-Size`** (cross-module impact, core refactoring): Full multi-agent state machine.

### 3. Canonical Skill Deployment (`skills/along-team/SKILL.md`)
- Created `skills/along-team/SKILL.md` with complete state machine, slash command triggers (`/along-team`, `/goal`), JSON subagent schemas, and step execution protocols.
- Updated `AGENTS.md` and registered `along-team` across all agent platforms via `install.ps1` (Antigravity, Claude Code, Codex, OpenCode).

### 4. Entity Reconciliation & Architectural Decisions
- Recorded ADR `#013` in `.along/DECISIONS.md`.
- Completed issue `feat--agentic-goals-and-mandatory-checklists.md` and moved to `.along/ISSUES/done/`.
- Updated `.along/ISSUES.md` and verified all 15 unit tests pass (`python -m unittest`).

## Code Review & Blast Radius Assessment
- **Clean Typography**: Checked with regex for zero non-ASCII characters, zero em-dashes, and standard ASCII quotes.
- **Cross-Platform Compatibility**: Validated on Windows PowerShell, Claude Code, Codex, and OpenCode command generators.
- **Blast Radius**: Zero breaking changes to existing skills; `along-team` seamlessly extends the execution suite.

