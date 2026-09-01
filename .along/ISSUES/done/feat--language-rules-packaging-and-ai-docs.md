---
protocol: along
protocol_version: 2.2.7
slug: feat--language-rules-packaging-and-ai-docs
type: feat
status: done
completed: 2026-09-01
priority: high
created: 2026-09-01
updated: 2026-09-01
agent: antigravity
tags: [rules, packaging, nuget, npm, pypi, cargo, ai-docs, wiki]
milestone: v2.0.0-along-transition
blocked_by: []
related: []
---

# Feature: Language Rules Packaging and AI Docs Distribution

## Description
Extend language-specific rules in `rules/languages/` (C#/.NET, Python, TypeScript, JavaScript, Rust) with explicit guidelines and configuration standards for authoring, packaging, and distributing AI documentation (`AGENTS.md`, `llms.txt`, and `docs/` Wiki) to package consumers across standard and recommended package management tooling.

## Acceptance Criteria
- [x] `rules/languages/csharp.md` updated with Section 6 covering MSBuild / `Directory.Build.props` / `*.csproj` packaging of `AGENTS.md`, `llms.txt`, and `docs/` into `.nupkg`.
- [x] `rules/languages/python.md` updated with Section 6 covering `pyproject.toml` (Setuptools, Hatchling, Flit, Poetry), `MANIFEST.in`, and UV workspace packaging.
- [x] `rules/languages/typescript.md` updated with Section 6 covering `package.json` `"files"`, `"ai"` metadata, and PNPM workspace publishing.
- [x] `rules/languages/javascript.md` updated with Section 4 covering `.npmignore` safety, `package.json` `"files"`, and metadata.
- [x] `rules/languages/rust.md` updated with Section 6 covering `Cargo.toml` `include` array and crate metadata.
- [x] All files verified for clean ASCII typography and explicit code fences.
