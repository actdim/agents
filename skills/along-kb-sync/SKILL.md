---
name: along-kb-sync
description: Synchronize, compile, and reconcile the Knowledge Base in docs/ using LLM-Wiki pipeline. Ingests README facts and raw sources, moves originals to .archive/, validates Markdown links, and rebuilds docs/INDEX.md. Use when invoking /along-kb-sync.
---

# Along KB Sync  [v2.1.5]

Idempotent LLM-Wiki Knowledge Base synchronization, compilation, and link-linting engine for `docs/`.

## Capabilities
1. **Cold-Start Bootstrapping**: If `docs/` is missing or empty, generates `docs/INDEX.md`, `docs/topic--architecture.md`, `docs/topic--domain-model.md`, `docs/topic--setup-and-workflow.md` grounded in codebase and `README.md` facts.
2. **README Ingestion & Streamlining**: Extracts deep technical specifications from monolithic `README.md` files into modular `docs/topic--<slug>.md` articles, leaving `README.md` as an executive overview with direct navigation links.
3. **Ingestion & Archival**: Compiles unmanaged notes, specs, or drafts (`wiki/`, `kb/`, `docs/`) into structured Wiki articles and safely moves raw source files into `.archive/`.
4. **Link & Graph Linting**: Validates all relative links `[Title](./topic--<slug>.md)` and regenerates `docs/INDEX.md`.
5. **LLM-Wiki Paradigm**: Native pure-Python implementation of the Andrej Karpathy LLM-Wiki methodology with zero external dependencies.

## Universal Rendering & Package Registry Portability

All Markdown generated or maintained by `along-kb-sync` MUST strictly adhere to universal rendering standards:
- **Relative Markdown Links**: Use standard relative paths (`./docs/topic--<name>.md` from root, `./topic--<name>.md` within `docs/`). Never use absolute URLs, local filesystem schemes (`file:///`), or OS-specific backslashes.
- **Cross-Platform Renderers**: Guarantees 100% clean rendering across **GitHub**, **GitLab**, **GitHub Pages** (Jekyll, Astro, Docusaurus, MkDocs), **npm**, **NuGet**, **PyPI**, and **crates.io**.
- **Clean ASCII Typography**: Zero non-ASCII typography (no em-dashes U+2014, curly quotes, or ellipsis glyphs).
- **Explicit Code Fences**: Every code block must declare an explicit language identifier (`bash`, `yaml`, `typescript`, `python`, `powershell`).

## Execution Strategy: Adaptive Ingestion & Parallel Research

When executing `/along-kb-sync`:
- **Direct Incremental Ingestion**: For 1-3 raw source files or minor updates, the agent directly reads facts, creates/updates `docs/topic--<slug>.md`, and runs the compiler.
- **Parallel Research Ingestion (Large-Scale / Multi-Package)**:
  - When processing extensive documentation dumps, large monorepos, or multiple subprojects:
    1. **Decompose Topics**: Split the knowledge extraction into 2-4 discrete domain vectors (e.g. `architecture`, `data-models`, `api-integrations`, `workflows`).
    2. **Spawn Parallel Subagents**: Concurrently invoke research subagents to synthesize independent `docs/topic--<slug>.md` articles in parallel with standard YAML front-matter.
    3. **Reconcile & Link**: Run `python scripts/along_kb_sync.py` to validate all relative links `[Title](./target.md)`, move processed raw sources into `.archive/`, and rebuild `docs/INDEX.md`.

## Usage
```bash
python scripts/along_kb_sync.py [REPO_ROOT] [--check]
```
*(Or `python scripts/along_exec.py kb-sync` / `/along-kb-sync`)*

