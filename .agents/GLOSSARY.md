# Glossary

_Domain terms for ACTDIM-AGENTS and repository tracking. Add or refine terms whenever introduced._

- **ACTDIM-AGENTS-PROTOCOL** - Provider-agnostic agent memory and project management standard enabling seamless pair-programming across Claude Code, Codex, OpenCode, and Antigravity via `.agents/` and `AGENTS.md`.
- **Issue** - Discrete, structured unit of work (`feat`, `bug`, `debt`, `task`, `docs`) tracked with YAML front-matter in `.agents/ISSUES/` and summarized in `.agents/ISSUES.md`.
- **Milestone** - Release target, stage, or sprint grouping multiple issues to measure delivery velocity and progress percentage in `.agents/MILESTONES/`.
- **Risk / Blocker** - Explicitly tracked technical blocker, missing API credential, external dependency, or security risk documented in `.agents/RISKS/` with mitigation plans.
- **Spike** - Exploratory research spike, benchmark evaluation, or PoC experiment documented in `.agents/SPIKES/` prior to architectural decision-making.
- **Checklist** - Reusable, step-by-step verification checklist (`pre-commit`, `stage-completion`, `release`, `security`) in `.agents/CHECKLISTS/` ensuring quality assurance compliance.
- **Session Log** - Immutable, structured work session record in `.agents/SESSIONS/<YYYY>/<YYYY-MM-DD>--<slug>.md` capturing files touched, issues advanced/completed, ADRs, and metrics.
- **ADR (Architectural Decision Record)** - Append-only record of a non-trivial architectural or technical choice stored in `.agents/DECISIONS.md`.
- **Knowledge Base (KB)** - Persistent project documentation repository in `.agents/KB/` (`INDEX.md`, `01-architecture.md`, `02-domain-model.md`, `03-setup-and-workflow.md`).
- **Zero Friction** - Operational paradigm where agents automatically infer developer intent from natural conversation and manage project tracking entities in the background without human overhead.
- **Context Token Hygiene** - Practice of keeping root context files (`CONTEXT.md`, `ISSUES.md`, `AGENTS.md`) strictly compact (< 50–80 lines) to prevent LLM context bloat while pushing details into session logs and KB articles.
