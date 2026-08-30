---
protocol: along
slug: 02-domain-model
title: Domain Model & Entity Ecosystem
type: domain-model
created: 2026-08-30
updated: 2026-08-30
tags: [domain-model, entities, schemas, dag, metadata]
---

# Domain Model & Entity Ecosystem

Along models repository context as a structured, strongly-typed **Directed Acyclic Graph (DAG)** of markdown entities with YAML front-matter (protocol: along).

---

## 1. Entity Types & Front-Matter Schemas

### Issues (.along/ISSUES/<type>--<slug>.md)
Atomic units of work. Types: feat, bug, debt, task, docs.

\\yaml
---
protocol: along
slug: user-authentication-jwt
type: feat
status: open
priority: high
created: 2026-08-30
updated: 2026-08-30
completed: 2026-08-30
agent: antigravity
tags: [auth, jwt, security]
milestone: v2.2.0-auth
blocked_by: [feat--db-schema]
related: [risk--jwt-secret-rotation]
parent: feat--identity-platform
---
\
### Milestones (.along/MILESTONES/<slug>.md)
Release targets and sprint goals grouping multiple issues.

### Risks & Blockers (.along/RISKS/<slug>.md)
External dependencies, technical debt, and blocking constraints.

### Spikes & R&D Experiments (.along/SPIKES/<slug>.md)
Timeboxed research experiments, benchmarks, and prototype evaluations.

### Work Sessions (.along/SESSIONS/<YYYY>/<YYYY-MM-DD>--<slug>.md)
Per-session journals recording accomplishments, decisions, and code reviews.

### Architectural Decision Records (.along/DECISIONS.md)
Single-file append-only log of non-trivial technical and architectural decisions. Never rewritten; superseded ADRs are marked Superseded by #N.

---

## 2. Unidirectional DAG Relationships & Graph Invariance

Entity relationships use canonical string keys (<type>--<slug> or <slug>), never hardcoded file paths. This guarantees that links remain unbroken when completed issues move to ISSUES/done/:

- blocked_by: Forward dependency requirement.
- related: Associative link between issues, risks, or spikes.
- parent: Hierarchical container link to an epic or parent issue.
- **Inverse Resolution**: Relationships like blocks and children are computed dynamically by graph parsers and the dashboard engine.
