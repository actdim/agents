# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "fastapi>=0.110.0",
#     "uvicorn>=0.28.0",
#     "jinja2>=3.1.0",
#     "pyyaml>=6.0.0",
#     "rich>=13.0.0",
# ]
# ///

"""
Along Dashboard & Analytics Engine.

High-performance FastAPI & Uvicorn dashboard with PEP 723 metadata for instant execution via uv:
- CLI mode: Rich terminal summary tables and metrics.
- Web mode: FastAPI & Uvicorn asynchronous local server with Cytoscape DAG and real-time refresh.
- Static export mode: Standalone single-file HTML report.
- Markdown report mode: Updates .along/DASHBOARD.md with Mermaid diagrams.
"""

import os
import sys
import re
import json
import argparse
import webbrowser
from datetime import datetime
from pathlib import Path

# External dependencies (FastAPI, Uvicorn, Jinja2, PyYAML, Rich)
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

try:
    from jinja2 import Template
    HAS_JINJA = True
except ImportError:
    HAS_JINJA = False

try:
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse, JSONResponse
    import uvicorn
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False


# ----------------------------------------------------------------------
# 1. Front-Matter & Entity Parsing
# ----------------------------------------------------------------------

def parse_frontmatter(content: str):
    """Extract YAML front-matter and markdown body from markdown content."""
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content
    fm_str, body = match.group(1), match.group(2)

    if HAS_YAML:
        try:
            data = yaml.safe_load(fm_str)
            if isinstance(data, dict):
                return data, body
        except Exception:
            pass

    # Fallback parser
    fm = {}
    for line in fm_str.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if val.startswith("[") and val.endswith("]"):
                items = [x.strip().strip("'").strip('"') for x in val[1:-1].split(",") if x.strip()]
                fm[key] = items
            elif val.lower() == "true":
                fm[key] = True
            elif val.lower() == "false":
                fm[key] = False
            elif val.lower() in ("null", "none", "~"):
                fm[key] = None
            else:
                fm[key] = val.strip("'").strip('"')
    return fm, body


def find_agents_dir(start_dir: str = ".") -> Path:
    """Find nearest .along (or fallback .agents) directory starting from start_dir and walking upwards."""
    current = Path(start_dir).resolve()
    while current != current.parent:
        candidate = current / ".along"
        if candidate.is_dir():
            return candidate
        legacy_candidate = current / ".agents"
        if legacy_candidate.is_dir():
            return legacy_candidate
        current = current.parent
    return Path(start_dir).resolve() / ".along"


