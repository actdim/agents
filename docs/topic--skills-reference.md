---
protocol: along
slug: topic--skills-reference
title: Skills & Slash Commands Technical Reference
type: topic
created: 2026-08-30
updated: 2026-08-30
tags: [skills, commands, reference, runners, lifecycle]
---

# Skills & Slash Commands Technical Reference

Along provides a complete suite of **17 singular automation skills** operating across Claude Code, OpenAI Codex, OpenCode, and Google Antigravity.

---

## 1. Complete Skills & Slash Commands Catalog

| Skill Name | Canonical Command | Invocation Script | Purpose |
| :--- | :--- | :--- | :--- |
| `along-init` | `/along-init` | `python skills/along-init/along_init.py` | Scaffold or refresh `AGENTS.md` and `.along/` in a directory. |
| `along-update` | `/along-update` | `python skills/along-update/along_update.py` | One-liner update of repository context and global skills from GitHub. |
| `along-dash` | `/along-dash` | `python scripts/along_dash.py -w` | Launch dynamic FastAPI executive dashboard and Cytoscape DAG UI. |
| `along-wrap` | `/along-wrap` | `along-wrap` | Unified session finalization: verification, session log, context, issues, history. |
| `along-commit` | `/along-commit` | `along-commit -i <slug>` | ASCII cleanliness check and Conventional Commit linked to active issue. |
| `along-build` | `/along-build` | `python skills/along-build/along_build.py` | Universal build lifecycle runner (.along/scripts/build.py, npm, cargo, dotnet). |
| `along-test` | `/along-test` | `python skills/along-test/along_test.py` | Automated test suite runner with quiet flags (pytest, npm, cargo, dotnet). |
| `along-dev` | `/along-dev` | `python skills/along-dev/along_dev.py` | Local development and debugging server runner. |
| `along-kb-sync` | `/along-kb-sync` | `python skills/along-kb-sync/along_kb_sync.py` | Idempotent LLM-Wiki Knowledge Base compiler in `docs/`. |
| `along-kb-search` | `/along-kb-search` | `python skills/along-kb-search/along_kb_search.py` | Fast unified search across `docs/` and `.along/` project memory. |
| `along-issue-sync` | `/along-issue-sync` | `python skills/along-issue-sync/along_issue_sync.py` | Reconcile active issue board and `<type>--<slug>.md` entity files. |
| `along-context-sync` | `/along-context-sync` | `python skills/along-context-sync/along_context_sync.py` | Refresh and compact the nearest `.along/CONTEXT.md` (<20 lines). |
| `along-decision-sync` | `/along-decision-sync` | `python skills/along-decision-sync/along_decision_sync.py` | Append numbered ADR entries in `.along/DECISIONS.md`. |
| `along-history-sync` | `/along-history-sync` | `python skills/along-history-sync/along_history_sync.py` | Reconstruct `.along/` entities and milestones from Git commit history. |
| `along-graph-check` | `/along-graph-check` | `python scripts/along_graph_check.py` | Evaluate `code-review-graph` AST impact radius and blast radius. |
| `along-dep-scan` | `/along-dep-scan` | `python scripts/along_dep_scan.py` | Scan declared dependencies for AI instructions into `docs/topic--dependencies.md`. |
| `along-version-bump` | `/along-version-bump` | `python scripts/along_version_bump.py` | Multi-stack version bump with pre-commit test gate and release commit. |
| `along-team` | `/along-team` | `along-team` | Multi-agent autonomous team coordination and living execution plans. |
| `along-feedback` | `/along-feedback` | `python scripts/along_feedback.py` | System self-diagnostics, incident logging, and feedback dispatch (Telegram/Webhook/File). |

---

## 2. Adaptive Ingestion in `along-kb-sync`

`along-kb-sync` operates adaptively without needing multiple fragmented skills:
- **Direct Mode**: For incremental updates (1-3 files), the agent compiles articles and runs `along_kb_sync.py` directly.
- **Parallel Mode**: When handling massive external documentation dumps or multi-package monorepos, the agent decomposes extraction into discrete domain vectors, spawns parallel research subagents, and reconciles all generated articles into `docs/` with automated link linting.

---

## 3. Version Bump & Release Commands (`along-version-bump`)

```bash
# Bump patch version with automated test execution and git commit
python scripts/along_version_bump.py patch -c

# Bump minor version with commit and push
python scripts/along_version_bump.py minor -c -p

# Bump to explicit target version
python scripts/along_version_bump.py 2.2.0 -cp
```
