---
name: along-dash
description: Launch the Along executive dashboard, inspect entity DAG dependency graph, print terminal analytics, or export static/markdown reports. Use when the user requests a dashboard, status overview, repository metrics, or invokes /along-dash.
---

# Along Dashboard & Executive Analytics (`/along-dash`) [v2.0.6]

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

When `/along-dash` is invoked, agents MUST:

1. **Execute CLI Mode First**:
   Run `python <path-to-along_dash.py> . --cli` (or `uv run <path-to-along_dash.py> . --cli`).
   This prints the terminal summary and automatically generates fresh [`.along/dashboard.html`](file://.along/dashboard.html) and [`.along/DASHBOARD.md`](file://.along/DASHBOARD.md).

2. **Present Executive Summary in Chat**:
   Directly output the key statistics table to the user:
   - Total Issues & Completion Percentage (Done / Open / In-Progress / Blocked)
   - Milestones & Sprints progress
   - Active Risks / Blockers
   - Sessions & ADR Decisions recorded
   - KB articles count & Context hygiene (< 20 lines)

3. **Provide Direct File Links**:
   - [`.along/dashboard.html`](file://.along/dashboard.html) - Standalone interactive HTML report.
   - [`.along/DASHBOARD.md`](file://.along/DASHBOARD.md) - Markdown summary with Mermaid graphs.

4. **Provide Interactive Web Server Controls**:
   - **Launch Web Dashboard**:
     If the user asked to run/launch the web server, run it as a background task:
     ```bash
     uv run <path-to-along_dash.py> . --web
     ```
     Provide the clickable URL: `http://127.0.0.1:8765`.
   - **Stop Web Dashboard**:
     - Terminal: `Ctrl+C`
     - Background task: Stop via task manager or terminate process on port 8765:
       - PowerShell: `Get-NetTCPConnection -LocalPort 8765 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }`
       - Bash: `fuser -k 8765/tcp || lsof -ti :8765 | xargs kill -9`

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

