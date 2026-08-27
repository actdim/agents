---
protocol: along
slug: feat--graph-ignore-and-interactive-skills-refinement
type: feat
status: done
priority: medium
created: 2026-08-26
updated: 2026-08-26
completed: 2026-08-26
agent: git-reconstructed
tags: [git-sync, graph, mcp, protocol]
milestone: v1.3.0-knowledge-base-and-graph
blocked_by: []
related: []
---

# Graph Ignore Scaffolding and Interactive Skills Refinement

Reconstructed from Git commits `9195772`, `5a92bc4`, `702c1b5`, `7aa7947`, and `f0df14f` by `pavel.borodaev`.

## Changes Made
- Added automatic `.code-review-graph-ignore` scaffolding and exclusion rules to prevent `node_modules` ballooning.
- Added strict anti-hallucination and fact-grounding rules to protocol and `init-kb`.
- Introduced interactive re-initialization prompts for Code Graph and Knowledge Base skills.
- Explicitly referenced `wiki-llm` MCP tools (`search_wiki_tool`, `sync_wiki_tool`) in `search-kb` and `sync-kb`.
