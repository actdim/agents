---
name: sync-kb
version: "1.3.2"
description: Reconcile and update the Knowledge Base hybrid vector index and cross-links across project documentation (.agents/, docs/, wiki/, *.md).
---

# Sync Knowledge Base (`/sync-kb`) [v1.3.2]

Use this skill to update, verify, and synchronize the hybrid search index across the project's **Knowledge Base (KB)** (`.agents/`, `docs/`, `wiki/`, `README.md`).

## Workflow

1. **Scan Knowledge Base Files**:
   - Inspect `.agents/` (`CONTEXT.md`, `ISSUES.md`, `DECISIONS.md`, `VISION.md`, `GLOSSARY.md`), `README.md`, `docs/`, `wiki/`.
   - If `wiki-llm` MCP tools are available, call `sync_wiki_tool` or `build_or_update_wiki_index_tool` to refresh the vector index.

2. **Reconcile Indexes & Cross-links**:
   - Update semantic cross-links and project context summaries.
   - Verify index freshness across active issues and architectural decisions.

3. **Report Status**:
   - Summarize the updated KB modules, total `.md` files indexed, and active focus areas.

