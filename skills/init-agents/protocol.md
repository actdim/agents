# ACTDIM-AGENTS-PROTOCOL v1.5.1

This repo carries its own agent context, provider-agnostically. Follow it every session, whatever tool you are.

## Scope & precedence
- Any folder may carry its own `AGENTS.md` + `.agents/`; they apply to that folder and everything under it. Use the NEAREST ones for the area you're working in; higher-level ones add broader context. On conflict, the more specific wins.
- Global/user config still applies as defaults (Claude auto-loads `~/.claude/CLAUDE.md`, Codex `~/.codex/AGENTS.md`, Antigravity `~/.gemini/config/GEMINI.md`). Precedence: nearest > higher-level > global.

## At session start - read these yourself (they are NOT auto-loaded)
Use the NEAREST `.agents/` for the area you're working in (fall back to a higher-level one if the folder has none):
1. `AGENTS.md` (nearest) - conventions to follow.
2. `.agents/CONTEXT.md` - current state.
3. `.agents/ISSUES.md` - active issue board.
4. `.agents/DECISIONS.md` - don't contradict.
Also, when relevant: `.agents/VISION.md`, `.agents/GLOSSARY.md`, and the `.agents/ISSUES/<type>--<slug>.md` you'll work on. These reflect the state WHEN WRITTEN - verify any named file/API/flag against the real code first.

## Entity Ecosystem & Structured Metadata
All entities are designed for zero-friction auto-parsing by dashboards and tools via YAML front-matter:

### 1. Issues (`.agents/ISSUES/<type>--<slug>.md`)
- **Placement**: Nearest `.agents/ISSUES/`. Types: `feat`, `bug`, `debt`, `task`, `docs`.
- **Front-matter**:
  - `slug`: lowercase kebab-case slug (2–5 words).
  - `type`: `feat` | `bug` | `debt` | `task` | `docs`.
  - `status`: `open` | `in-progress` | `blocked` | `done`.
  - `priority`: `critical` | `high` | `medium` | `low`.
  - `created`: `YYYY-MM-DD`.
  - `updated`: `YYYY-MM-DD`.
  - `completed`: `YYYY-MM-DD` (mandatory when `status: done` / moved to `done/`).
  - `agent`: model or tool name (e.g. `antigravity`, `claude-code`).
  - `tags`: array of tags (e.g. `[mcp, protocol]`).
  - `milestone`: optional milestone slug (e.g. `v1.5.0-dashboard`).
- `.agents/ISSUES.md` is the compact board read every session (`## Active`, `## Backlog`, `## Done (recent)`).
- On completion: set `status: done` and `completed: YYYY-MM-DD`, MOVE to `.agents/ISSUES/done/<type>--<slug>.md`, and update `.agents/ISSUES.md`.

### 2. Milestones & Releases (`.agents/MILESTONES/<slug>.md`)
- Group multiple issues into a release target, stage, or sprint.
- **Front-matter**: `slug`, `title`, `status` (`open` | `in-progress` | `completed`), `due_date`, `created`, `target_issues: []`, `progress_pct`.

### 3. Risks & Blockers (`.agents/RISKS/<slug>.md`)
- Track external dependencies, API limits, blocking ambiguities, and security flags.
- **Front-matter**: `slug`, `title`, `severity` (`critical` | `high` | `medium` | `low`), `status` (`active` | `mitigated` | `resolved`), `owner` (`agent` | `user`), `mitigation`, `created`, `updated`.

### 4. Spikes & R&D Experiments (`.agents/SPIKES/<slug>.md`)
- Exploratory spikes, benchmark experiments, and library evaluations before implementation.
- **Front-matter**: `slug`, `title`, `status` (`hypothesis` | `evaluating` | `concluded`), `hypothesis`, `outcome`, `resulting_adr`, `created`.

### 5. Checklists & Verification (`.agents/CHECKLISTS/<slug>.md`)
- Reusable verification checklists for quality gates, pre-commit, and security audits.
- **Front-matter**: `slug`, `title`, `category` (`pre-commit` | `stage-completion` | `release` | `security`), `items: [{ id, text, verified: bool }]`.

