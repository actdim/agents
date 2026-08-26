# ACTDIM-AGENTS-PROTOCOL v1.3.1

This repo carries its own agent context, provider-agnostically. Follow it every session, whatever tool you are.

## Scope & precedence
- Any folder may carry its own `AGENTS.md` + `.agents/`; they apply to that folder and everything under it. Use the NEAREST ones for the area you're working in; higher-level ones add broader context. On conflict, the more specific wins.
- Global/user config still applies as defaults (Claude auto-loads `~/.claude/CLAUDE.md`, Codex `~/.codex/AGENTS.md`, Antigravity `~/.gemini/config/GEMINI.md`). Precedence: nearest > higher-level > global.

## At session start — read these yourself (they are NOT auto-loaded)
Use the NEAREST `.agents/` for the area you're working in (fall back to a higher-level one if the folder has none):
1. `AGENTS.md` (nearest) — conventions to follow.
2. `.agents/CONTEXT.md` — current state.
3. `.agents/ISSUES.md` — active issue board.
4. `.agents/DECISIONS.md` — don't contradict.
Also, when relevant: `.agents/VISION.md`, `.agents/GLOSSARY.md`, and the `.agents/ISSUES/<type>--<slug>.md` you'll work on. These reflect the state WHEN WRITTEN — verify any named file/API/flag against the real code first.

## Issues
- **Placement in Nearest `.agents/`**: In multi-module or nested projects where subfolders carry their own `AGENTS.md` + `.agents/`, ALWAYS create and manage issues in the NEAREST `.agents/` directory for the subproject/area the issue belongs to. DO NOT dump all subproject issues into the root `.agents/`. Only repository-wide or cross-cutting issues belong in the root `.agents/`.
- One file per issue, formatted as `.agents/ISSUES/<type>--<slug>.md` (slug = lowercase kebab-case, 2–5 words).
- Supported types (`<type>`): `feat` (feature), `bug` (bug fix), `debt` (tech debt / refactoring), `task` (general task), `docs` (documentation).
- Issue YAML front-matter: `slug`, `type`, `status` (`open` | `in-progress` | `blocked` | `done`), `priority` (`critical` | `high` | `medium` | `low`), `created`, `updated`.
- `.agents/ISSUES.md` is the compact board read every session (`## Active`, `## Backlog`, `## Done (recent)`).
- On completion, MOVE the file to `.agents/ISSUES/done/<type>--<slug>.md` and update the board in that same nearest `.agents/`.

## Knowledge Base (KB) Management
- **Structured Knowledge Base**: Maintain project documentation in `.agents/KB/` (or `docs/`) with standard articles:
  - `INDEX.md`: Central cross-linked topic map (`[[link]]`).
  - `01-architecture.md`: System components, boundaries, and data flows.
  - `02-domain-model.md`: Domain concepts, business logic, and terms.
  - `03-setup-and-workflow.md`: Build, run, test, and workflow instructions.
- **Bootstrapping**: Use `/init-kb` to bootstrap or refresh `.agents/KB/` from existing `README.md`, `AGENTS.md`, human `docs/`, and codebase analysis.
- **Strict Fact Grounding Requirement**: When generating (`/init-kb`) or updating (`/sync-kb`) Knowledge Base articles, agents MUST extract facts strictly from actual `README.md`, `docs/`, `package.json`, and codebase symbols. Generating generic LLM placeholders, placeholder component names (e.g. "Schema Parser"), or domain concepts not explicitly found in the codebase is strictly prohibited.
- **Maintenance**: When implementing non-trivial features or architectural changes, update corresponding articles in `.agents/KB/` and run `/sync-kb`.

## While working
- Follow the conventions in `AGENTS.md`.
- `DECISIONS.md` is APPEND-ONLY: add a new dated entry per non-trivial architectural decision; never edit past ones — mark a replaced one "Superseded by #N".
- Add any new/clarified domain term to `.agents/GLOSSARY.md`.
- **Context & Token hygiene**: Keep tool output lean to prevent context bloat. Use quiet flags for builds/tests (e.g. `dotnet test -v q`, `pytest -q`), filter/limit command outputs, and inspect targeted line ranges instead of loading whole large files.
- **Code graph & Impact analysis**: If code graph tools (e.g. `code-review-graph` MCP: `build_or_update_graph_tool`, `get_impact_radius_tool`, `get_architecture_overview_tool`, `list_flows_tool`) are available, prioritize using them during research and refactoring to inspect dependencies, trace call hierarchies, and measure change impact with minimal token overhead.
- **Hybrid Knowledge Base Search (KB)**: If `wiki-llm` MCP tools (`search_wiki_tool`, `get_wiki_article_tool`) or KB search tools are available, use them to perform hybrid semantic search (TF-IDF + Vector + Cross-links) across existing project documentation (`.agents/`, `docs/`, `wiki/`, `README.md`) instead of reading whole raw Markdown files. Use `/sync-kb` (or `/sync-wiki`) to update hybrid vector indexes after adding or modifying documentation.

## Stage Completion Triggers
A **Stage** (or milestone phase) is a meaningful, verified unit of work. An agent MUST recognize that a Stage is complete when:
1. **Issue Acceptance Met**: An active Issue (`.agents/ISSUES/<type>--<slug>.md`) has satisfied its acceptance criteria and passes verification.
2. **Plan Milestone Reached**: A distinct phase of an implementation plan agreed with the user is complete.
3. **Explicit Request**: The user asks to wrap up, checkpoint, or complete the current stage.

## Stage & Session Wrap-up Protocol (Update in order)
When a Stage or session completes, perform the following steps:
1. **Documentation & Protocol Check** — Review if `README.md`, `AGENTS.md` (project conventions), or project guides need updates following the completed stage/task. Update them or report required doc updates.
2. **Session log** — Write a new session file `.agents/SESSIONS/<YYYY>/<YYYY-MM-DD>--<short-slug>.md` (slug 2–5 words; if it exists, suffix `-02`…). Begin with YAML front-matter (`date`, `slug`, `agent` = tool/model, `branch`, `commit`, `summary`), then a body: what changed & why, files touched, decisions (by slug/#N), issues advanced, gaps/follow-ups.
3. **CONTEXT** — Rewrite `.agents/CONTEXT.md` to the new state — a SHORT snapshot, not a log; history goes to the session file.
4. **ISSUES** — Update `.agents/ISSUES.md` (+ move any completed issue to `ISSUES/done/`).
5. **HISTORY** — Append one line to `.agents/HISTORY.md`: `<YYYY-MM-DD> — <slug> — <agent> — <summary> — <link>`.
6. **VISION** — Touch `.agents/VISION.md` only if scope/roadmap changed.
7. **Compaction prompt** — Advise the user to run `/compact` (or restart the session) if continuing in the same conversation, as the state is now safely committed to `.agents/`.

## Rules
- Windows-safe filenames: dates `YYYY-MM-DD` (no `:`), date first. Issue files keep a stable `<type>--<slug>.md` name; the only move is open → `ISSUES/done/`.
- Keep `CONTEXT.md` and `ISSUES.md` compact — they cost context every session.
- Never write secrets/credentials/tokens/keys into these files; they are committed.

