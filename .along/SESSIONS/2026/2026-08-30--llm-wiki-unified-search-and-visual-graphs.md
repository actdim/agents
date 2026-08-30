---
protocol: along
date: 2026-08-30
slug: llm-wiki-unified-search-and-visual-graphs
agent: antigravity
branch: main
commit: d1cf488
summary: Upgraded along to v2.1.2 with Karpathy LLM-Wiki parity, unified multi-scope retrieval engine across docs/ and .along/, dual Mermaid/Cytoscape visual graphs, script naming unification, alias purge, and transparent uv auto-bootstrap.
milestone: v1.5.0-dashboard-and-analytics
issues_advanced: []
issues_completed: [feat--dynamic-dashboard-and-kb-engine]
decisions: []
risks_logged: []
spikes_conducted: []
---

# Session Log: LLM-Wiki Parity, Unified Multi-Scope Retrieval & Visual Graphs (v2.1.2)

## Summary of Changes
1. **Karpathy LLM-Wiki Alignment & Strict Ingestion Pipeline**:
   - Verified 100% architectural parity against Andrej Karpathy's official `llm-wiki.md` specification.
   - Refactored `skills/along-kb-sync/along_kb_sync.py` and `scripts/migrate_protocol.py` (Step 7) to enforce deterministic source scanning across `docs/`, `wiki/`, `kb/`, and `.along/KB/`.
   - Injected `protocol: along` metadata discrimination into Wiki articles and scaffolded `.archive/` for raw source isolation.
2. **README.md Executive Streamlining & Universal Rendering**:
   - Refactored `README.md` into an executive overview with standard navigation catalog into `docs/topic--*.md`.
   - Enforced relative portable Markdown links (`./topic--*.md`) and clean ASCII typography.
3. **Unified Multi-Scope Retrieval Engine (`along-kb-search`)**:
   - Upgraded `along_kb_search.py` to index both curated Wiki articles (`docs/`) and living repository memory (`.along/ISSUES/`, `DECISIONS.md`, `MILESTONES/`, `RISKS/`, `SPIKES/`, `SESSIONS/`).
   - Implemented weighted scoring with status-based boosts and context snippet extraction (<100 tokens, <15ms).
4. **Dual Visual Graph Architecture**:
   - Auto-compiled static Mermaid knowledge map in `docs/INDEX.md` at each `/along-kb-sync`.
   - Integrated Knowledge Base article nodes and cross-references into Cytoscape.js interactive graph in Along Dashboard.
   - Added live Mermaid diagram rendering in Dashboard drawer view.
5. **Script Renaming & Alias Purge**:
   - Renamed `along_bump_version.py` -> `along_version_bump.py` (1-to-1 parity with `along-version-bump`).
   - Purged all unnamespaced noisy aliases from `SKILL.md`, `install.ps1`, and `install.sh`.
6. **Transparent uv Self-Bootstrapping**:
   - Added zero-traceback self-bootstrapping to `scripts/along_dash.py` and `skills/along-dash/along_dash.py` when FastAPI/Rich are not installed in global python.
7. **Release v2.1.2**:
   - Multi-stack version bump to `v2.1.2` across 23 manifests and skill files.
