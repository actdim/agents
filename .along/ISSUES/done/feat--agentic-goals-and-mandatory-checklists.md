---
protocol: along
slug: agentic-goals-and-mandatory-checklists
type: feat
status: done
priority: high
created: 2026-08-13
updated: 2026-08-30
completed: 2026-08-30
agent: antigravity
tags: [multi-agent, goal, team, protocol, checklists]
milestone: v2.1.0-along
blocked_by: []
related: []
---

# Introduce Agentic Goals (Autonomous Loop), Multi-Agent Development Protocol & Mandatory Checklists

## Goal
Enhance the agent protocol and execution environment with sequential multi-agent execution and autonomous goal capabilities:
1. **Multi-Agent Protocol & Team Skill (`/along-team`)**: Sequential state machine (Supervisor -> Research -> Architect -> Living Plan -> Step Loops [Implement -> Review/Test -> Reassess]) with bounded feedback retries and adaptive routing (S/M/L).
2. **Agentic Goals (`/goal` Autonomous Loop)**: Continuous, non-stop execution loop where the agent team works autonomously towards a defined goal until all completion and verification criteria are met.
3. **Mandatory Verification Checklists**: Enforceable, step-by-step checklists for key lifecycle events (e.g. end-of-session, pre-commit, post-implementation) that agents MUST execute item-by-item without skipping.

## Key Features

### 1. Sequential Multi-Agent Development Protocol (`skills/along-team/SKILL.md`)
- Define 5 core role primitives: Supervisor, Researcher (Scout), Architect (Living Plan), Implementer (Worker), Reviewer (Tester + Critic + Judge).
- Sequential by default with targeted feedback loops (maximum 2 retries per step before human escalation).
- Adaptive complexity routing (S-Size Fast-Path, M-Size Fast Loop, L/XL Full Protocol).

### 2. Goal-Driven Autonomous Execution Loop (`/goal`)
- Support autonomous self-correction: agent team keeps iterating until concrete tests/verifications pass.
- Full portability across Claude Code, Codex, OpenCode, and Antigravity.

### 3. Mandatory Checklists
- Define standard checklists for workflow stages:
  - **End-of-Session Checklist**: Verify build, clean git status, update `.along/` state.
  - **Feature Delivery Checklist**: Test coverage, documentation updates, issue board reconciliation.
  - **Security & Integrity Checklist**: No secrets committed, windows-safe filenames, valid links.

## Acceptance Criteria
- [x] Protocol updated with Goal-driven loop conventions and `/goal` command recommendations.
- [x] Canonical `/along-team` skill created and deployed globally via `install.ps1`.
- [x] Mandatory Checklists defined in protocol and skills (`along-wrap`, `along-team`).
- [x] Agent instructions and ADR #013 updated to enforce step-by-step verification.

