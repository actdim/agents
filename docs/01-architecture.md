---
protocol: along
slug: 01-architecture
title: System Architecture & Flow
type: architecture
created: 2026-08-30
updated: 2026-08-30
tags: [architecture, boundaries, providers, mcp, dashboard]
---

# System Architecture & Flow

Along (actdim-along) is a provider-agnostic agent-context, project memory, and documentation protocol designed to give software repositories a persistent, durable, and human-readable context layer.

\\mermaid
flowchart TD
    subgraph HostAgents[Supported Host AI Agents]
        CC[Claude Code (~/.claude)]
        CX[Codex (~/.codex)]
        OC[OpenCode (~/.config/opencode)]
        AG[Antigravity (~/.gemini/config)]
    end

    subgraph RepoContext[Repository Memory Layer (.along/ & docs/)]
        AGENTS[AGENTS.md (Root Protocol & Conventions)]
        ALONG_DIR[.along/ (Persistent Project State)]
        DOCS[docs/ (Compiled LLM-Wiki Knowledge Base)]
        ARCHIVE[.archive/ (Archived Raw Sources)]
    end

    subgraph SkillsAndMCP[Skills & MCP Tooling]
        SKILLS[skills/ (17 Singular Domain-First Skills)]
        CRG_MCP[code-review-graph MCP]
        WIKI_MCP[llm-wiki MCP & along-kb-search]
        DASH[FastAPI Dashboard + Dynstruct UI (/along-dash)]
    end

    CC --> AGENTS
    CX --> AGENTS
    OC --> AGENTS
    AG --> AGENTS

    AGENTS --> ALONG_DIR
    AGENTS --> DOCS
    ALONG_DIR --> SKILLS
    DOCS --> WIKI_MCP
    ALONG_DIR --> DASH
\
---

## 1. Provider Compatibility & Discovery

Along operates without vendor lock-in by using standardized agent discovery paths:

- **Claude Code**: Reads CLAUDE.md, which imports root AGENTS.md. Verbatim skill folders installed in ~/.claude/skills/.
- **Codex**: Reads AGENTS.md natively. Skills installed in ~/.codex/skills/.
- **OpenCode**: Reads AGENTS.md natively (and CLAUDE.md). Flat command files installed in ~/.config/opencode/commands/.
- **Antigravity**: Reads AGENTS.md (or GEMINI.md) natively. Skills installed in ~/.gemini/config/skills/.

---

## 2. Nearest Context Boundary & Subproject Localization

Along enforces strict context localization across monorepos, Git submodules, and symlinked packages:

- **Nearest .along/ Boundary**: Any folder may carry its own AGENTS.md + .along/. Agents MUST evaluate and write entities (ISSUES, SESSIONS, CONTEXT.md, DECISIONS.md, HISTORY.md) to the **NEAREST** .along/ corresponding to the modified files.
- **Submodule Isolation**: Submodule bug fixes and features are recorded directly in that submodule's .along/, preventing workspace root pollution.
- **Parent Orchestration**: Root workspace .along/ is reserved for whole-solution orchestration, top-level integration tasks, and cross-package architectural ADRs.

---

## 3. Dynamic Executive Dashboard (dashboard/ & packages/dashboard-ui/)

Along includes an integrated, multi-mode executive dashboard:

- **Backend (dashboard/)**:
  - Modular FastAPI application serving REST endpoints and live Server-Sent Events (SSE) stream on http://127.0.0.1:8765.
  - Automatic OpenAPI Swagger documentation available at /docs.
  - Scans .along/ entities and docs/ Knowledge Base articles dynamically.
- **Frontend (packages/dashboard-ui/)**:
  - Built strictly on @actdim/dynstruct (structure-first component model with MobX observable state) and @actdim/msgmesh message bus.
  - Interactive Directed Acyclic Graph (DAG) rendered with Cytoscape.
  - Real-time file system change detection and automatic UI refresh.

---

## 4. MCP Server Integrations

- **code-review-graph**: Automatic code analysis and call graph tracing (build_or_update_graph_tool, get_impact_radius_tool, get_affected_flows_tool).
- **nvk/llm-wiki & along-kb-search**: Fast structured retrieval across docs/ to minimize agent context window and token usage.
