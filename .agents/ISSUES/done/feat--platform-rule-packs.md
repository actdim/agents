---
slug: feat--platform-rule-packs
type: feat
status: done
priority: high
created: 2026-08-27
updated: 2026-08-27
completed: 2026-08-27
agent: antigravity
tags: [rules, platforms, msw, architecture, guidelines]
milestone: v1.3.0-knowledge-base-and-graph
blocked_by: []
related: []
---

# Feature: Platform Rule Packs (Application Archetypes)

## Context & Objectives
Expand `rules/` beyond programming languages into platform archetypes (Web, Desktop, Mobile, Backend, CLI), including the MSW API-mocking standard. Reorganize directory into `rules/languages/` and `rules/platforms/`.

## Tasks
- [x] Create implementation plan.
- [x] Move language rules to `rules/languages/`.
- [x] Create `rules/platforms/web.md` with MSW API mocking, state separation, SSR safety, A11y.
- [x] Create `rules/platforms/desktop.md` with IPC security, window lifecycle, offline storage.
- [x] Create `rules/platforms/mobile.md` with touch UX, permissions, offline sync, battery/memory limits.
- [x] Create `rules/platforms/backend.md` with REST/gRPC contracts, transactions, idempotency, observability.
- [x] Create `rules/platforms/cli.md` with POSIX flags, stdout/stderr stream isolation, exit codes.
- [x] Update `rules/INDEX.md` with auto-detection mappings.
- [x] Update `install.sh` and `install.ps1`.
- [x] Verify typography and installation.
