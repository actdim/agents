---
protocol: along
slug: topic--skills-reference
title: Skills & Slash Commands Technical Reference
type: topic
created: 2026-08-30
updated: 2026-08-30
tags: [skills, commands, reference, aliases, runners]
---

# Skills & Slash Commands Technical Reference

Along ships with **17 Singular Domain-First skills** (`along-<entity>-<action>`), providing automated lifecycle management across Claude Code, Codex, OpenCode, and Antigravity.

---

## Skills Catalog

| Skill Name | Primary Command | Short Alias | Execution Runner | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `along-init` | `/along-init` | `/init` | `along-init` | Scaffold or refresh `AGENTS.md` and `.along/` in any folder. |
| `along-update` | `/along-update` | `/update` | `python scripts/along_update.py` | Sync local repo and global skills with latest upstream GitHub release. |
| `along-dash` | `/along-dash` | `/dash` | `python scripts/along_dash.py -w` | Launch dynamic FastAPI executive dashboard and Cytoscape DAG UI. |
| `along-wrap` | `/along-wrap` | `/wrap` | `along-wrap` | Unified session finalization: verification, session log, context, history. |
| `along-commit` | `/along-commit` | `/commit` | `python skills/along-commit/along_commit.py` | Clean ASCII check, pre-commit test gate, and issue-linked commit. |
| `along-build` | `/along-build` | `/build` | `.along/scripts/build.py` / auto | Project build lifecycle hook via auto-detected build runner. |
| `along-test` | `/along-test` | `/test` | `.along/scripts/test.py` / auto | Automated unit tests with quiet flags. |
| `along-dev` | `/along-dev` | `/dev` | `.along/scripts/dev.py` / auto | Development and debugging server runner. |
| `along-kb-sync` | `/along-kb-sync` | `/kb-sync` | `python skills/along-kb-sync/along_kb_sync.py` | Idempotent LLM-Wiki Knowledge Base compiler in `docs/`. |
| `along-kb-search` | `/along-kb-search` | `/kb-search` | `python skills/along-kb-search/along_kb_search.py` | Fast targeted structured retrieval across `docs/` and project documentation. |
| `along-issue-sync` | `/along-issue-sync` | `/issue-sync` | `along-issue-sync` | Reconcile nearest `.along/ISSUES.md` and per-issue files. |
| `along-context-sync` | `/along-context-sync` | `/context-sync` | `along-context-sync` | Refresh nearest `.along/CONTEXT.md` snapshot (< 20 lines). |
| `along-decision-sync` | `/along-decision-sync` | `/decision-sync` | `along-decision-sync` | Append ADR entries to nearest `.along/DECISIONS.md`. |
| `along-history-sync` | `/along-history-sync` | `/history-sync` | `along-history-sync` | Reconstruct `.along/` history, milestones, and sessions from Git. |
| `along-graph-check` | `/along-graph-check` | `/graph-check` | `along-graph-check` | Inspect `code-review-graph` MCP status, blast radius, and ignore filters. |
| `along-dep-scan` | `/along-dep-scan` | `/dep-scan` | `python skills/along-dep-scan/along_dep_scan.py` | Scan dependencies for AI instructions and register in `docs/dependencies.md`. |
| `along-version-bump` | `/along-version-bump` | `/version-bump` | `python scripts/along_bump_version.py` | Multi-stack version bump with pre-commit test gate and release commit. |

---

## Skill Details & Usage

### 1. `along-kb-sync` (`/along-kb-sync`, `/kb-sync`)
Bootstraps standard articles if `docs/` is empty, verifies YAML front-matter, validates relative Markdown links `[01-architecture.md](./01-architecture.md)`, and regenerates `docs/INDEX.md`.

```bash
python skills/along-kb-sync/along_kb_sync.py [REPO_ROOT] [--check]
```

### 2. `along-kb-search` (`/along-kb-search`, `/kb-search`)
Performs token-efficient snippet search across `docs/`, scoring matches in titles, tags, and body text.

```bash
python skills/along-kb-search/along_kb_search.py "<query>" [--limit 5] [--tag <tag>]
```

### 3. `along-version-bump` (`/along-version-bump`, `/version-bump`)
Universal version incrementer supporting Node (`package.json`), Python (`pyproject.toml`), Rust (`Cargo.toml`), .NET, or custom `.along/scripts/bump_version.py`.

```bash
python scripts/along_bump_version.py patch -c -p
```
