---
slug: integrate-wiki-llm-mcp
type: feat
status: done
priority: high
created: 2026-08-26
updated: 2026-08-26
---

# Integrate WikiLLM MCP Server for Hybrid MD Documentation Search

## Goal
Integrate the [`NexusLayerEU/wiki-llm`](https://github.com/NexusLayerEU/wiki-llm) MCP server into the `actdim-agents` suite to provide agents (Antigravity, Claude Code, Codex, OpenCode) with hybrid semantic search (TF-IDF + Vector Embeddings + Cross-links) across existing `.md` documentation (`.agents/`, `docs/`, `wiki/`, `README.md`) without requiring external LLM extraction overhead.

## Acceptance Criteria
- [x] Issue file and board updated in `.agents/`.
- [x] `wiki-llm` MCP registration added to `install.ps1` and `install.sh`.
- [x] Dedicated `skills/sync-wiki/SKILL.md` and `skills/search-wiki/SKILL.md` created to trigger hybrid index updates and search queries.
- [x] `AGENTS.md` and `init-agents` protocol updated with `wiki-llm` guidance.

