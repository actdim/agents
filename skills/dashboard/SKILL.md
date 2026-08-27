---
name: dashboard
version: "1.5.7"
description: Launch the repository executive dashboard, inspect entity DAG dependency graph, print terminal analytics, or export static/markdown reports. (Alias for /repo-dashboard).
---

# Dashboard (`/dashboard`) [v1.5.7]

Convenient alias for [`repo-dashboard`](../repo-dashboard/SKILL.md).

---

## 🎯 When to Use

Use when the user invokes `/dashboard`, asks to view the project dashboard, or inspect DAG dependencies.

---

## 🛠️ Quick Commands

- **Terminal Summary**: `uv run scripts/dashboard.py --cli`
- **Interactive Web UI**: `uv run scripts/dashboard.py --web`
- **Static HTML Export**: `uv run scripts/dashboard.py --export .agents/dashboard.html`
- **Markdown Report**: `uv run scripts/dashboard.py --markdown`

