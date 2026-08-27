---
name: search-kb
version: "1.5.4"
description: Query project Knowledge Base (.agents/, docs/, wiki/, *.md) using hybrid semantic search and cross-linking.
---

# Search Knowledge Base (`/search-kb`) [v1.5.4]

Use this skill to perform hybrid search across the project's **Knowledge Base (KB)** (`.agents/`, `docs/`, `wiki/`, `README.md`).

## Usage
- `/search-kb <query>`: Performs hybrid semantic search across the project Knowledge Base.

## Workflow

1. **Perform KB Search**:
   - If `wiki-llm` MCP tools (`search_wiki_tool`, `get_wiki_article_tool`) are available, call `search_wiki_tool` with `query: "<query>"` to search across project documentation.
   - Otherwise, perform native hybrid search across project Knowledge Base files (`.agents/`, `docs/`, `wiki/`, `README.md`) using targeted semantic and keyword lookup.

2. **Format & Present Results**:
   - Format header cleanly as `# Project Knowledge Base Search Results (Knowledge Base Search v1.3.1)`.
   - Output relevant matching Markdown sections, ADR decisions, or issue documents with clickable links.
   - Show cross-links (`[[links]]`) and relevant context snippets.

