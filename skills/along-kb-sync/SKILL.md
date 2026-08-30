---
name: along-kb-sync
description: Synchronize, compile, and reconcile the Knowledge Base in docs/ using LLM-Wiki pipeline. Ingests raw sources, moves originals to .archive/, validates Markdown links, and rebuilds docs/INDEX.md. Use when invoking /along-kb-sync (aliases: /kb-sync, /along-sync-kb, /along-init-kb).
---

# Along KB Sync (`/along-kb-sync`, `/kb-sync`) [v2.1.1]

Idempotent LLM-Wiki Knowledge Base synchronization and compilation engine for `docs/`.

## Capabilities
1. **Cold-Start Bootstrapping**: If `docs/` is missing or empty, generates `docs/INDEX.md`, `docs/topic--architecture.md`, `docs/topic--domain-model.md`, `docs/topic--setup-and-workflow.md` grounded in codebase facts.
2. **Ingestion & Archival**: Compiles unmanaged notes or specs into structured Wiki articles and safely moves raw source files into `.archive/`.
3. **Link & Graph Linting**: Validates all relative links `[Title](./target.md)` and regenerates `docs/INDEX.md`.
4. **LLM-Wiki Engine Integration**: Compatible with `nvk/llm-wiki` MCP server (`wiki_ingest`, `wiki_lint`).

## Execution Strategy: Adaptive Ingestion & Parallel Research

When executing `/along-kb-sync`:
- **Direct Incremental Ingestion**: For 1-3 raw source files or minor updates, the agent directly reads facts, creates/updates `docs/topic--<slug>.md`, and runs the compiler.
- **Parallel Research Ingestion (Large-Scale / Multi-Package)**:
  - When processing extensive documentation dumps, large monorepos, or multiple subprojects:
    1. **Decompose Topics**: Split the knowledge extraction into 2-4 discrete domain vectors (e.g. `architecture`, `data-models`, `api-integrations`, `workflows`).
    2. **Spawn Parallel Subagents**: Concurrently invoke research subagents to synthesize independent `docs/topic--<slug>.md` articles in parallel with standard YAML front-matter.
    3. **Reconcile & Link**: Run `python skills/along-kb-sync/along_kb_sync.py` to validate all relative links `[Title](./target.md)`, move processed raw sources into `.archive/`, and rebuild `docs/INDEX.md`.

## Usage
```bash
python skills/along-kb-sync/along_kb_sync.py [REPO_ROOT] [--check]
```

- Command: `/along-kb-sync` (aliases: `/kb-sync`, `/along-sync-kb`, `/along-init-kb`)
