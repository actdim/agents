# Current Context Snapshot (2026-08-30)

## You Are Here
- **Repository**: `actdim/along` (Along Protocol & Skills Suite)
- **Current Version**: `v2.1.2`
- **Active Protocol**: `ALONG-PROTOCOL v2.1.2`

## Recent Architectural Milestones
- **LLM-Wiki Engine**: 100% Karpathy parity in `docs/` with `.archive/` isolation and front-matter discrimination.
- **Unified Knowledge Search**: `along_kb_search.py` indexes `docs/` + `.along/` living memory.
- **Dual Visual Graphs**: Auto-generated Mermaid map in `docs/INDEX.md` + Interactive Cytoscape.js in `/along-dash`.
- **Clean Command Namespace**: Canonical 17 `/along-*` skills with zero noisy aliases.
- **Dashboard Self-Bootstrapping**: Seamless `uv run` fallback for zero-dependency launches.

## Immediate Next Focus
- Autonomous goal loop (`along-goal`) & checklists engine.
