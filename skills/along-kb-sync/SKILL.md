---
name: along-kb-sync
description: Synchronize, compile, and reconcile the Knowledge Base in docs/ using LLM-Wiki pipeline. Ingests raw sources, moves originals to .archive/, validates Markdown links, and rebuilds docs/INDEX.md. Use when invoking /along-kb-sync (aliases: /kb-sync, /along-sync-kb, /along-init-kb).
---

# Along KB Sync (`/along-kb-sync`, `/kb-sync`) [v2.1.1]

Idempotent LLM-Wiki Knowledge Base synchronization and compilation engine for `docs/`.

## Capabilities
1. **Cold-Start Bootstrapping**: If `docs/` is missing or empty, generates `docs/INDEX.md`, `docs/01-architecture.md`, `docs/02-domain-model.md`, `docs/03-setup-and-workflow.md` grounded in codebase facts.
2. **Ingestion & Archival**: Compiles unmanaged notes or specs into structured Wiki articles and safely moves raw source files into `.archive/`.
3. **Link & Graph Linting**: Validates all relative links `[Title](./target.md)` and regenerates `docs/INDEX.md`.
4. **LLM-Wiki Engine Integration**: Compatible with `nvk/llm-wiki` MCP server (`wiki_ingest`, `wiki_lint`).

## Usage
```bash
python skills/along-kb-sync/along_kb_sync.py [REPO_ROOT] [--check]
```

- Command: `/along-kb-sync` (aliases: `/kb-sync`, `/along-sync-kb`, `/along-init-kb`)
