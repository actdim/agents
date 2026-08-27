# Engineering Standards & Rule Packs

Modular language-specific and platform-specific engineering standards for `actdim-agents`.

---

## Overview

Rule packs provide strict, pragmatic engineering standards for both programming languages and software application archetypes. When running `/init-agents` in a repository, the agent inspects project descriptors (`package.json`, `pyproject.toml`, `*.csproj`, `tauri.conf.json`, `pnpm-workspace.yaml`, `Directory.Packages.props`, etc.) and attaches matching guidelines to `## Project specifics` in `AGENTS.md` and `.agents/KB/03-setup-and-workflow.md`.

---

## Available Language Rule Packs

| Language | Rule File | Primary Focus & Standards |
| :--- | :--- | :--- |
| **C# / .NET** | [`languages/csharp.md`](file://rules/languages/csharp.md) | Central Package Management (`Directory.Packages.props`), `Directory.Build.props`, Modern .NET 8+, Nullable reference types, Async/Await correctness, Memory efficiency (`Span<T>`, records). |
| **TypeScript** | [`languages/typescript.md`](file://rules/languages/typescript.md) | PNPM Workspaces (`workspace:*`, Catalogs), Strict type safety, Zero `any`, Explicit function return types, Discriminated unions, Immutable structures. |
| **JavaScript** | [`languages/javascript.md`](file://rules/languages/javascript.md) | Modern ES2022+, ESM modules, Async/Await error handling, Defensive object manipulation. |
| **Python** | [`languages/python.md`](file://rules/languages/python.md) | UV Workspaces (`[tool.uv.workspace]`), Modern Python 3.11+, PEP 8, Type annotations (`mypy`/`pyright`), Dataclasses/Pydantic, Ruff linting. |
| **Rust** | [`languages/rust.md`](file://rules/languages/rust.md) | Cargo Workspace dependency inheritance (`[workspace.dependencies]`), Memory safety, Zero panic in production (`unwrap`/`expect` ban), `thiserror`/`anyhow`. |

---

## Available Platform & Application Archetypes

| Platform / Archetype | Rule File | Primary Focus & Architectural Standards |
| :--- | :--- | :--- |
| **Monorepos & Workspaces** | [`platforms/monorepo.md`](file://rules/platforms/monorepo.md) | Multi-package / multi-platform architecture (`apps/*` vs `packages/*`), strict dependency flow, Central Package Management (CPM), dual workspace/registry resolution, filtered CI builds. |
| **Web Applications** | [`platforms/web.md`](file://rules/platforms/web.md) | Web SPA/SSR, Mock Service Worker (MSW) REST simulation standard for serverless local dev & testing, Server/Client state separation, SSR hydration safety, A11y (WCAG 2.1), Optimistic updates. |
| **Desktop Applications** | [`platforms/desktop.md`](file://rules/platforms/desktop.md) | Tauri / Electron / Native, IPC least-privilege security, File system sandboxing & atomic writes, Window & process lifecycle, Embedded SQLite/DuckDB. |
| **Mobile Applications** | [`platforms/mobile.md`](file://rules/platforms/mobile.md) | React Native / Expo / Flutter, 44x44 touch targets & safe areas, Offline-first storage & conflict resolution, Just-in-time permissions, Battery/RAM limits. |
| **Backend & Services** | [`platforms/backend.md`](file://rules/platforms/backend.md) | REST / gRPC API contracts, 12-Factor stateless services, Idempotent mutations, Atomic DB transactions & connection pools, Structured JSON telemetry. |
| **CLI Tools** | [`platforms/cli.md`](file://rules/platforms/cli.md) | POSIX argument parsing, Strict stdout (data) vs stderr (logs) isolation, Standard exit codes (0, 1, 2, 130), Non-interactive TTY / `NO_COLOR` support. |

---

## Automatic Detection Matrix

When `/init-agents` scaffolds or refreshes a project:

| Detected File or Dependency | Inferred Rule Pack |
| :--- | :--- |
| `Directory.Packages.props`, `pnpm-workspace.yaml`, `[workspace]` in `Cargo.toml` | `rules/platforms/monorepo.md` |
| `tsconfig.json`, `*.ts`, `*.tsx` | `rules/languages/typescript.md` |
| `pyproject.toml`, `requirements.txt`, `setup.py` | `rules/languages/python.md` |
| `*.csproj`, `*.sln`, `Directory.Build.props` | `rules/languages/csharp.md` |
| `Cargo.toml`, `src/main.rs`, `src/lib.rs` | `rules/languages/rust.md` |
| `vite.config.*`, `next.config.*`, `msw`, `react-dom` | `rules/platforms/web.md` |
| `src-tauri/`, `electron-builder.*`, `tauri.conf.json` | `rules/platforms/desktop.md` |
| `react-native`, `expo`, `pubspec.yaml` | `rules/platforms/mobile.md` |
| `docker-compose.yml`, `fastapi`, `express`, `nest-cli.json` | `rules/platforms/backend.md` |

---

## Usage in Repositories

1. **Automatic Detection (`/init-agents`)**:
   - The agent inspects project descriptors and adds matching rules to `AGENTS.md`.
2. **Manual Reference**:
   - Reference in `AGENTS.md`: `See rules/platforms/monorepo.md, rules/platforms/web.md and rules/languages/typescript.md for engineering guidelines.`
   - Or include as Knowledge Base articles in `.agents/KB/`.
