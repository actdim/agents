---
slug: add-sqlite-vector-indexing
type: feat
status: open
priority: high
created: 2026-08-13
updated: 2026-08-13
---

# Add SQLite Vector Indexing MCP Server for Fast Issue & Context Search

## Goal
Implement a local vector indexing system (e.g. SQLite + `sqlite-vec` or local embeddings) exposed as an **MCP (Model Context Protocol) Server**. The MCP server will index all markdown files inside `.agents/` (`ISSUES/`, `DECISIONS.md`, `SESSIONS/`, `GLOSSARY.md`, `VISION.md`), enabling AI agents to instantly perform semantic search across historical context, past session logs, and issue boards using native MCP tools.

## Key Requirements
1. **MCP Protocol Server**: Expose vector indexing and semantic search as standard MCP tools (e.g., `index_agents_context`, `search_agents_context`).
2. **Local & Lightweight Storage**: Store index in a `.gitignored` SQLite database (e.g., `.agents/.index.db`).
3. **Discrete Document Embeddings**:
   - Index each issue file `.agents/ISSUES/<type>--<slug>.md` as a standalone document chunk using its YAML front-matter (`type`, `priority`, `status`) and body text.
   - Index decisions by ADR entry `#NNN`.
   - Index session logs by file.
4. **Automatic/On-demand Indexing**: MCP tool automatically refreshes vector embeddings whenever `.agents/` files are updated or queried.
5. **Semantic Search Querying**: Allow agents to query issues and project memory by natural language (e.g. `search_agents_context(query="Find all bugs related to authentication")`).

## Acceptance Criteria
- [ ] MCP Server (`sqlite-vector-agents`) implemented and configured for Claude, Codex, OpenCode, and Antigravity.
- [ ] MCP tools for indexing (`index_agents_context`) and semantic querying (`search_agents_context`) tested.
- [ ] Integration with `init-agents` to scaffold `mcp_config.json` entry.
