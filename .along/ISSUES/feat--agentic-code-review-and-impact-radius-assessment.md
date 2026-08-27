---
protocol: along
slug: agentic-code-review-and-impact-radius-assessment
type: feat
status: open
priority: high
created: 2026-08-27
updated: 2026-08-27
agent: antigravity
tags: [code-review, impact-analysis, quality-gate, mcp]
milestone: v2.0.0-along-transition
blocked_by: []
related: [feat--automated-ui-screenshots-and-visual-verification, feat--agentic-goals-and-mandatory-checklists]
---

# Agentic Code Review & Blast Radius Impact Assessment Protocol

## Goal
Establish a mandatory, automated **Agentic Code Review & Impact Radius Assessment** protocol within the system, requiring agents to critically analyze their own code changes before completing non-trivial tasks, assessing blast radius across dependent modules, architecture compliance, and safety.

## Problem Statement
Agents often introduce localized changes that inadvertently break distant components, introduce silent edge cases, violate architectural conventions, or leave unhandled nulls/exceptions. Without a formalized post-implementation review gate, bugs and architectural drift accumulate unnoticed until runtime.

## Proposed Code Review Workflow

### 1. Mandatory Post-Change Review Gate
Integrate a mandatory review step into the protocol and session wrap-up checklist:
- Before moving any issue to `status: done` or closing a stage, the agent MUST run a structured self-review.

### 2. Blast Radius & Dependency Impact Analysis
- Utilize code graph intelligence (e.g. `code-review-graph` MCP tools: `get_impact_radius_tool`, `get_affected_flows_tool`, `find_large_functions_tool`):
  - Identify all symbols, functions, and files directly or transitively affected by the diff.
  - Verify that downstream callers and interface contracts remain intact.
  - Flag potential breaking changes or schema mismatches across service boundaries.

### 3. Critical Code Review Criteria Checklist
The agent must evaluate:
- **Correctness & Edge Cases**: Are edge cases, null states, error handling, and concurrency risks covered?
- **Architectural & ADR Conformance**: Does the change contradict active ADRs in `.along/DECISIONS.md`?
- **Performance & Context Hygiene**: Does the change introduce excessive token overhead, unindexed queries, or memory bloat?
- **Typographic & Protocol Compliance**: Clean ASCII typography, windows-safe paths, valid front-matter metadata.

### 4. Review Outcome Documentation
- Append a concise `## Code Review & Blast Radius Assessment` section in the session log (`.along/SESSIONS/`) and issue verification checklist summarizing:
  - Total files touched and affected blast radius.
  - Identified risks and mitigations applied.
  - Confirmation of automated tests and graph checks passed.

## Acceptance Criteria
- [ ] Code Review & Blast Radius guidelines added to `AGENTS.md` protocol.
- [ ] Session wrap-up checklist updated with mandatory review gate.
- [ ] Integration with `code-review-graph` impact tools documented for all AI assistants.
