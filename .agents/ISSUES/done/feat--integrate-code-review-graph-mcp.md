---
slug: integrate-code-review-graph-mcp
type: feat
status: done
priority: high
created: 2026-08-13
updated: 2026-08-15
---

# Integrate `code-review-graph` MCP Server via `uv`

## Goal
Integrate the [`code-review-graph`](https://github.com/tirth8205/code-review-graph) MCP server into the `actdim-agents` skills suite (`init-agents`, `wrap-session`, protocol guidance).

The goal is for agents to recommend, detect, and automatically set up `code-review-graph` (using Python's `uv` package runner, e.g. `uvx code-review-graph`) so repositories gain automatic code graph analysis, impact radius checking, and architectural flow tracing.

## Proposed Integration Details
1. **`uv` Package Manager Setup**:
   - Leverage `uv` / `uvx` for fast, zero-dependency installation of `code-review-graph`.
2. **Skill Guidance Integration**:
   - Update `init-agents` and `AGENTS.md` protocol to recommend initializing `code-review-graph` MCP server during project setup.
   - Instruct agents to use `code-review-graph` tools (e.g. `build_or_update_graph_tool`, `get_impact_radius_tool`, `get_architecture_overview_tool`) during research and code review phases.
3. **MCP Configuration Scaffolding**:
   - Provide standard `mcp_config.json` snippet for `code-review-graph` powered by `uv`:
     ```json
     {
       "mcpServers": {
         "code-review-graph": {
           "command": "uvx",
           "args": ["code-review-graph"]
         }
       }
     }
     ```

## Acceptance Criteria
- [x] Protocol updated to include `code-review-graph` recommendation for code analysis.
- [x] `init-agents` updated to offer `code-review-graph` MCP configuration via `uv`.
- [x] Guidelines added for agents on when to run graph building and impact radius queries.
