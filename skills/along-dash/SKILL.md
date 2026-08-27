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

## Standard Agent Workflow for `/along-dash`

When `/along-dash` is invoked, agents MUST:
1. Run `python scripts/along_dash.py --cli` (which automatically recalculates metrics, updates `.along/DASHBOARD.md`, and exports `.along/dashboard.html`).
2. Present the Executive Summary and Active Issues tables in the chat response.
3. Provide clickable file links to [`.along/DASHBOARD.md`](file://.along/DASHBOARD.md) and [`.along/dashboard.html`](file://.along/dashboard.html).
4. Provide the exact command to launch the live interactive Cytoscape web server:
   ```bash
   uv run --with fastapi --with uvicorn scripts/along_dash.py --web
   ```

---

## Execution Modes

### Mode 1: Terminal Summary (CLI - Fast & Lightweight)
Print a structured summary with Rich tables and priority breakdowns directly in the terminal:
### Mode 1: Terminal Summary (CLI - Default & Fast)
```bash
python scripts/along_dash.py --cli
```
*(Or `uv run scripts/along_dash.py --cli`)*

---

### Mode 2: Interactive Local Web Dashboard (FastAPI + Cytoscape DAG)
Launch the interactive web UI with real-time entity search, status filters, markdown preview drawer, and visual dependency graph:
```bash
uv run --with fastapi --with uvicorn scripts/along_dash.py --web
```
*(Or `python scripts/along_dash.py --web`)*
- Automatically refreshes `.along/DASHBOARD.md` and exports `.along/dashboard.html`.
- Opens `http://127.0.0.1:8765` in the default browser.
- Displays interactive DAG graph showing blockers (`blocked_by`), relationships (`related`), and milestones.
- Live data refresh endpoint (`/api/refresh`).
- Automatically serves at `http://127.0.0.1:8765`.
- Interactive Cytoscape DAG graph with real-time entity preview.

---

### Mode 3: Standalone Static HTML Report (Zero Server Overhead)
Export a portable, self-contained single HTML report with embedded JSON and client-side filtering:
### Mode 3: Standalone Static HTML Report
```bash
uv run scripts/along_dash.py --export .along/dashboard.html
python scripts/along_dash.py --export .along/dashboard.html
```

---

### Mode 4: Markdown Dashboard Report (`.along/DASHBOARD.md`)
Generate or update the repository's `.along/DASHBOARD.md` containing Mermaid status charts, active issue tables, and file links:
### Mode 4: Markdown Dashboard Report
```bash
uv run scripts/along_dash.py --markdown
python scripts/along_dash.py --markdown
```
