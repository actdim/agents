---
name: init-kb
version: "1.2.0"
description: Bootstrap or refresh the structured Knowledge Base (.agents/KB/ or docs/) from README.md, AGENTS.md, docs/, and codebase analysis.
---

# Init Knowledge Base (`/init-kb`) [v1.2.0]

Use this skill to bootstrap or refresh a structured, interlinked **Knowledge Base (KB)** in `.agents/KB/` for any repository.

## Architectural Structure
- **`.agents/KB/`**: Primary agent Knowledge Base directory (`INDEX.md`, `01-architecture.md`, `02-domain-model.md`, `03-setup-and-workflow.md`).
- **Human Documentation (`docs/`, `README.md`)**: Always scanned as read-only inputs during `/init-kb` and `/sync-kb` to incorporate human-written specs and documentation into the Knowledge Base.
- **`AGENTS.md`**: Executive summary (protocol block + quick build commands + links to `.agents/KB/`).
- **`CLAUDE.md`**: Minimal 1-line import (`@AGENTS.md`).

## Workflow

1. **Source Content Analysis**:
   - Read human documentation in `docs/`, `README.md`.
   - Read agent context files: `AGENTS.md`, `.agents/CONTEXT.md`, `.agents/DECISIONS.md`, `.agents/GLOSSARY.md`.
   - Inspect top-level project structure and main code directories.

2. **Generate Standard Knowledge Base (`.agents/KB/`)**:
   Create or refresh the following structured articles:
   - **`.agents/KB/INDEX.md`**: Central entry point with topic map and cross-links (`[[links]]`).
   - **`.agents/KB/01-architecture.md`**: System components, data flows, boundaries, and tech stack overview.
   - **`.agents/KB/02-domain-model.md`**: Key domain concepts, entities, business logic, and glossary terms.
   - **`.agents/KB/03-setup-and-workflow.md`**: Environment setup, build/run/test instructions, and development conventions.

3. **Synchronize KB Index**:
   - Run `/sync-kb` to index `.agents/KB/` and human `docs/` for hybrid semantic search.
