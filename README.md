# Along (v2.1.5)

A provider-agnostic **agent-context and memory system** for software repositories - the `ALONG-PROTOCOL v2.1.5` plus the automation skills suite that scaffolds and maintains it. One unified convention, honored natively across **Claude Code**, **OpenAI Codex**, **OpenCode**, and **Google Antigravity**.

---

## Why Along?

AI coding agents start every session blind. They lack persistent memory of past architectural decisions, work in progress, open issues, or repository conventions. Each tool maintains its own isolated configuration (`~/.claude`, `~/.codex`, `~/.config/opencode`, `~/.gemini/config`), leading to context loss and fragmented workflows.

**Along fixes this by giving the repository an isolated, durable, human-readable memory directory (`.along/`) and a structured Knowledge Base (`docs/`) that all agents read and maintain collaboratively.**

---

## Core Value Proposition

- **Persistent In-Repo Memory**: Context snapshot, DAG issue tracking, append-only ADR log, milestones, risks, and session logs committed with the code.
- **Provider-Agnostic Single Protocol**: Write conventions once in `AGENTS.md`; Claude Code, Codex, OpenCode, and Antigravity follow them identically.
- **LLM-Wiki Knowledge Base (`docs/`)**: Modular, cross-linked topic articles with isolated raw source archival (`.archive/`) and 95-98% token reduction on retrieval.
- **Nearest Context Boundary**: Strict isolation for monorepos, microservices, and Git submodules preventing root workspace pollution.
- **Zero Bookkeeping Overhead**: 17 automation skills handle scaffolding, sync, commit checks, and stage wrap-ups in the background.

---

## Quickstart & Installation

Install Along across all supported AI providers with a single command:

### Windows (PowerShell)
```powershell
git clone https://github.com/actdim/along.git
cd along
powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1 -Target all
```

### Linux / macOS (Bash)
```bash
git clone https://github.com/actdim/along.git
cd along
bash install.sh --target=all
```

---

## Knowledge Base & Architecture Index

The repository's complete technical specification is maintained as a living LLM-Wiki in [`docs/`](./docs/INDEX.md):

| Topic | Description | Link |
| :--- | :--- | :--- |
| **System Architecture** | Provider flow, context boundaries, MCP servers, and bridge layers. | [System Architecture & Flow](./docs/topic--architecture.md) |
| **Domain Model & Entities** | Machine-parseable schemas for Issues, ADRs, Milestones, and Risks. | [Domain Model & Entity Ecosystem](./docs/topic--domain-model.md) |
| **Setup & Workflows** | Installation matrix, repository onboarding, and session lifecycle. | [Setup, Installation & Workflows](./docs/topic--setup-and-workflow.md) |
| **LLM-Wiki Architecture** | Andrej Karpathy paradigm, source isolation, and token efficiency. | [LLM-Wiki Architecture & Paradigm](./docs/topic--llm-wiki-architecture.md) |
| **Skills & Commands** | Complete reference for all 17 singular automation skills. | [Skills & Commands Reference](./docs/topic--skills-reference.md) |
| **Frontend & Dashboard** | Reactive Dashboard architecture (`packages/dashboard-ui`), Dynstruct & MsgMesh. | [Frontend Architecture & Dashboard](./docs/topic--frontend-frameworks.md) |
| **Protocol Migrations** | Versioned migration engine and upgrade instructions. | [Protocol & Migrations Guide](./docs/topic--migrations.md) |
| **Dependency AI Rules** | AI instructions discovery across package manifests. | [Dependencies AI Documentation](./docs/topic--dependencies.md) |

---

## Automation Skills Reference (Singular Domain-First)

| Skill / Command | Purpose |
| :--- | :--- |
| `along-init` (`/along-init`) | Scaffold/refresh `AGENTS.md` + `CLAUDE.md` + `.along/` in a folder. |
| `along-update` (`/along-update`) | One-liner update of repository context, protocol, and global skills from GitHub. |
| `along-dash` (`/along-dash`) | Launch executive dashboard (Web UI, CLI, Cytoscape DAG, SVG/HTML export). |
| `along-wrap` (`/along-wrap`) | Unified end-of-stage update: code review, session log, context, issues, history. |
| `along-commit` (`/along-commit`) | Smart pre-commit ASCII check and Conventional Commit linked to active issue. |
| `along-build` (`/along-build`) | Project build lifecycle hook via `.along/scripts/build.py` or auto-detected runner. |
| `along-test` (`/along-test`) | Automated tests with quiet flags via `.along/scripts/test.py` or auto-detected runner. |
| `along-dev` (`/along-dev`) | Development / debugging server via `.along/scripts/dev.py` or auto-detected runner. |
| `along-kb-sync` (`/along-kb-sync`) | Synchronize, compile, and reconcile the Knowledge Base in `docs/` using LLM-Wiki pipeline. |
| `along-kb-search` (`/along-kb-search`) | Fast targeted structured retrieval across `docs/` and project documentation. |
| `along-issue-sync` (`/along-issue-sync`) | Reconcile the issue board + per-issue `<type>--<slug>.md` files with the actual work. |
| `along-context-sync` (`/along-context-sync`) | Refresh just the nearest `.along/CONTEXT.md`. |
| `along-decision-sync` (`/along-decision-sync`) | Append architectural decisions as ADR entries; mark superseded ones. |
| `along-history-sync` (`/along-history-sync`) | Reconstruct and reconcile `.along/` milestones, issues, and sessions from Git commits. |
| `along-graph-check` (`/along-graph-check`) | Inspect `code-review-graph` status, impact radius (blast radius), and architecture flows. |
| `along-dep-scan` (`/along-dep-scan`) | Scan declared dependencies for AI instructions and register in `docs/topic--dependencies.md`. |
| `along-version-bump` (`/along-version-bump`) | Multi-stack version bump (Node, Python, Rust, .NET, or .along/scripts/bump_version.py). |

---

## License

MIT License. See [LICENSE](./LICENSE) for details.
