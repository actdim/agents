---
slug: agentic-goals-and-mandatory-checklists
type: feat
status: open
priority: high
created: 2026-08-13
updated: 2026-08-13
---

# Introduce Agentic Goals (Autonomous Loop) & Mandatory Checklists

## Goal
Enhance `actdim-agents` with two core execution patterns:
1. **Agentic Goals (`/goal` Autonomous Loop)**: Continuous, non-stop execution loop where the agent works autonomously towards a defined goal until all completion and verification criteria are met.
2. **Mandatory Verification Checklists**: Enforceable, step-by-step checklists for key lifecycle events (e.g. end-of-session, pre-commit, post-implementation) that agents MUST execute item-by-item without skipping.

## Key Features

### 1. Goal-Driven Autonomous Execution Loop (`/goal`)
- Define explicit **Goal** structures in issue files and session plans (`Goal`, `Verification Criteria`, `Autonomous Iteration Loop`).
- Support autonomous self-correction: agent keeps iterating until concrete tests/verifications pass.
- Provide guidelines and slash-command patterns (`/goal`) for non-stop execution.

### 2. Mandatory Checklists (`Checklist` Pattern)
- Define standard checklists for workflow stages:
  - **End-of-Session Checklist**: Verify build, clean git status, update `.agents/` state.
  - **Feature Delivery Checklist**: Test coverage, documentation updates, issue board reconciliation.
  - **Security & Integrity Checklist**: No secrets committed, windows-safe filenames, valid links.
- Enforce mandatory step-by-step checklist execution where agents explicitly mark each item as verified before completing a task.

## Acceptance Criteria
- [ ] Protocol updated with Goal-driven loop conventions and `/goal` command recommendations.
- [ ] Mandatory Checklists defined in protocol and skills (`wrap-session`, `sync-issues`, etc.).
- [ ] Agent instructions updated to enforce step-by-step checklist verification.
