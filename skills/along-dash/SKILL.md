---
name: along-dash
description: Launch the Along executive dashboard, inspect entity DAG dependency graph, print terminal analytics, or export static/markdown reports. Use when the user requests a dashboard, status overview, repository metrics, or invokes /along-dash.
---

# Along Dashboard & Executive Analytics (`/along-dash`) [v2.0.7]

Inspect, visualize, and analyze repository status across all `.along/` entities (`ISSUES`, `MILESTONES`, `RISKS`, `SPIKES`, `CHECKLISTS`, `SESSIONS`, `KB`, and ADR decisions).

---

## When to Use

1. The user asks for a dashboard, status report, project analytics, or DAG dependency graph (e.g., "покажи дашборд", "запусти дашборд", "generate repo report", `/along-dash`).
2. Reviewing milestone progress, active blockers, risk mitigation status, and completed accomplishments.
3. Generating `.along/DASHBOARD.md` or standalone `.along/dashboard.html` for stakeholder reviews.

---

## Resolving `along_dash.py` Engine Path

Agents MUST resolve the path to `along_dash.py` using this precedence:
1. **Local repository script**: `./scripts/along_dash.py` (if working inside the `along` codebase).
2. **Local workspace skill**: `./skills/along-dash/along_dash.py` (if present in repo).
3. **Global skill installation**:
   - Antigravity: `~/.gemini/config/skills/along-dash/along_dash.py`
   - Claude Code: `~/.claude/skills/along-dash/along_dash.py`
   - Codex: `~/.codex/skills/along-dash/along_dash.py`
   - OpenCode: `~/.config/opencode/actdim-along/along_dash.py`

---

## Standard Agent Workflow for `/along-dash`

When `/along-dash` is invoked (or the user asks for the dashboard), agents MUST:

1. **Execute CLI Mode & Recalculate Metrics**:
   Run `python <path-to-along_dash.py> . --cli` (or `uv run <path-to-along_dash.py> . --cli`).
   This recalculates metrics, prints the terminal summary, and automatically refreshes [`.along/dashboard.html`](file://.along/dashboard.html) and [`.along/DASHBOARD.md`](file://.along/DASHBOARD.md).

2. **Present Executive Summary & Backlog in Chat**:
   Directly output the key statistics table and active issues list in the chat response.

3. **Launch the Live Web Dashboard in Background**:
   Start the interactive FastAPI web server as a background daemon task (`run_command` with `IsDaemon: true`):
   ```bash
   uv run --with fastapi --with uvicorn --with jinja2 --with pyyaml --with rich <path-to-along_dash.py> . --web --no-browser
   ```

4. **Provide Direct Clickable Links & Controls**:
   - **Live Interactive Dashboard**: [**http://127.0.0.1:8765**](http://127.0.0.1:8765) (Cytoscape DAG graph, real-time node previews).
   - **Static HTML File**: [`.along/dashboard.html`](file://.along/dashboard.html) (Single-file standalone report).
   - **Markdown Report**: [`.along/DASHBOARD.md`](file://.along/DASHBOARD.md) (Mermaid diagrams).
   - **Server Control**: Clearly state that the web server is actively running in the background, and the user can stop it at any time by asking *"останови дашборд"* / *"stop dashboard"*, or pressing `Ctrl+C` if running in terminal.


---

## Execution Modes

### Mode 1: Terminal Summary (CLI - Instant & Auto-Export)
```bash
python <path-to-along_dash.py> . --cli
```

### Mode 2: Interactive Local Web Dashboard (FastAPI + Cytoscape DAG)
```bash
uv run <path-to-along_dash.py> . --web
```
- Serves live DAG graph at `http://127.0.0.1:8765`.
- Press `Ctrl+C` or kill process to stop.

### Mode 3: Standalone Static HTML Report
```bash
python <path-to-along_dash.py> . --export .along/dashboard.html
```

### Mode 4: Markdown Dashboard Report
```bash
python <path-to-along_dash.py> . --markdown
```

