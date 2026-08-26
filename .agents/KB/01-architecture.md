# 01. Architecture Overview (`.agents/KB/01-architecture.md`) [v1.2.0]

## Overview
`actdim-agents` is a provider-agnostic agent-context protocol and skills suite supporting:
- **Claude Code** (`~/.claude/skills/`)
- **Codex** (`~/.codex/skills/`)
- **OpenCode** (`~/.config/opencode/commands/`)
- **Antigravity (AGY)** (`~/.gemini/config/skills/`)

## MCP Integration Architecture
- **Code Graph (`code-review-graph`)**: Automatically configured via `uvx code-review-graph` to analyze AST call graphs, compute impact radius, and inspect architecture flows.
- **Knowledge Base Search (`wiki-llm`)**: Configured for hybrid semantic documentation search across `.agents/`, `docs/`, `wiki/`, `README.md`.