### 6. Sessions (`.agents/SESSIONS/<YYYY>/<YYYY-MM-DD>--<slug>.md`)
- Comprehensive work session log.
- **Front-matter**: `date`, `slug`, `agent`, `branch`, `commit`, `summary`, `milestone`, `issues_advanced: []`, `issues_completed: []`, `decisions: []`, `risks_logged: []`, `spikes_conducted: []`.

## Automated Intent Recognition & Entity Heuristics (Zero Human Friction)
Agents MUST automatically detect user intent and maintain entities in the background without prompting the human to manage project tracking:

| User Trigger / Natural Prompt | Auto-Inferred Entity | Automatic Agent Action (in background) |
| :--- | :--- | :--- |
| *"Build feature X"*, *"Fix bug Y"*, *"Refactor Z"* | **`ISSUE`** | Auto-create `.agents/ISSUES/<type>--<slug>.md` & add to `ISSUES.md`. On completion, set `status: done`, `completed: YYYY-MM-DD` & move to `done/`. |
| *"API rate limit hit"*, *"Waiting for API key"*, *"Blocked on X"* | **`RISK / BLOCKER`** | Auto-create `.agents/RISKS/<slug>.md` (`status: active`), mark related issue as `status: blocked`. |
| *"Compare library A vs B"*, *"Benchmark SQLite vs DuckDB"*, *"Test if X works"* | **`SPIKE`** | Auto-create `.agents/SPIKES/<slug>.md`. After testing, document outcome & generate ADR in `DECISIONS.md` if an architectural choice was made. |
| *"Sprint goal"*, *"Preparing Release v1.5"*, *"Target for next milestone"* | **`MILESTONE`** | Auto-create `.agents/MILESTONES/<slug>.md` and link newly created issues via `milestone: <slug>`. |
| *"I'm done for today"*, *"Wrap up"*, or Stage Completion | **`SESSION & CHECKLIST`** | Execute mandatory stage wrap-up checklist, compile `.agents/SESSIONS/`, and update compact boards. |

### Anti-Pollution & Entity Filtering Rules
To keep `.agents/` lean and avoid token bloat:
1. **Simple Q&A ("How does function X work?")**: Read-only, DO NOT create issues or entity files.
2. **Micro-edits (1-line typo fix, comment change)**: Record directly in the session log; DO NOT create an issue file.
3. **Non-trivial code changes (new logic, bug fixes, refactoring)**: ALWAYS ensure an `ISSUE` exists and tracks progress.

## Knowledge Base (KB) Management
- **Structured Knowledge Base**: Maintain project documentation in `.agents/KB/` (or `docs/`) with standard articles:
  - `INDEX.md`: Central cross-linked topic map (`[[link]]`).
  - `01-architecture.md`: System components, boundaries, and data flows.
  - `02-domain-model.md`: Domain concepts, business logic, and terms.
  - `03-setup-and-workflow.md`: Build, run, test, and workflow instructions.
- **Front-matter Schema**: Every `.agents/KB/*.md` article MUST include YAML front-matter: `slug`, `title`, `type` (`topic` | `architecture` | `domain-model` | `setup-workflow` | `index`), `created`, `updated`, `tags: []`.
- **Bootstrapping**: Use `/init-kb` to bootstrap or refresh `.agents/KB/` from existing `README.md`, `AGENTS.md`, human `docs/`, and codebase analysis.
- **Strict Fact Grounding Requirement**: Agents MUST extract facts strictly from actual `README.md`, `docs/`, `package.json`, and codebase symbols. Generating generic LLM placeholders is strictly prohibited.
- **Maintenance**: Update corresponding articles in `.agents/KB/` and run `/sync-kb` when implementing non-trivial architectural changes.