class AgentEntityCollector:
    """Collects, parses, and resolves relationships for all entities in .agents/."""

    def __init__(self, agents_dir: Path):
        self.agents_dir = agents_dir
        self.repo_root = agents_dir.parent
        self.issues = []
        self.milestones = []
        self.risks = []
        self.spikes = []
        self.checklists = []
        self.sessions = []
        self.kb_articles = []
        self.decisions = []
        self.context_text = ""
        self.issues_board_text = ""
        self.history_text = ""
        self.graph = {"nodes": [], "edges": []}
        self.metrics = {}

    def collect_all(self):
        """Execute full scan and metric aggregation."""
        self.issues.clear()
        self.milestones.clear()
        self.risks.clear()
        self.spikes.clear()
        self.checklists.clear()
        self.sessions.clear()
        self.kb_articles.clear()
        self.decisions.clear()

        self._collect_issues()
        self._collect_milestones()
        self._collect_risks()
        self._collect_spikes()
        self._collect_checklists()
        self._collect_sessions()
        self._collect_kb()
        self._collect_decisions()
        self._collect_raw_files()
        self._build_graph()
        self._compute_metrics()
        return self

    def _collect_issues(self):
        issues_dir = self.agents_dir / "ISSUES"
        if not issues_dir.exists():
            return

        files = list(issues_dir.glob("*.md")) + list((issues_dir / "done").glob("*.md"))
        for p in files:
            try:
                content = p.read_text(encoding="utf-8")
                fm, body = parse_frontmatter(content)
                is_done = "done" in p.parts
                slug = fm.get("slug") or p.stem.split("--")[-1]
                issue_type = fm.get("type") or (p.stem.split("--")[0] if "--" in p.stem else "feat")
                status = "done" if is_done else fm.get("status", "open")
                priority = fm.get("priority", "medium")

                title = fm.get("title")
                if not title:
                    title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
                    title = title_match.group(1) if title_match else slug.replace("-", " ").title()

                blocked_by = fm.get("blocked_by", [])
                if isinstance(blocked_by, str):
                    blocked_by = [blocked_by] if blocked_by else []

                related = fm.get("related", [])
                if isinstance(related, str):
                    related = [related] if related else []

                tags = fm.get("tags", [])
                if isinstance(tags, str):
                    tags = [tags] if tags else []

                self.issues.append({
                    "id": f"{issue_type}--{slug}",
                    "slug": slug,
                    "type": issue_type,
                    "title": title,
                    "status": status,
                    "priority": priority,
                    "created": str(fm.get("created", "")),
                    "updated": str(fm.get("updated", "")),
                    "completed": str(fm.get("completed", "")) if status == "done" else None,
                    "agent": fm.get("agent", "antigravity"),
                    "tags": tags,
                    "milestone": fm.get("milestone"),
                    "parent": fm.get("parent"),
                    "blocked_by": blocked_by,
                    "related": related,
                    "file_path": str(p.relative_to(self.repo_root)).replace("\\", "/"),
                    "is_done": is_done,
                    "body": body.strip()
                })
            except Exception as e:
                print(f"[Warning] Failed parsing issue {p}: {e}", file=sys.stderr)

    def _collect_milestones(self):
        m_dir = self.agents_dir / "MILESTONES"
        if not m_dir.exists():
            return

        for p in m_dir.glob("*.md"):
            try:
                content = p.read_text(encoding="utf-8")
                fm, body = parse_frontmatter(content)
                slug = fm.get("slug") or p.stem
                title = fm.get("title") or slug.replace("-", " ").title()
                status = fm.get("status", "open")
                target_issues = fm.get("target_issues", [])
                if isinstance(target_issues, str):
                    target_issues = [target_issues] if target_issues else []

                self.milestones.append({
                    "id": f"milestone--{slug}",
                    "slug": slug,
                    "title": title,
                    "status": status,
                    "due_date": str(fm.get("due_date", "")),
                    "created": str(fm.get("created", "")),
                    "target_issues": target_issues,
                    "progress_pct": fm.get("progress_pct", 0),
                    "file_path": str(p.relative_to(self.repo_root)).replace("\\", "/"),
                    "body": body.strip()
                })
            except Exception as e:
                print(f"[Warning] Failed parsing milestone {p}: {e}", file=sys.stderr)

    def _collect_risks(self):
        r_dir = self.agents_dir / "RISKS"
        if not r_dir.exists():
            return

        for p in r_dir.glob("*.md"):
            try:
                content = p.read_text(encoding="utf-8")
                fm, body = parse_frontmatter(content)
                slug = fm.get("slug") or p.stem
                title = fm.get("title") or slug.replace("-", " ").title()
                severity = fm.get("severity", "medium")
                status = fm.get("status", "active")

                self.risks.append({
                    "id": f"risk--{slug}",
                    "slug": slug,
                    "title": title,
                    "severity": severity,
                    "status": status,
                    "owner": fm.get("owner", "agent"),
                    "mitigation": fm.get("mitigation", ""),
                    "created": str(fm.get("created", "")),
                    "updated": str(fm.get("updated", "")),
                    "file_path": str(p.relative_to(self.repo_root)).replace("\\", "/"),
                    "body": body.strip()
                })
            except Exception as e:
                print(f"[Warning] Failed parsing risk {p}: {e}", file=sys.stderr)

    def _collect_spikes(self):
        s_dir = self.agents_dir / "SPIKES"
        if not s_dir.exists():
            return

        for p in s_dir.glob("*.md"):
            try:
                content = p.read_text(encoding="utf-8")
                fm, body = parse_frontmatter(content)
                slug = fm.get("slug") or p.stem
                title = fm.get("title") or slug.replace("-", " ").title()

                self.spikes.append({
                    "id": f"spike--{slug}",
                    "slug": slug,
                    "title": title,
                    "status": fm.get("status", "hypothesis"),
                    "hypothesis": fm.get("hypothesis", ""),
                    "outcome": fm.get("outcome", ""),
                    "resulting_adr": fm.get("resulting_adr"),
                    "created": str(fm.get("created", "")),
                    "file_path": str(p.relative_to(self.repo_root)).replace("\\", "/"),
                    "body": body.strip()
                })
            except Exception as e:
                print(f"[Warning] Failed parsing spike {p}: {e}", file=sys.stderr)

    def _collect_checklists(self):
        c_dir = self.agents_dir / "CHECKLISTS"
        if not c_dir.exists():
            return

        for p in c_dir.glob("*.md"):
            try:
                content = p.read_text(encoding="utf-8")
                fm, body = parse_frontmatter(content)
                slug = fm.get("slug") or p.stem
                title = fm.get("title") or slug.replace("-", " ").title()

                self.checklists.append({
                    "id": f"checklist--{slug}",
                    "slug": slug,
                    "title": title,
                    "category": fm.get("category", "general"),
                    "items": fm.get("items", []),
                    "file_path": str(p.relative_to(self.repo_root)).replace("\\", "/"),
                    "body": body.strip()
                })
            except Exception as e:
                print(f"[Warning] Failed parsing checklist {p}: {e}", file=sys.stderr)

    def _collect_sessions(self):
        sess_dir = self.agents_dir / "SESSIONS"
        if not sess_dir.exists():
            return

        for p in sess_dir.glob("**/*.md"):
            try:
                content = p.read_text(encoding="utf-8")
                fm, body = parse_frontmatter(content)
                slug = fm.get("slug") or p.stem

                self.sessions.append({
                    "id": f"session--{p.stem}",
                    "slug": slug,
                    "date": str(fm.get("date", p.stem.split("--")[0])),
                    "agent": fm.get("agent", "antigravity"),
                    "branch": fm.get("branch", "main"),
                    "commit": fm.get("commit", ""),
                    "summary": fm.get("summary", ""),
                    "issues_advanced": fm.get("issues_advanced", []),
                    "issues_completed": fm.get("issues_completed", []),
                    "decisions": fm.get("decisions", []),
                    "file_path": str(p.relative_to(self.repo_root)).replace("\\", "/"),
                    "body": body.strip()
                })
            except Exception as e:
                print(f"[Warning] Failed parsing session {p}: {e}", file=sys.stderr)
        self.sessions.sort(key=lambda s: s["date"], reverse=True)

    def _collect_kb(self):
        kb_dir = self.agents_dir / "KB"
        if not kb_dir.exists():
            return

        for p in kb_dir.glob("*.md"):
            try:
                content = p.read_text(encoding="utf-8")
                fm, body = parse_frontmatter(content)
                slug = fm.get("slug") or p.stem
                title = fm.get("title") or slug.replace("-", " ").title()

                self.kb_articles.append({
                    "id": f"kb--{slug}",
                    "slug": slug,
                    "title": title,
                    "type": fm.get("type", "topic"),
                    "created": str(fm.get("created", "")),
                    "updated": str(fm.get("updated", "")),
                    "tags": fm.get("tags", []),
                    "file_path": str(p.relative_to(self.repo_root)).replace("\\", "/"),
                    "body": body.strip()
                })
            except Exception as e:
                print(f"[Warning] Failed parsing KB article {p}: {e}", file=sys.stderr)

    def _collect_decisions(self):
        dec_file = self.agents_dir / "DECISIONS.md"
        if not dec_file.exists():
            return

        try:
            content = dec_file.read_text(encoding="utf-8")
            sections = re.split(r"\n(?=##\s+)", content)
            for idx, sec in enumerate(sections):
                if not sec.strip().startswith("##"):
                    continue
                header_line = sec.strip().splitlines()[0]
                title = header_line.lstrip("#").strip()
                self.decisions.append({
                    "id": f"adr--{idx+1}",
                    "title": title,
                    "content": sec.strip()
                })
        except Exception as e:
            print(f"[Warning] Failed parsing DECISIONS.md: {e}", file=sys.stderr)

    def _collect_raw_files(self):
        for name in ["CONTEXT.md", "ISSUES.md", "HISTORY.md"]:
            p = self.agents_dir / name
            if p.exists():
                try:
                    text = p.read_text(encoding="utf-8")
                    if name == "CONTEXT.md":
                        self.context_text = text
                    elif name == "ISSUES.md":
                        self.issues_board_text = text
                    elif name == "HISTORY.md":
                        self.history_text = text
                except Exception:
                    pass

    def _build_graph(self):
        nodes = []
        edges = []

        for iss in self.issues:
            nodes.append({
                "id": iss["id"],
                "label": iss["title"],
                "type": "issue",
                "status": iss["status"],
                "priority": iss["priority"],
                "issue_type": iss["type"]
            })

        for m in self.milestones:
            nodes.append({
                "id": m["id"],
                "label": m["title"],
                "type": "milestone",
                "status": m["status"],
                "progress_pct": m["progress_pct"]
            })

        for r in self.risks:
            nodes.append({
                "id": r["id"],
                "label": r["title"],
                "type": "risk",
                "severity": r["severity"],
                "status": r["status"]
            })

        for iss in self.issues:
            src = iss["id"]
            for blocker in iss.get("blocked_by", []):
                target = blocker if blocker.startswith(("feat--", "bug--", "debt--", "task--", "docs--")) else f"feat--{blocker}"
                edges.append({"source": target, "target": src, "type": "blocks", "label": "blocks"})
            for rel in iss.get("related", []):
                target = rel if rel.startswith(("feat--", "bug--", "debt--", "task--", "docs--", "risk--")) else f"feat--{rel}"
                edges.append({"source": src, "target": target, "type": "related", "label": "related"})
            if iss.get("milestone"):
                edges.append({"source": src, "target": f"milestone--{iss['milestone']}", "type": "belongs_to", "label": "part of"})
            if iss.get("parent"):
                edges.append({"source": src, "target": iss["parent"], "type": "child_of", "label": "child of"})

        self.graph = {"nodes": nodes, "edges": edges}

    def _compute_metrics(self):
        total_issues = len(self.issues)
        done_issues = sum(1 for i in self.issues if i["status"] == "done")
        open_issues = sum(1 for i in self.issues if i["status"] == "open")
        inprogress_issues = sum(1 for i in self.issues if i["status"] == "in-progress")
        blocked_issues = sum(1 for i in self.issues if i["status"] == "blocked")
        completion_pct = round((done_issues / total_issues * 100), 1) if total_issues > 0 else 0.0

        type_dist = {}
        for i in self.issues:
            t = i["type"]
            type_dist[t] = type_dist.get(t, 0) + 1

        prio_dist = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for i in self.issues:
            p = i.get("priority", "medium")
            prio_dist[p] = prio_dist.get(p, 0) + 1

        active_risks = [r for r in self.risks if r["status"] == "active"]
        critical_risks = sum(1 for r in active_risks if r["severity"] in ("critical", "high"))

        self.metrics = {
            "total_issues": total_issues,
            "done_issues": done_issues,
            "open_issues": open_issues,
            "inprogress_issues": inprogress_issues,
            "blocked_issues": blocked_issues,
            "completion_pct": completion_pct,
            "type_distribution": type_dist,
            "priority_distribution": prio_dist,
            "total_milestones": len(self.milestones),
            "active_risks_count": len(active_risks),
            "critical_risks_count": critical_risks,
            "total_spikes": len(self.spikes),
            "total_sessions": len(self.sessions),
            "total_kb_articles": len(self.kb_articles),
            "total_decisions": len(self.decisions),
            "context_lines": len(self.context_text.splitlines()),
            "issues_board_lines": len(self.issues_board_text.splitlines()),
            "scan_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def to_dict(self):
        return {
            "metrics": self.metrics,
            "issues": self.issues,
            "milestones": self.milestones,
            "risks": self.risks,
            "spikes": self.spikes,
            "checklists": self.checklists,
            "sessions": self.sessions,
            "kb_articles": self.kb_articles,
            "decisions": self.decisions,
            "context_text": self.context_text,
            "issues_board_text": self.issues_board_text,
            "history_text": self.history_text,
            "graph": self.graph,
            "repo_name": self.repo_root.name,
            "repo_path": str(self.repo_root)
        }


# ----------------------------------------------------------------------
# 2. CLI Renderer (Rich / Plain)
# ----------------------------------------------------------------------

def render_cli(collector: AgentEntityCollector):
    m = collector.metrics
    if HAS_RICH:
        console = Console()
        console.print()
        console.print(Panel(
            f"[bold cyan]Along Dashboard[/bold cyan] [dim]({collector.repo_root.name})[/dim]\n"
            f"[dim]Scanned {m['scan_timestamp']} | Root: {collector.repo_root}[/dim]",
            expand=False,
            border_style="cyan"
        ))

        summary_table = Table(title="Executive Summary", show_header=True, header_style="bold magenta")
        summary_table.add_column("Metric", style="dim")
        summary_table.add_column("Value", justify="right", style="bold")
        summary_table.add_column("Details", style="italic")

        summary_table.add_row("Total Issues", str(m["total_issues"]), f"Done: {m['done_issues']} ({m['completion_pct']}%)")
        summary_table.add_row("In-Progress / Open", f"{m['inprogress_issues']} / {m['open_issues']}", "Active backlog")
        summary_table.add_row("Blocked Issues", str(m["blocked_issues"]), "Requires unblocking" if m["blocked_issues"] else "None")
        summary_table.add_row("Active Risks", str(m["active_risks_count"]), f"Critical/High: {m['critical_risks_count']}")
        summary_table.add_row("Milestones & Sprints", str(m["total_milestones"]), "Tracked targets")
        summary_table.add_row("Sessions & ADRs", f"{m['total_sessions']} / {m['total_decisions']}", "Recorded progress")
        summary_table.add_row("KB Articles", str(m["total_kb_articles"]), "Knowledge base docs")
        summary_table.add_row("Context Hygiene", f"{m['context_lines']} lines", "CONTEXT.md (<20 lines target)")

        console.print(summary_table)

        active_issues = [i for i in collector.issues if i["status"] in ("in-progress", "open", "blocked")]
        if active_issues:
            issues_table = Table(title="Active Issues & Tasks", show_header=True, header_style="bold blue")
            issues_table.add_column("Status", width=12)
            issues_table.add_column("Type", width=8)
            issues_table.add_column("Priority", width=10)
            issues_table.add_column("Slug / Title", style="cyan")
            issues_table.add_column("Milestone / Blocked By", style="dim")

            for iss in active_issues[:15]:
                status_style = {
                    "in-progress": "[yellow]in-progress[/yellow]",
                    "open": "[white]open[/white]",
                    "blocked": "[bold red]blocked[/bold red]"
                }.get(iss["status"], iss["status"])

                prio_style = {
                    "critical": "[bold red]critical[/bold red]",
                    "high": "[red]high[/red]",
                    "medium": "[yellow]medium[/yellow]",
                    "low": "[green]low[/green]"
                }.get(iss["priority"], iss["priority"])

                blockers = ", ".join(iss.get("blocked_by", []))
                meta = iss.get("milestone") or ""
                if blockers:
                    meta += f" (Blocked by: {blockers})"

                issues_table.add_row(status_style, iss["type"], prio_style, iss["title"], meta)

            console.print(issues_table)
        console.print()
    else:
        print("=" * 70)
        print(f"Along Dashboard ({collector.repo_root.name})")
        print(f"Scanned: {m['scan_timestamp']} | Root: {collector.repo_root}")
        print("=" * 70)
        print(f"Total Issues:      {m['total_issues']} (Done: {m['done_issues']} / {m['completion_pct']}%)")
        print(f"In-Progress/Open:  {m['inprogress_issues']} / {m['open_issues']}")
        print(f"Blocked Issues:    {m['blocked_issues']}")
        print(f"Active Risks:      {m['active_risks_count']} (Critical/High: {m['critical_risks_count']})")
        print(f"Milestones:        {m['total_milestones']}")
        print(f"Sessions Logged:   {m['total_sessions']}")
        print(f"ADR Decisions:     {m['total_decisions']}")
        print(f"KB Articles:       {m['total_kb_articles']}")
        print(f"CONTEXT.md Lines:  {m['context_lines']}")
        print("-" * 70)


# ----------------------------------------------------------------------
# 3. Markdown Report Generator (.along/DASHBOARD.md)
# ----------------------------------------------------------------------

def generate_markdown_report(collector: AgentEntityCollector, output_path: Path):
    m = collector.metrics
    lines = []
    lines.append("# Along Executive Dashboard & Repository Analytics")
    lines.append("")
    lines.append(f"> Auto-generated on `{m['scan_timestamp']}` for repository `{collector.repo_root.name}`.")
    lines.append("")
    lines.append("## 1. Executive Summary")
    lines.append("")
    lines.append("| Metric | Value | Details |")
    lines.append("| :--- | :--- | :--- |")
    lines.append(f"| **Completion Progress** | `{m['completion_pct']}%` | `{m['done_issues']}` done / `{m['total_issues']}` total |")
    lines.append(f"| **Active Backlog** | `{m['open_issues']}` open, `{m['inprogress_issues']}` in-progress | `{m['blocked_issues']}` blocked |")
    lines.append(f"| **Active Risks** | `{m['active_risks_count']}` active | `{m['critical_risks_count']}` critical/high |")
    lines.append(f"| **Milestones Tracked** | `{m['total_milestones']}` | Stage releases |")
    lines.append(f"| **Session Logs / ADRs** | `{m['total_sessions']}` sessions / `{m['total_decisions']}` ADRs | Architectural record |")
    lines.append(f"| **Knowledge Base** | `{m['total_kb_articles']}` articles | `.along/KB/` documentation |")
    lines.append(f"| **Context Footprint** | `{m['context_lines']}` lines | `.along/CONTEXT.md` |")
    lines.append("")

    if m["total_issues"] > 0:
        lines.append("## 2. Issues Breakdown")
        lines.append("")
        lines.append("```mermaid")
        lines.append("pie title Issues Status Breakdown")
        if m["done_issues"]:
            lines.append(f'    "Done" : {m["done_issues"]}')
        if m["inprogress_issues"]:
            lines.append(f'    "In Progress" : {m["inprogress_issues"]}')
        if m["open_issues"]:
            lines.append(f'    "Open" : {m["open_issues"]}')
        if m["blocked_issues"]:
            lines.append(f'    "Blocked" : {m["blocked_issues"]}')
        lines.append("```")
        lines.append("")

    active_issues = [i for i in collector.issues if i["status"] in ("in-progress", "open", "blocked")]
    if active_issues:
        lines.append("## 3. Active Issues & Backlog")
        lines.append("")
        lines.append("| Status | Type | Priority | Issue | Milestone / Blockers |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for iss in active_issues:
            slug_link = f"[{iss['title']}](file:///{iss['file_path']})"
            blockers = ", ".join(iss.get("blocked_by", []))
            meta = iss.get("milestone") or ""
            if blockers:
                meta += f" (Blocked by: `{blockers}`)"
            lines.append(f"| `{iss['status']}` | `{iss['type']}` | `{iss['priority']}` | {slug_link} | {meta} |")
        lines.append("")

    active_risks = [r for r in collector.risks if r["status"] == "active"]
    if active_risks:
        lines.append("## 4. Active Risks & Blockers")
        lines.append("")
        lines.append("| Severity | Risk Title | Owner | Mitigation Plan |")
        lines.append("| :--- | :--- | :--- | :--- |")
        for r in active_risks:
            r_link = f"[{r['title']}](file:///{r['file_path']})"
            lines.append(f"| `{r['severity']}` | {r_link} | `{r['owner']}` | {r.get('mitigation', '-')} |")
        lines.append("")

    if collector.milestones:
        lines.append("## 5. Milestones & Sprints")
        lines.append("")
        lines.append("| Milestone | Status | Due Date | Progress |")
        lines.append("| :--- | :--- | :--- | :--- |")
        for ms in collector.milestones:
            ms_link = f"[{ms['title']}](file:///{ms['file_path']})"
            lines.append(f"| {ms_link} | `{ms['status']}` | `{ms.get('due_date', '-')}` | `{ms.get('progress_pct', 0)}%` |")
        lines.append("")

    content = "\n".join(lines) + "\n"
    output_path.write_text(content, encoding="utf-8")
    print(f"-> Markdown dashboard generated: {output_path}")


# ----------------------------------------------------------------------
# 4. Web UI Template & Static HTML Generator
# ----------------------------------------------------------------------

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Along Dashboard - {{ repo_name }}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: { 50: '#f0f9ff', 500: '#0284c7', 600: '#0369a1', 900: '#0c4a6e' }
          }
        }
      }
    }
  </script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.28.1/cytoscape.min.js"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    #cy { width: 100%; height: 550px; background-color: #0f172a; border-radius: 0.75rem; }
    .tab-btn.active { border-bottom: 2px solid #38bdf8; color: #38bdf8; font-weight: 600; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans antialiased">

  <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-30 px-6 py-4 flex items-center justify-between">
    <div class="flex items-center space-x-3">
      <div class="w-8 h-8 rounded-lg bg-sky-600 flex items-center justify-center font-bold text-white shadow-lg shadow-sky-600/30">A</div>
      <div>
        <h1 class="text-lg font-bold text-slate-100 flex items-center gap-2">
          Along Dashboard
          <span class="text-xs px-2 py-0.5 rounded-full bg-sky-950 text-sky-400 border border-sky-800 font-mono">{{ repo_name }}</span>
        </h1>
        <p class="text-xs text-slate-400">Protocol v2.0.1 | Last scanned: <span id="scan-time">{{ metrics.scan_timestamp }}</span></p>
      </div>
    </div>
    <div class="flex items-center space-x-3">
      {% if is_live %}
      <button onclick="refreshData()" class="px-3 py-1.5 text-xs bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-md flex items-center gap-1.5 transition">
        <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i> Refresh
      </button>
      {% endif %}
      <span class="text-xs px-2.5 py-1 bg-emerald-950 text-emerald-400 border border-emerald-800 rounded-md flex items-center gap-1">
        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> {{ metrics.completion_pct }}% Complete
      </span>
    </div>
  </header>

  <nav class="border-b border-slate-800 bg-slate-900/40 px-6 flex space-x-6 text-sm overflow-x-auto">
    <button onclick="switchTab('overview')" id="tab-overview" class="tab-btn active py-3 flex items-center gap-2 text-slate-400 hover:text-slate-200">
      <i data-lucide="layout-dashboard" class="w-4 h-4"></i> Overview
    </button>
    <button onclick="switchTab('issues')" id="tab-issues" class="tab-btn py-3 flex items-center gap-2 text-slate-400 hover:text-slate-200">
      <i data-lucide="check-square" class="w-4 h-4"></i> Issues ({{ metrics.total_issues }})
    </button>
    <button onclick="switchTab('graph')" id="tab-graph" class="tab-btn py-3 flex items-center gap-2 text-slate-400 hover:text-slate-200">
      <i data-lucide="git-fork" class="w-4 h-4"></i> Dependency Graph (DAG)
    </button>
    <button onclick="switchTab('milestones')" id="tab-milestones" class="tab-btn py-3 flex items-center gap-2 text-slate-400 hover:text-slate-200">
      <i data-lucide="flag" class="w-4 h-4"></i> Milestones ({{ metrics.total_milestones }})
    </button>
    <button onclick="switchTab('risks')" id="tab-risks" class="tab-btn py-3 flex items-center gap-2 text-slate-400 hover:text-slate-200">
      <i data-lucide="alert-triangle" class="w-4 h-4"></i> Risks & Blockers ({{ metrics.active_risks_count }})
    </button>
    <button onclick="switchTab('kb')" id="tab-kb" class="tab-btn py-3 flex items-center gap-2 text-slate-400 hover:text-slate-200">
      <i data-lucide="book-open" class="w-4 h-4"></i> Knowledge Base ({{ metrics.total_kb_articles }})
    </button>
    <button onclick="switchTab('sessions')" id="tab-sessions" class="tab-btn py-3 flex items-center gap-2 text-slate-400 hover:text-slate-200">
      <i data-lucide="history" class="w-4 h-4"></i> Sessions ({{ metrics.total_sessions }})
    </button>
  </nav>

  <main class="flex-1 p-6 max-w-7xl mx-auto w-full space-y-6">

    <!-- TAB: OVERVIEW -->
    <section id="content-overview" class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
          <div class="flex items-center justify-between">
            <span class="text-xs font-medium text-slate-400 uppercase tracking-wider">Completion</span>
            <i data-lucide="check-circle" class="w-4 h-4 text-emerald-400"></i>
          </div>
          <div class="text-2xl font-bold text-slate-100 mt-2">{{ metrics.completion_pct }}%</div>
          <div class="text-xs text-slate-400 mt-1">{{ metrics.done_issues }} done / {{ metrics.total_issues }} total issues</div>
          <div class="w-full bg-slate-800 h-1.5 rounded-full mt-3 overflow-hidden">
            <div class="bg-emerald-500 h-full rounded-full" style="width: {{ metrics.completion_pct }}%"></div>
          </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
          <div class="flex items-center justify-between">
            <span class="text-xs font-medium text-slate-400 uppercase tracking-wider">Active Backlog</span>
            <i data-lucide="clock" class="w-4 h-4 text-amber-400"></i>
          </div>
          <div class="text-2xl font-bold text-slate-100 mt-2">{{ metrics.inprogress_issues + metrics.open_issues }}</div>
          <div class="text-xs text-slate-400 mt-1">{{ metrics.inprogress_issues }} in-progress, {{ metrics.open_issues }} open</div>
          <div class="text-xs text-rose-400 mt-2 flex items-center gap-1">
            <i data-lucide="shield-alert" class="w-3 h-3"></i> {{ metrics.blocked_issues }} blocked issues
          </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
          <div class="flex items-center justify-between">
            <span class="text-xs font-medium text-slate-400 uppercase tracking-wider">Active Risks</span>
            <i data-lucide="alert-octagon" class="w-4 h-4 text-rose-400"></i>
          </div>
          <div class="text-2xl font-bold text-slate-100 mt-2">{{ metrics.active_risks_count }}</div>
          <div class="text-xs text-slate-400 mt-1">{{ metrics.critical_risks_count }} critical/high severity</div>
          <div class="text-xs text-slate-400 mt-2 flex items-center gap-1">
            <i data-lucide="shield-check" class="w-3 h-3 text-emerald-400"></i> Mitigations logged
          </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
          <div class="flex items-center justify-between">
            <span class="text-xs font-medium text-slate-400 uppercase tracking-wider">Repository Health</span>
            <i data-lucide="cpu" class="w-4 h-4 text-sky-400"></i>
          </div>
          <div class="text-2xl font-bold text-slate-100 mt-2">{{ metrics.total_kb_articles }} KB / {{ metrics.total_decisions }} ADRs</div>
          <div class="text-xs text-slate-400 mt-1">Context: {{ metrics.context_lines }} lines</div>
          <div class="text-xs text-sky-400 mt-2 flex items-center gap-1">
            <i data-lucide="activity" class="w-3 h-3"></i> Zero-friction metadata v2.0.1
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 class="text-sm font-bold text-slate-200 uppercase tracking-wider mb-4 flex items-center gap-2">
            <i data-lucide="zap" class="w-4 h-4 text-amber-400"></i> Active & In-Progress Issues
          </h2>
          <div class="space-y-2.5">
            {% for iss in issues if iss.status in ['in-progress', 'open', 'blocked'] %}
            <div class="p-3 bg-slate-950 border border-slate-800/80 rounded-lg flex items-center justify-between hover:border-slate-700 cursor-pointer transition" onclick="openEntity('{{ iss.id }}')">
              <div class="flex items-center space-x-3 truncate">
                <span class="px-2 py-0.5 text-xs rounded font-mono font-bold
                  {% if iss.status == 'in-progress' %}bg-amber-950 text-amber-400 border border-amber-800{% elif iss.status == 'blocked' %}bg-rose-950 text-rose-400 border border-rose-800{% else %}bg-slate-800 text-slate-300{% endif %}">
                  {{ iss.status }}
                </span>
                <span class="text-sm font-medium text-slate-200 truncate">{{ iss.title }}</span>
              </div>
              <span class="text-xs font-mono px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">{{ iss.type }}</span>
            </div>
            {% else %}
            <div class="text-sm text-slate-500 italic p-4 text-center">No active issues in backlog. Everything is completed!</div>
            {% endfor %}
          </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 class="text-sm font-bold text-slate-200 uppercase tracking-wider mb-4 flex items-center gap-2">
            <i data-lucide="sparkles" class="w-4 h-4 text-emerald-400"></i> Milestones Overview
          </h2>
          <div class="space-y-2.5">
            {% for ms in milestones %}
            <div class="p-3 bg-slate-950 border border-slate-800/80 rounded-lg flex items-center justify-between hover:border-slate-700 cursor-pointer transition" onclick="openEntity('{{ ms.id }}')">
              <div class="flex items-center space-x-3 truncate">
                <span class="w-2 h-2 rounded-full bg-sky-400"></span>
                <span class="text-sm text-slate-300 truncate">{{ ms.title }}</span>
              </div>
              <span class="text-xs text-sky-400 font-mono">{{ ms.progress_pct }}%</span>
            </div>
            {% else %}
            <div class="text-sm text-slate-500 italic p-4 text-center">No milestones defined.</div>
            {% endfor %}
          </div>
        </div>
      </div>
    </section>

    <!-- TAB: ISSUES -->
    <section id="content-issues" class="space-y-4 hidden">
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center space-x-3 flex-1 min-w-[280px]">
          <i data-lucide="search" class="w-4 h-4 text-slate-400"></i>
          <input type="text" id="issue-search" oninput="filterIssues()" placeholder="Search issues by title, slug, tag, or priority..." class="bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-sm w-full text-slate-200 focus:outline-none focus:border-sky-500">
        </div>
        <div class="flex items-center space-x-2 text-xs">
          <select id="filter-status" onchange="filterIssues()" class="bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-slate-300">
            <option value="all">All Statuses</option>
            <option value="open">Open</option>
            <option value="in-progress">In Progress</option>
            <option value="blocked">Blocked</option>
            <option value="done">Done</option>
          </select>
          <select id="filter-type" onchange="filterIssues()" class="bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-slate-300">
            <option value="all">All Types</option>
            <option value="feat">feat</option>
            <option value="bug">bug</option>
            <option value="debt">debt</option>
            <option value="task">task</option>
            <option value="docs">docs</option>
          </select>
          <select id="filter-prio" onchange="filterIssues()" class="bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-slate-300">
            <option value="all">All Priorities</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>
      </div>

      <div id="issues-container" class="space-y-2">
        {% for iss in issues %}
        <div class="issue-card bg-slate-900 border border-slate-800 rounded-lg p-4 hover:border-slate-700 cursor-pointer transition flex items-center justify-between"
             data-id="{{ iss.id }}"
             data-title="{{ iss.title | lower }}"
             data-slug="{{ iss.slug | lower }}"
             data-status="{{ iss.status }}"
             data-type="{{ iss.type }}"
             data-priority="{{ iss.priority }}"
             onclick="openEntity('{{ iss.id }}')">
          <div class="flex items-center space-x-4 truncate">
            <span class="px-2.5 py-1 text-xs rounded-md font-mono font-bold
              {% if iss.status == 'done' %}bg-emerald-950 text-emerald-400 border border-emerald-800
              {% elif iss.status == 'in-progress' %}bg-amber-950 text-amber-400 border border-amber-800
              {% elif iss.status == 'blocked' %}bg-rose-950 text-rose-400 border border-rose-800
              {% else %}bg-slate-800 text-slate-300 border border-slate-700{% endif %}">
              {{ iss.status }}
            </span>
            <div>
              <div class="text-sm font-semibold text-slate-200 hover:text-sky-400 transition">{{ iss.title }}</div>
              <div class="text-xs text-slate-500 font-mono mt-0.5 flex items-center gap-2">
                <span>{{ iss.id }}</span>
                {% if iss.milestone %}<span>- {{ iss.milestone }}</span>{% endif %}
                {% if iss.blocked_by %}<span>- <span class="text-rose-400">Blocked by: {{ iss.blocked_by | join(', ') }}</span></span>{% endif %}
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-3 text-xs">
            <span class="px-2 py-0.5 rounded bg-slate-950 border border-slate-800 text-slate-400 font-mono">{{ iss.type }}</span>
            <span class="px-2 py-0.5 rounded font-mono
              {% if iss.priority == 'critical' %}bg-rose-950 text-rose-300 border border-rose-800
              {% elif iss.priority == 'high' %}bg-orange-950 text-orange-300 border border-orange-800
              {% elif iss.priority == 'medium' %}bg-yellow-950 text-yellow-300 border border-yellow-800
              {% else %}bg-slate-800 text-slate-400{% endif %}">
              {{ iss.priority }}
            </span>
          </div>
        </div>
        {% endfor %}
      </div>
    </section>

    <!-- TAB: DAG GRAPH -->
    <section id="content-graph" class="space-y-4 hidden">
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center justify-between">
        <div class="text-sm text-slate-300">
          <strong>Interactive Dependency DAG</strong>: Nodes represent Issues, Milestones, and Risks. Edges represent <span class="text-rose-400 font-bold">blocks</span>, <span class="text-sky-400">part-of</span>, and <span class="text-slate-400">related</span> relationships.
        </div>
        <button onclick="layoutGraph()" class="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 rounded border border-slate-700">
          Reset Layout
        </button>
      </div>
      <div id="cy" class="border border-slate-800 shadow-inner"></div>
    </section>

    <!-- TAB: MILESTONES -->
    <section id="content-milestones" class="space-y-4 hidden">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {% for ms in milestones %}
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 cursor-pointer hover:border-slate-700 transition" onclick="openEntity('{{ ms.id }}')">
          <div class="flex items-center justify-between">
            <span class="text-xs px-2 py-0.5 rounded bg-sky-950 text-sky-400 border border-sky-800 font-mono">{{ ms.status }}</span>
            <span class="text-xs text-slate-400">Due: {{ ms.due_date or 'No date' }}</span>
          </div>
          <h3 class="text-base font-bold text-slate-100 mt-2">{{ ms.title }}</h3>
          <div class="text-xs text-slate-400 mt-1">Slug: {{ ms.slug }}</div>
          <div class="w-full bg-slate-800 h-2 rounded-full mt-4 overflow-hidden">
            <div class="bg-sky-500 h-full rounded-full" style="width: {{ ms.progress_pct }}%"></div>
          </div>
          <div class="flex justify-between text-xs text-slate-400 mt-1.5">
            <span>Progress</span>
            <span class="font-bold text-slate-200">{{ ms.progress_pct }}%</span>
          </div>
        </div>
        {% else %}
        <div class="col-span-2 text-sm text-slate-500 italic p-6 text-center bg-slate-900 border border-slate-800 rounded-xl">No milestones defined.</div>
        {% endfor %}
      </div>
    </section>

    <!-- TAB: RISKS -->
    <section id="content-risks" class="space-y-4 hidden">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {% for r in risks %}
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 cursor-pointer hover:border-slate-700 transition" onclick="openEntity('{{ r.id }}')">
          <div class="flex items-center justify-between">
            <span class="px-2.5 py-0.5 text-xs rounded font-bold uppercase tracking-wider
              {% if r.severity in ['critical', 'high'] %}bg-rose-950 text-rose-300 border border-rose-800{% else %}bg-yellow-950 text-yellow-300 border border-yellow-800{% endif %}">
              {{ r.severity }}
            </span>
            <span class="text-xs text-slate-400 font-mono">{{ r.status }}</span>
          </div>
          <h3 class="text-base font-bold text-slate-100 mt-2">{{ r.title }}</h3>
          <p class="text-xs text-slate-400 mt-2"><strong>Mitigation:</strong> {{ r.mitigation or 'No mitigation specified' }}</p>
          <div class="text-xs text-slate-500 font-mono mt-3">Owner: {{ r.owner }} - Created: {{ r.created }}</div>
        </div>
        {% else %}
        <div class="col-span-2 text-sm text-slate-500 italic p-6 text-center bg-slate-900 border border-slate-800 rounded-xl">No active risks logged.</div>
        {% endfor %}
      </div>
    </section>

    <!-- TAB: KB -->
    <section id="content-kb" class="space-y-4 hidden">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        {% for kb in kb_articles %}
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 cursor-pointer hover:border-slate-700 transition" onclick="openEntity('{{ kb.id }}')">
          <span class="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">{{ kb.type }}</span>
          <h3 class="text-base font-bold text-slate-100 mt-2">{{ kb.title }}</h3>
          <div class="text-xs text-slate-400 font-mono mt-1">{{ kb.slug }}.md</div>
          <div class="flex flex-wrap gap-1 mt-3">
            {% for tag in kb.tags %}
            <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-950 text-slate-400 border border-slate-800">#{{ tag }}</span>
            {% endfor %}
          </div>
        </div>
        {% else %}
        <div class="col-span-3 text-sm text-slate-500 italic p-6 text-center bg-slate-900 border border-slate-800 rounded-xl">No KB articles found.</div>
        {% endfor %}
      </div>
    </section>

    <!-- TAB: SESSIONS -->
    <section id="content-sessions" class="space-y-4 hidden">
      <div class="space-y-3">
        {% for sess in sessions %}
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 cursor-pointer hover:border-slate-700 transition" onclick="openEntity('{{ sess.id }}')">
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold text-sky-400 font-mono">{{ sess.date }}</span>
            <span class="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">{{ sess.agent }}</span>
          </div>
          <div class="text-sm text-slate-200 mt-2 font-medium">{{ sess.summary }}</div>
          <div class="text-xs text-slate-500 font-mono mt-2 flex gap-4">
            <span>Branch: {{ sess.branch }}</span>
            {% if sess.issues_completed %}<span>Completed: {{ sess.issues_completed | length }} issues</span>{% endif %}
          </div>
        </div>
        {% else %}
        <div class="text-sm text-slate-500 italic p-6 text-center bg-slate-900 border border-slate-800 rounded-xl">No session logs found.</div>
        {% endfor %}
      </div>
    </section>

  </main>

  <div id="drawer-backdrop" onclick="closeDrawer()" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 hidden transition-opacity"></div>
  <aside id="entity-drawer" class="fixed right-0 top-0 bottom-0 w-full max-w-2xl bg-slate-900 border-l border-slate-800 shadow-2xl z-50 p-6 overflow-y-auto transform translate-x-full transition-transform duration-300 ease-in-out">
    <div class="flex items-center justify-between border-b border-slate-800 pb-4">
      <div>
        <span id="drawer-tag" class="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">Entity</span>
        <h2 id="drawer-title" class="text-lg font-bold text-slate-100 mt-1">Entity Details</h2>
      </div>
      <button onclick="closeDrawer()" class="p-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>
    </div>
    <div id="drawer-metadata" class="py-4 border-b border-slate-800 text-xs grid grid-cols-2 gap-2 text-slate-400 font-mono"></div>
    <div id="drawer-body" class="prose prose-invert prose-sm max-w-none py-4 text-slate-300"></div>
  </aside>

  <script>
    const RAW_DATA = {{ raw_json_data | safe }};
    let cyInstance = null;

    document.addEventListener('DOMContentLoaded', () => {
      lucide.createIcons();
      initCytoscape();
    });

    function switchTab(tabName) {
      document.querySelectorAll('nav .tab-btn').forEach(btn => btn.classList.remove('active'));
      document.getElementById(`tab-${tabName}`).classList.add('active');

      const tabs = ['overview', 'issues', 'graph', 'milestones', 'risks', 'kb', 'sessions'];
      tabs.forEach(t => {
        const el = document.getElementById(`content-${t}`);
        if (t === tabName) {
          el.classList.remove('hidden');
        } else {
          el.classList.add('hidden');
        }
      });

      if (tabName === 'graph') {
        setTimeout(() => {
          if (cyInstance) {
            cyInstance.resize();
            cyInstance.layout({ name: 'cose', animate: false }).run();
          }
        }, 100);
      }
      lucide.createIcons();
    }

    function filterIssues() {
      const q = document.getElementById('issue-search').value.toLowerCase();
      const statusFilter = document.getElementById('filter-status').value;
      const typeFilter = document.getElementById('filter-type').value;
      const prioFilter = document.getElementById('filter-prio').value;

      document.querySelectorAll('.issue-card').forEach(card => {
        const title = card.getAttribute('data-title');
        const slug = card.getAttribute('data-slug');
        const status = card.getAttribute('data-status');
        const type = card.getAttribute('data-type');
        const prio = card.getAttribute('data-priority');

        const matchQuery = !q || title.includes(q) || slug.includes(q);
        const matchStatus = statusFilter === 'all' || status === statusFilter;
        const matchType = typeFilter === 'all' || type === typeFilter;
        const matchPrio = prioFilter === 'all' || prio === prioFilter;

        if (matchQuery && matchStatus && matchType && matchPrio) {
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      });
    }

    function initCytoscape() {
      const elements = [];
      const nodes = RAW_DATA.graph.nodes || [];
      const edges = RAW_DATA.graph.edges || [];

      nodes.forEach(n => {
        let color = '#38bdf8';
        let shape = 'roundrectangle';
        if (n.type === 'issue') {
          color = n.status === 'done' ? '#10b981' : (n.status === 'in-progress' ? '#f59e0b' : (n.status === 'blocked' ? '#ef4444' : '#64748b'));
        } else if (n.type === 'milestone') {
          color = '#818cf8';
          shape = 'hexagon';
        } else if (n.type === 'risk') {
          color = '#f43f5e';
          shape = 'diamond';
        }
        elements.push({ data: { id: n.id, label: n.label, color: color, shape: shape } });
      });

      edges.forEach(e => {
        let edgeColor = '#475569';
        if (e.type === 'blocks') edgeColor = '#ef4444';
        if (e.type === 'belongs_to') edgeColor = '#38bdf8';
        elements.push({ data: { id: `${e.source}->${e.target}`, source: e.source, target: e.target, label: e.label, color: edgeColor } });
      });

      cyInstance = cytoscape({
        container: document.getElementById('cy'),
        elements: elements,
        style: [
          {
            selector: 'node',
            style: {
              'background-color': 'data(color)',
              'label': 'data(label)',
              'color': '#f8fafc',
              'font-size': '10px',
              'text-valign': 'center',
              'text-halign': 'center',
              'shape': 'data(shape)',
              'width': 'label',
              'height': '32px',
              'padding': '8px'
            }
          },
          {
            selector: 'edge',
            style: {
              'width': 2,
              'line-color': 'data(color)',
              'target-arrow-color': 'data(color)',
              'target-arrow-shape': 'triangle',
              'curve-style': 'bezier',
              'label': 'data(label)',
              'font-size': '8px',
              'color': '#94a3b8'
            }
          }
        ],
        layout: { name: 'cose', padding: 30, animate: false }
      });

      cyInstance.on('tap', 'node', (evt) => {
        openEntity(evt.target.id());
      });
    }

    function layoutGraph() {
      if (cyInstance) {
        cyInstance.layout({ name: 'cose', padding: 30, animate: true }).run();
      }
    }

    function openEntity(id) {
      let entity = null;
      let typeLabel = 'Entity';

      if (id.startsWith('feat--') || id.startsWith('bug--') || id.startsWith('debt--') || id.startsWith('task--') || id.startsWith('docs--')) {
        entity = RAW_DATA.issues.find(i => i.id === id);
        typeLabel = `ISSUE (${entity ? entity.type : ''})`;
      } else if (id.startsWith('milestone--')) {
        entity = RAW_DATA.milestones.find(m => m.id === id);
        typeLabel = 'MILESTONE';
      } else if (id.startsWith('risk--')) {
        entity = RAW_DATA.risks.find(r => r.id === id);
        typeLabel = 'RISK';
      } else if (id.startsWith('kb--')) {
        entity = RAW_DATA.kb_articles.find(k => k.id === id);
        typeLabel = 'KNOWLEDGE BASE';
      } else if (id.startsWith('session--')) {
        entity = RAW_DATA.sessions.find(s => s.id === id);
        typeLabel = 'SESSION';
      }

      if (!entity) return;

      document.getElementById('drawer-tag').innerText = typeLabel;
      document.getElementById('drawer-title').innerText = entity.title || entity.slug || entity.date || id;

      let metaHtml = '';
      if (entity.status) metaHtml += `<div>Status: <span class="text-slate-200 font-bold">${entity.status}</span></div>`;
      if (entity.priority) metaHtml += `<div>Priority: <span class="text-slate-200 font-bold">${entity.priority}</span></div>`;
      if (entity.created) metaHtml += `<div>Created: <span class="text-slate-200">${entity.created}</span></div>`;
      if (entity.completed) metaHtml += `<div>Completed: <span class="text-emerald-400">${entity.completed}</span></div>`;
      if (entity.file_path) metaHtml += `<div class="col-span-2">File: <span class="text-sky-400">${entity.file_path}</span></div>`;
      document.getElementById('drawer-metadata').innerHTML = metaHtml;

      const bodyHtml = marked.parse(entity.body || '*No markdown description provided.*');
      document.getElementById('drawer-body').innerHTML = bodyHtml;

      document.getElementById('drawer-backdrop').classList.remove('hidden');
      document.getElementById('entity-drawer').classList.remove('translate-x-full');
      lucide.createIcons();
    }

    function closeDrawer() {
      document.getElementById('drawer-backdrop').classList.add('hidden');
      document.getElementById('entity-drawer').classList.add('translate-x-full');
    }

    async function refreshData() {
      try {
        const res = await fetch('/api/refresh');
        if (res.ok) {
          window.location.reload();
        }
      } catch (err) {
        console.error('Failed refreshing data:', err);
      }
    }
  </script>
</body>
</html>
"""


def render_html_page(collector: AgentEntityCollector, is_live: bool = False) -> str:
    """Render the full HTML dashboard using Jinja2 with string fallback."""
    collector_dict = collector.to_dict()
    raw_json = json.dumps(collector_dict, ensure_ascii=False)

    if HAS_JINJA:
        tmpl = Template(HTML_TEMPLATE)
        return tmpl.render(
            repo_name=collector.repo_root.name,
            metrics=collector.metrics,
            issues=collector.issues,
            milestones=collector.milestones,
            risks=collector.risks,
            kb_articles=collector.kb_articles,
            sessions=collector.sessions,
            decisions=collector.decisions,
            is_live=is_live,
            raw_json_data=raw_json
        )
    else:
        html = HTML_TEMPLATE.replace("{{ repo_name }}", collector.repo_root.name)
        html = html.replace("{{ metrics.scan_timestamp }}", collector.metrics["scan_timestamp"])
        html = html.replace("{{ metrics.completion_pct }}", str(collector.metrics["completion_pct"]))
        html = html.replace("{{ metrics.total_issues }}", str(collector.metrics["total_issues"]))
        html = html.replace("{{ raw_json_data | safe }}", raw_json)
        return html


def export_static_html(collector: AgentEntityCollector, output_file: Path):
    html_content = render_html_page(collector, is_live=False)
    output_file.write_text(html_content, encoding="utf-8")
    print(f"-> Static dashboard exported: {output_file}")


# ----------------------------------------------------------------------
# 5. FastAPI & Uvicorn Web Server
# ----------------------------------------------------------------------

def run_web_server(collector: AgentEntityCollector, host: str = "127.0.0.1", port: int = 8765, open_browser: bool = True):
    if not HAS_FASTAPI:
        print("[Error] fastapi and uvicorn are required for web mode. Run with: uv run scripts/dashboard.py --web", file=sys.stderr)
        sys.exit(1)

    app = FastAPI(title="Along Dashboard")

    @app.get("/", response_class=HTMLResponse)
    def index():
        collector.collect_all()
        return render_html_page(collector, is_live=True)

    @app.get("/api/data", response_class=JSONResponse)
    def get_data():
        collector.collect_all()
        return collector.to_dict()

    @app.get("/api/refresh", response_class=JSONResponse)
    def refresh_data():
        collector.collect_all()
        return {"status": "ok", "metrics": collector.metrics}

    url = f"http://{host}:{port}"
    print(f"-> Starting Along FastAPI Dashboard at {url}")
    print("   Press Ctrl+C to stop.")

    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    uvicorn.run(app, host=host, port=port, log_level="warning")


# ----------------------------------------------------------------------
# 6. Main CLI Entrypoint
# ----------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Along Dashboard & Analytics")
    parser.add_argument("path", nargs="?", default=".", help="Target repository root path (default: current directory)")
    parser.add_argument("-w", "--web", action="store_true", help="Launch interactive FastAPI web dashboard")
    parser.add_argument("-c", "--cli", action="store_true", help="Print summary table to terminal (default)")
    parser.add_argument("-m", "--markdown", action="store_true", help="Generate or update .along/DASHBOARD.md")
    parser.add_argument("-e", "--export", nargs="?", const=".along/dashboard.html", help="Export standalone static HTML dashboard (default: .along/dashboard.html)")
    parser.add_argument("--port", type=int, default=8765, help="Web server port (default: 8765)")
    parser.add_argument("--host", default="127.0.0.1", help="Web server host (default: 127.0.0.1)")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open browser on web launch")

    args = parser.parse_args()

    agents_dir = find_agents_dir(args.path)
    if not agents_dir.exists():
        print(f"[Error] No .agents/ directory found in {args.path} or parent directories.", file=sys.stderr)
        sys.exit(1)

    collector = AgentEntityCollector(agents_dir).collect_all()

    if args.markdown:
        md_path = agents_dir / "DASHBOARD.md"
        generate_markdown_report(collector, md_path)

    if args.export:
        export_path = Path(args.export)
        if not export_path.is_absolute():
            export_path = collector.repo_root / export_path
        export_static_html(collector, export_path)

    if args.web:
        run_web_server(collector, host=args.host, port=args.port, open_browser=not args.no_browser)
    elif not args.markdown and not args.export:
        render_cli(collector)


if __name__ == "__main__":
    main()
