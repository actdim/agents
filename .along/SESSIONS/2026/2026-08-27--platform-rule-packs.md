---
protocol: along
date: 2026-08-27
slug: platform-rule-packs
agent: antigravity
branch: main
commit: HEAD
summary: Introduced Platform Rule Packs (Web with MSW REST simulation, Monorepo with Central Package Management, Desktop, Mobile, Backend, CLI), integrated CPM and Workspaces across language standards, and updated installer scripts.
milestone: v1.5.0-dashboard-and-analytics
issues_advanced: []
issues_completed: [feat--platform-rule-packs]
decisions: []
risks_logged: []
spikes_conducted: []
---

# Work Session: Platform Rule Packs, Central Package Management & Monorepo Architecture

Expanded the `rules/` engineering standard system by introducing modular Platform Rule Packs and deep integration of Central Package Management (CPM) across all supported programming languages and multi-platform monorepos.

## Changes Made

1. **Reorganized Rules Directory Taxonomy**:
   - Split `rules/` into two distinct categories: `rules/languages/` and `rules/platforms/`.
   - Relocated and enriched language standards (`csharp.md`, `javascript.md`, `python.md`, `rust.md`, `typescript.md`).

2. **Integrated Central Package Management Across Languages**:
   - `csharp.md`: Added Central Package Management standard via `Directory.Packages.props` (`<ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>`) and root `Directory.Build.props`.
   - `typescript.md`: Added PNPM Workspaces standard (`pnpm-workspace.yaml`), `workspace:*` dependency protocol, and PNPM Catalogs (`pnpm:catalog:`) for aligned tool versions.
   - `rust.md`: Added Cargo Workspace dependency inheritance (`[workspace.dependencies]` and `{ workspace = true }`).
   - `python.md`: Added UV Workspace management (`[tool.uv.workspace]`).

3. **Created Platform & Architectural Archetypes (`rules/platforms/`)**:
   - `monorepo.md`: Architectural guidelines for multi-platform repositories (`apps/*` vs `packages/*`), unidirectional dependency flow, domain contract isolation, and filtered CI testing.
   - `web.md`: Browser & SSR application standards, Mock Service Worker (MSW) REST simulation standard for serverless local dev & testing, server vs client state separation, and A11y.
   - `desktop.md`: Desktop standards (Tauri, Electron, Native), IPC security, filesystem sandboxing, and local SQLite.
   - `mobile.md`: Mobile standards (React Native, Expo, Flutter), 44x44 touch targets, Safe Area wrapping, and offline-first sync outbox.
   - `backend.md`: Backend standards, formal REST/gRPC contracts, 12-Factor statelessness, idempotent mutations, and database transactions.
   - `cli.md`: CLI standards, POSIX flags, stdout/stderr stream isolation, and exit code contracts.

4. **Updated Rules Index & Installer Scripts**:
   - Updated `rules/INDEX.md` with complete taxonomy tables and an auto-detection matrix mapping descriptors to rule packs.
   - Enhanced `install.ps1` and `install.sh` for recursive, deterministic deployment into tool configurations.