## While working
- Follow the conventions in `AGENTS.md`.
- `DECISIONS.md` is APPEND-ONLY: add a new dated entry per non-trivial architectural decision; never edit past ones - mark a replaced one "Superseded by #N".
- Add any new/clarified domain term to `.agents/GLOSSARY.md`.
- **Context & Token hygiene**: Keep tool output lean to prevent context bloat. Use quiet flags for builds/tests (`pytest -q`, `dotnet test -v q`), filter command outputs, and inspect targeted line ranges.
- **Code graph & Impact analysis**: Prioritize `code-review-graph` MCP tools (`build_or_update_graph_tool`, `get_impact_radius_tool`) during research and refactoring to inspect dependencies with minimal token overhead.
- **Hybrid Knowledge Base Search (KB)**: Prioritize `search-kb` or `wiki-llm` MCP tools for targeted searches across `.agents/`, `docs/`, `wiki/`, `README.md`.

## Mandatory Stage & Session Completion Checklist
When a Stage or session completes, agents MUST execute this verification checklist in exact order:
1. [ ] **Verification & Tests**: Run automated unit tests / linting / builds with quiet flags.
2. [ ] **Entity Reconciliation**:
   - Set `status: done` and `completed: YYYY-MM-DD` for finished issues; MOVE to `.agents/ISSUES/done/`.
   - Update related `.agents/MILESTONES/` progress percentages.
   - Resolve mitigated `.agents/RISKS/` (`status: resolved` / `mitigated`).
   - Conclude active `.agents/SPIKES/` and log any resulting ADR in `.agents/DECISIONS.md`.
3. [ ] **Documentation Check**: Update `README.md`, `AGENTS.md` (project specifics), or `.agents/KB/` if code interfaces or architecture changed.
4. [ ] **Session Log**: Write `.agents/SESSIONS/<YYYY>/<YYYY-MM-DD>--<short-slug>.md` with complete front-matter (`issues_advanced`, `issues_completed`, `decisions`, `risks_logged`, `spikes_conducted`).
5. [ ] **CONTEXT Snapshot**: Rewrite `.agents/CONTEXT.md` to a short "you are here" snapshot (< 20 lines).
6. [ ] **ISSUES Board**: Update `.agents/ISSUES.md` (keep active list lean, reflect done items).
7. [ ] **HISTORY**: Append one line to `.agents/HISTORY.md`: `<YYYY-MM-DD> - <slug> - <agent> - <summary> - <link>`.
8. [ ] **Compaction Prompt**: Advise user to run `/compact` to free up token budget.

## Rules
- **Strict File Modification & Anti-Deletion**:
  - **Zero Unintended Deletions**: Never delete, truncate, or overwrite existing documentation, comments, planned features, or code unless explicitly instructed by the user.
  - **Minimal Edit Scope**: Anchor edit blocks strictly on exact single lines or minimal unique chunks.
  - **Mandatory Diff Verification**: After modifying any file, inspect the generated diff to ensure only intended lines were touched.
  - **Immediate Rollback**: If an unintended deletion or truncation is detected, restore missing lines immediately.
- **Technical Markdown & Formatting Standards**:
  - **Forbidden Symbol (No Em-Dash `—`)**: NEVER use the em-dash character (`—`, U+2014) in markdown files, code comments, session logs, or documentation. Use standard ASCII hyphens (`-`), colons (`:`), or parentheses `()`.
  - **Clean ASCII Punctuation**: Avoid typographic curly quotes (`“`, `”`, `‘`, `’`) in code blocks, shell commands, and YAML front-matter; use standard ASCII quotes (`"`, `'`).
  - **Explicit Code Fence Languages**: Always specify the language identifier on code fences (e.g. ```` ```bash ````, ```` ```yaml ````, ```` ```typescript ````, ```` ```python ````). Never use bare unlabelled fences.
  - **Relative & Portable Links**: Always use relative paths (`file://...` or standard markdown links) without hardcoding local absolute paths.
  - **UTF-8 Clean Encoding**: Keep all text files in clean UTF-8 without BOM.
- Windows-safe filenames: dates `YYYY-MM-DD` (no `:`), date first.
- Keep `CONTEXT.md` and `ISSUES.md` compact - they cost context every session.
- Never write secrets/credentials/tokens/keys into these files; they are committed.

