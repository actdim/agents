---
protocol: along
slug: 02-domain-model
title: Domain Model and Entity Ecosystem
type: domain-model
created: 2026-08-27
updated: 2026-08-28
tags: [domain-model, entities, issues, milestones, risks, spikes, adr, sessions, dag]
---

# Along Domain Model & Entity Ecosystem

Along models repository memory and project execution as a set of structured, typed entities with YAML frontmatter.

---

## 1. Entity Types

| Entity | Directory | Description | Mandatory Frontmatter Fields |
| :--- | :--- | :--- | :--- |
| **Issue** | `.along/ISSUES/<type>--<slug>.md` | Unit of work (`feat`, `bug`, `debt`, `task`, `docs`). | `protocol: along`, `slug`, `type`, `status`, `priority`, `created`, `updated` |
| **Milestone** | `.along/MILESTONES/<slug>.md` | Release target, stage, or sprint container. | `protocol: along`, `slug`, `title`, `status`, `due_date`, `created`, `target_issues: []` |
| **Risk / Blocker**| `.along/RISKS/<slug>.md` | External blockers, API limits, security flags. | `protocol: along`, `slug`, `title`, `severity`, `status`, `owner`, `mitigation` |
| **Spike** | `.along/SPIKES/<slug>.md` | R&D experiments, benchmarks, evaluations. | `protocol: along`, `slug`, `title`, `status`, `hypothesis`, `outcome`, `resulting_adr` |
| **Session** | `.along/SESSIONS/<year>/<date>--<slug>.md` | Log of actions taken in an agent session. | `protocol: along`, `date`, `slug`, `agent`, `branch`, `commit`, `summary` |
| **Decision (ADR)** | `.along/DECISIONS.md` | Append-only architectural decisions log. | `# NNN: <Title>`, `Date: YYYY-MM-DD`, `Status: Accepted | Superseded by #M` |
| **KB Article** | `.along/KB/<slug>.md` | Long-term technical knowledge base docs. | `protocol: along`, `slug`, `title`, `type`, `created`, `updated`, `tags: []` |

---

## 2. Relationships & Dependency Graph (DAG)

Entities support explicit unidirectional relationships declared in YAML frontmatter:

```yaml
blocked_by: [feat--core-parser, risk--api-rate-limit]
related: [feat--dashboard-ui, spike--wasm-eval]
parent: milestone--v200-release
```

### Graph Invariance Rules:
- Entities are referenced by **canonical key** (`<type>--<slug>` or `<slug>`), never by relative filesystem path.
- When an issue is completed, it moves to `.along/ISSUES/done/<type>--<slug>.md` without breaking graph links.
- The Along Dashboard (`scripts/along_dash.py`) dynamically evaluates the Directed Acyclic Graph (DAG), verifying acyclicity and rendering interactive Cytoscape graphs.

---

## 3. Automated Lifecycle & Reconciliation

1. **Active Work**: Stored in `.along/ISSUES/` and summarized in `.along/ISSUES.md`.
2. **Completion**:
   - `status: done` and `completed: YYYY-MM-DD` set in frontmatter.
   - File moved to `.along/ISSUES/done/`.
   - Linked milestones update their `progress_pct`.
3. **Session Closure**:
   - Written to `.along/SESSIONS/<YYYY>/<YYYY-MM-DD>--<slug>.md`.
   - Index appended in `.along/HISTORY.md`.
   - Snapshot refreshed in `.along/CONTEXT.md`.
