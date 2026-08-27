# Vision

_North star: scope, boundaries, non-goals, roadmap. Evolves slowly; slims as features ship._

## Scope
`Along` is a provider-agnostic, zero-friction agent memory and project management protocol and skills suite for AI coding assistants (Claude Code, OpenAI Codex, OpenCode, Google Antigravity). It equips repositories with:
1. **Persistent Project Memory**: Structured `.along/` repository memory across sessions and tools.
2. **Automated Entity Lifecycle**: Zero-friction tracking of issues, milestones, risks, spikes, and checklists in the background.
3. **Structured Knowledge Base (KB)**: Scalable, fact-grounded documentation (`.along/KB/`) with hybrid search capabilities.
4. **Visual Dashboard & Analytics**: Executive project dashboard (`/along-dash`) visualizing velocity, milestone progress, and repository health.

## Non-goals
- **No Proprietary Vendor Lock-in**: Never rely on tool-specific closed formats; everything is plain Markdown, YAML front-matter, and JSON.
- **No Context Bloat**: Never load full project history into active context; maintain compact entry points (`CONTEXT.md`, `ISSUES.md`).
- **No Manual Admin Overhead**: Humans should never be required to write metadata or manually maintain project tracking files; agents infer and maintain them automatically.

## Roadmap
- [x] **Phase 1 (Core Agent Memory)**: `init-agents`, `wrap-session`, `sync-context`, `sync-issues`, `sync-decisions`, and `install.ps1`/`install.sh`.
- [x] **Phase 2 (Knowledge Base & Code Graph)**: `.along/KB/`, `/along-init-kb`, `/along-search-kb`, `/along-sync-kb`, `/along-check-graph`, and `code-review-graph` MCP integration.
- [x] **Phase 3 (Entity Ecosystem & Metadata Migration)**: Protocol v1.5.0, Automated Entity Lifecycles (Milestones, Risks, Spikes, Checklists), and Auto-Migration tooling.
- [ ] **Phase 4 (Visual Dashboard & Repository Analytics)**: `/along-dash` skill, Generative UI widgets, Mermaid progress charts, and CLI executive summaries.
