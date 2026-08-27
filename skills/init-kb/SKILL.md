---
name: init-kb
version: "1.5.6"
description: Bootstrap or refresh the structured Knowledge Base (.agents/KB/ or docs/) from README.md, AGENTS.md, docs/, and codebase analysis.
---

# Init Knowledge Base (`/init-kb`) [v1.5.6]

Use this skill to bootstrap or refresh a structured, interlinked **Knowledge Base (KB)** in `.agents/KB/` for any repository.

## Architectural Structure
- **`.agents/KB/`**: Primary agent Knowledge Base directory (`INDEX.md`, `01-architecture.md`, `02-domain-model.md`, `03-setup-and-workflow.md`).
- **Human Documentation (`docs/`, `README.md`)**: Scanned as authoritative inputs during `/init-kb` and `/sync-kb` to incorporate human-written specs and documentation into the Knowledge Base.
- **`AGENTS.md`**: Executive summary (protocol block + quick build commands + links to `.agents/KB/`).
- **`CLAUDE.md`**: Minimal 1-line import (`@AGENTS.md`).

## Strict Anti-Hallucination & Fact-Grounding Rules

1. **Mandatory Deep Source Verification**:
   - Before writing any `.agents/KB/` article, you MUST inspect `README.md` (using `view_file`), `package.json`, and core source files (e.g., `src/contracts.ts`, `src/index.ts`).
   - NEVER generate articles based on guesses or assumptions derived solely from package names.

2. **Zero Generic Boilerplate**:
   - Do NOT invent placeholder component names, architectural layers, or domain concepts (e.g., "Schema Parser", "Validation Engine", "Data Manager") if they do not explicitly exist in `README.md` or the source code.
   - If a project lacks certain components, document ONLY what is actually present.

3. **Verifiable Extraction Mapping**:
   - **`01-architecture.md`**: Extract architecture layers, tech stack, and subsystem boundaries directly from `README.md` (`Overview`, `Features`, `Architecture`, `Modules` sections) or actual `src/` directory trees.
   - **`02-domain-model.md`**: Extract exported types, interfaces, classes, and core concepts directly from `README.md` (`Core Concepts`, `API Reference`, `Types`) or source type definitions.
   - **`03-setup-and-workflow.md`**: Extract install, build, run, and test commands verbatim from `package.json` scripts or `README.md` (`Quick Start`, `Development`).

4. **Self-Audit Check**:
   - Prior to saving any file, verify: *Is every symbol, term, and command in this document directly backed by empirical evidence in the repo?*

## Workflow & Interactive Re-initialization

1. **Re-initialization Check**:
   - When running on a project that already has `.agents/KB/`, ask the user if they want to:
     * Full refresh: Re-extract architecture & domain model from latest `README.md`, `docs/`, `package.json`, and codebase.
     * Incremental sync: Run `/sync-kb` to update indexes and cross-links without overwriting custom edits.

2. **Source Content Analysis**:
   - Read human documentation in `docs/`, `README.md`.
   - Read agent context files: `AGENTS.md`, `.agents/CONTEXT.md`, `.agents/DECISIONS.md`, `.agents/GLOSSARY.md`.
   - Inspect top-level project structure and main code directories (`src/`).

2. **Generate Standard Knowledge Base (`.agents/KB/`)**:
   Create or refresh the following structured articles:
   - **`.agents/KB/INDEX.md`**: Central entry point with topic map and cross-links (`[[links]]`).
   - **`.agents/KB/01-architecture.md`**: System components, data flows, boundaries, and tech stack overview.
   - **`.agents/KB/02-domain-model.md`**: Key domain concepts, entities, business logic, and glossary terms.
   - **`.agents/KB/03-setup-and-workflow.md`**: Environment setup, build/run/test instructions, and development conventions.

3. **Synchronize KB Index**:
   - Run `/sync-kb` to index `.agents/KB/` and human `docs/` for hybrid semantic search.
