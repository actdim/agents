---
protocol: along
slug: hierarchical-dep-scan-and-wiki-integration
type: feat
status: done
priority: high
created: 2026-08-30
updated: 2026-08-30
completed: 2026-08-30
agent: antigravity
tags: [dependencies, kb, wiki, submodules, multi-project, nuget, node, python, rust]
milestone: v1.3.0-knowledge-base-and-graph
blocked_by: []
related: []
---

# Hierarchical Multi-Project Dependency Scanner & Wiki Integration

## Description
Upgrade `along-dep-scan` (`skills/along-dep-scan/along_dep_scan.py`) to support:
1. Multi-level recursive scanning of subprojects, monorepo packages, git submodules, and symlinks.
2. Traversal ignore rules (skipping `node_modules`, `.git`, `.venv`, `bin`, `obj`, `dist`, `build`, `.archive`, `.cache`, etc.).
3. Multi-ecosystem parsing: Node.js (npm/pnpm/yarn/bun), Python (pip/poetry/uv), .NET (NuGet `*.csproj`, `Directory.Packages.props`), Rust (Cargo), Go (`go.mod`).
4. Project-specific adaptive scripting hook: `.along/scripts/dep_scan.py` support and automatic template synthesis for custom/unknown stacks.
5. Wiki Integration: Updating `docs/topic--dependencies.md` and `docs/INDEX.md` with structured sections for both internal subprojects/submodules and declared external dependencies with relative links to AI documentation files.

## Acceptance Criteria
- [x] Recursive project discovery traverses repository tree, following submodules and symlinks while avoiding loops and skipping build/ignore directories.
- [x] Node, Python, .NET (NuGet), Rust, and Go dependencies are scanned and attributed to their declaring project scope.
- [x] Project hook `.along/scripts/dep_scan.py` is supported with adaptive fallback/synthesis.
- [x] Discovered AI instructions in dependencies (`AGENTS.md`, `llms.txt`, `docs/`, etc.) and internal subprojects are linked into `docs/topic--dependencies.md` with valid relative links.
- [x] Automated tests in `tests/test_scan_deps.py` verify all scenarios.

