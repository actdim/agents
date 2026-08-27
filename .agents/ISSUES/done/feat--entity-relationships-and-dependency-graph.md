---
slug: entity-relationships-and-dependency-graph
type: feat
status: done
priority: high
created: 2026-08-27
updated: 2026-08-27
completed: 2026-08-27
agent: antigravity
tags: [protocol, graph, metadata]
milestone: v1.5.0-dashboard-and-analytics
blocked_by: []
related: [feat--project-dashboard-and-analytics-skill]
---

# Feature: Entity Relationships & Dependency Graph Support

## Goal
Introduce standardized metadata fields (`blocked_by`, `related`, `parent`) across entity front-matter in `ACTDIM-AGENTS-PROTOCOL` to enable dependency modeling, DAG cycle detection, and automated relationship graphs for project dashboards and agent reasoning.

## Requirements
- Update `protocol.md` and `AGENTS.md` to document the relationship fields with clear semantics and canonical slug referencing rules.
- Update `skills/sync-issues/SKILL.md` and `skills/init-agents/SKILL.md` to guide agents in managing relationship front-matter without dual-sync drift.
- Enhance `migrate_protocol.py` with validation and extraction helpers (detecting dangling references and cyclic dependencies in `blocked_by`).
- Ensure full ASCII compliance (no typographic Unicode).

