---
protocol: along
slug: llm-wiki-docs-architecture-and-skill-refactor
type: feat
status: done
completed: 2026-08-30
priority: critical
created: 2026-08-30
updated: 2026-08-30
agent: antigravity
tags: [kb, wiki, mcp, skills, protocol, migration]
milestone: v2.1.0-wiki-llm
blocked_by: []
related: []
---

# Full LLM-Wiki Integration, docs/ KB Architecture, .archive/ Archival & Singular Domain-First Skills

## Goal
Integrate the nvk/llm-wiki engine directly as the foundational MCP server, CLI engine, and agent protocol for documentation compilation and search. Migrate active Knowledge Base articles to top-level docs/, archive processed source documents into .archive/, mandate agent querying via along-kb-search / wiki_query, and standardize all skill names to the Singular Domain-First format (along-<entity>-<action>).
