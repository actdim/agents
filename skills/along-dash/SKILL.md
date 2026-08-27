---
name: along-dash
description: Launch the Along executive dashboard, inspect entity DAG dependency graph, print terminal analytics, or export static/markdown reports. Use when the user requests a dashboard, status overview, repository metrics, or invokes /along-dash.
---

# Along Dashboard & Executive Analytics (`/along-dash`) [v2.0.5]

Inspect, visualize, and analyze repository status across all `.along/` entities (`ISSUES`, `MILESTONES`, `RISKS`, `SPIKES`, `CHECKLISTS`, `SESSIONS`, `KB`, and ADR decisions).

---

## When to Use

1. The user asks for a dashboard, status report, project analytics, or DAG dependency graph (e.g., "покажи дашборд", "запусти дашборд", "generate repo report", `/along-dash`).
2. Reviewing milestone progress, active blockers, risk mitigation status, and completed accomplishments.
3. Generating `.along/DASHBOARD.md` or standalone `.along/dashboard.html` for stakeholder reviews.

---

## Execution Modes

### Mode 1: Terminal Summary (CLI - Fast & Lightweight)
Print a structured summary with Rich tables and priority breakdowns directly in the terminal:
```bash
uv run scripts/along_dash.py --cli
```
*(Or `python scripts/along_dash.py --cli`)*

```text
+-------------------------------------------------------------------+
| Along Dashboard (along)                                           |
| Scanned 2026-08-27 20:41:45 | Root: D:\Src\my\actdim\public\along |
+-------------------------------------------------------------------+
                        Executive Summary                         
+----------------------------------------------------------------+
| Metric               |   Value | Details                       |
|----------------------+---------+-------------------------------|
| Total Issues         |      18 | Done: 14 (77.8%)              |
| In-Progress / Open   |   0 / 4 | Active backlog                |
| Blocked Issues       |       0 | None                          |
| Active Risks         |       0 | Critical/High: 0              |
| Milestones & Sprints |       4 | Tracked targets               |
| Sessions & ADRs      |   8 / 7 | Recorded progress             |
| KB Articles          |       4 | Knowledge base docs           |
| Context Hygiene      | 9 lines | CONTEXT.md (<20 lines target) |
+----------------------------------------------------------------+
```

---

### Mode 2: Interactive Local Web Dashboard (FastAPI + Cytoscape DAG)
Launch the interactive web UI with real-time entity search, status filters, markdown preview drawer, and visual dependency graph:
```bash
uv run scripts/along_dash.py --web
```
- Opens `http://127.0.0.1:8765` in the default browser.
- Displays interactive DAG graph showing blockers (`blocked_by`), relationships (`related`), and milestones.
- Live data refresh endpoint (`/api/refresh`).

---

### Mode 3: Standalone Static HTML Report (Zero Server Overhead)
Export a portable, self-contained single HTML report with embedded JSON and client-side filtering:
```bash
uv run scripts/along_dash.py --export .along/dashboard.html
```

---

### Mode 4: Markdown Dashboard Report (`.along/DASHBOARD.md`)
Generate or update the repository's `.along/DASHBOARD.md` containing Mermaid status charts, active issue tables, and file links:
```bash
uv run scripts/along_dash.py --markdown
```
