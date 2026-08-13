---
slug: add-sqlite-vector-indexing
type: feat
status: open
priority: high
created: 2026-08-13
updated: 2026-08-13
---

# Add SQLite Vector Indexing for Fast Issue & Context Search

## Goal
Implement a local vector indexing system (e.g. SQLite + `sqlite-vec` or local embeddings) that indexes all markdown files inside `.agents/` (`ISSUES/`, `DECISIONS.md`, `SESSIONS/`, `GLOSSARY.md`, `VISION.md`). This enables instant semantic search across historical context, past session logs, and issue boards.

## Key Requirements
1. **Local & Lightweight**: Store index in a `.gitignored` SQLite database (e.g., `.agents/.index.db`).
2. **Discrete Document Embeddings**:
   - Index each issue file `.agents/ISSUES/<type>--<slug>.md` as a standalone document chunk using its YAML front-matter (`type`, `priority`, `status`) and body text.
   - Index decisions by ADR entry `#NNN`.
   - Index session logs by file.
3. **Automatic/On-demand Indexing**: Provide an automated trigger (or `/sync-index` skill / MCP tool) to refresh vector embeddings whenever `.agents/` files are updated.
4. **Semantic Search Querying**: Allow agents and developers to query issues and project memory by natural language (e.g. "Find all bugs related to authentication").

## Acceptance Criteria
- [ ] SQLite vector database indexing script / tool created.
- [ ] Automated or skill-driven index sync implemented (`/sync-index`).
- [ ] Semantic search CLI / tool returning ranked relevant markdown links.
