---
name: repo-dashboard
version: "1.5.7"
description: Launch the repository executive dashboard, inspect entity DAG dependency graph, print terminal analytics, or export static/markdown reports. Use when the user requests a dashboard, status overview, repository metrics, or invokes /repo-dashboard.
---

# Repository Dashboard & Executive Analytics (`/repo-dashboard`) [v1.5.7]

Inspect, visualize, and analyze repository status across all `.agents/` entities (`ISSUES`, `MILESTONES`, `RISKS`, `SPIKES`, `CHECKLISTS`, `SESSIONS`, `KB`, and ADR decisions).

---

## 🎯 When to Use

1. The user asks for a dashboard, status report, project analytics, or DAG dependency graph (e.g., "покажи дашборд", "запусти дашборд", "generate repo report", `/repo-dashboard`, `/dashboard`).
2. Reviewing milestone progress, active blockers, risk mitigation status, and completed accomplishments.
3. Generating `.agents/DASHBOARD.md` or standalone `.agents/dashboard.html` for stakeholder reviews.

---

## 🛠️ Execution Modes

### Mode 1: Terminal Summary (CLI - Fast & Lightweight)
Print a structured summary with Rich tables and priority breakdowns directly in the terminal:
```bash
uv run scripts/dashboard.py --cli
```
*(Or `python scripts/dashboard.py --cli`)*

---

### Mode 2: Interactive Local Web Dashboard (FastAPI + Cytoscape DAG)
Launch the interactive web UI with real-time entity search, status filters, markdown preview drawer, and visual dependency graph:
```bash
uv run scripts/dashboard.py --web
```
- Opens `http://127.0.0.1:8765` in the default browser.
- Displays interactive DAG graph showing blockers (`blocked_by`), relationships (`related`), and milestones.
- Live data refresh endpoint (`/api/refresh`).

---

### Mode 3: Standalone Static HTML Report (Zero Server Overhead)
Export a portable, self-contained single HTML report with embedded JSON and client-side filtering:
```bash
uv run scripts/dashboard.py --export .agents/dashboard.html
```

---

### Mode 4: Markdown Dashboard Report (`.agents/DASHBOARD.md`)
Generate or update the repository's `.agents/DASHBOARD.md` containing Mermaid status charts, active issue tables, and file links:
```bash
uv run scripts/dashboard.py --markdown
```

