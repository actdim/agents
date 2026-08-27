#!/usr/bin/env python3
"""
migrate_protocol.py - Version-aware migration engine for ACTDIM-AGENTS-PROTOCOL.
migrate_protocol.py - Version-aware migration engine for ACTDIM-AGENTS-PROTOCOL.

Executes sequential, version-specific migration steps on target repository's .agents/ structure:
  - v1.0.0 -> v1.1.0: Tasks -> Issues directory & kebab-case renaming
  - v1.1.0 -> v1.3.0: Knowledge Base (.agents/KB/) & .code-review-graph-ignore scaffolding
  - v1.0.0 -> v1.1.0: Tasks -> Issues directory and kebab-case renaming
  - v1.1.0 -> v1.3.0: Knowledge Base (.agents/KB/) and .code-review-graph-ignore scaffolding
  - v1.3.3 -> v1.5.0: Entity Ecosystem (MILESTONES, RISKS, SPIKES, CHECKLISTS),
                     retroactive Milestone synthesis from past sessions/done issues,
                     standard Checklists synthesis, and complete YAML front-matter enrichment.
  - Typography sanitation: bans em-dash (-) and replaces with standard ASCII hyphens (-).
  - Typography sanitation: bans em-dash (U+2014) and replaces with standard ASCII hyphens (-).

Usage:
    python skills/init-agents/migrate_protocol.py [TARGET_REPO_ROOT]
"""

import os
import re
import sys
import glob
from datetime import datetime

CURRENT_PROTOCOL_VERSION = "1.5.0"
CURRENT_PROTOCOL_VERSION = "1.5.2"

def parse_yaml_frontmatter(content):
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content
    fm_str, body = match.group(1), match.group(2)
    fm = {}
    for line in fm_str.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                fm[key] = [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()] if inner else []
            elif val.lower() == "true":
                fm[key] = True
            elif val.lower() == "false":
                fm[key] = False
            elif val.lower() == "null" or val == "":
                fm[key] = None
            else:
                fm[key] = val
    return fm, body

def dump_yaml_frontmatter(fm, body):
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            items_str = ", ".join(f'"{x}"' if " " in str(x) or "#" in str(x) else str(x) for x in v)
            lines.append(f"{k}: [{items_str}]")
        elif v is None:
            lines.append(f"{k}: null")
        elif isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.lstrip()

def detect_protocol_version(repo_root):
    agents_md = os.path.join(repo_root, "AGENTS.md")
    if os.path.exists(agents_md):
        with open(agents_md, "r", encoding="utf-8") as f:
            content = f.read()
        m = re.search(r"ACTDIM-AGENTS-PROTOCOL v(\d+\.\d+\.\d+)", content)
        if m:
            return m.group(1)
    return "1.0.0"

def step_migrate_v1_1_tasks_to_issues(agents_dir):
    updated = False
    tasks_md = os.path.join(agents_dir, "TASKS.md")
    issues_md = os.path.join(agents_dir, "ISSUES.md")
    if os.path.exists(tasks_md) and not os.path.exists(issues_md):
        with open(tasks_md, "r", encoding="utf-8") as f:
            c = f.read()
        c = re.sub(r"# Tasks", "# Issues", c)
        c = re.sub(r"TASKS", "ISSUES", c)
        with open(issues_md, "w", encoding="utf-8") as f:
            f.write(c)
        os.remove(tasks_md)
        updated = True

    tasks_dir = os.path.join(agents_dir, "TASKS")
    issues_dir = os.path.join(agents_dir, "ISSUES")
    if os.path.exists(tasks_dir) and not os.path.exists(issues_dir):
        os.rename(tasks_dir, issues_dir)
        updated = True
    return updated

def step_migrate_v1_3_kb_scaffolding(repo_root, agents_dir):
    kb_dir = os.path.join(agents_dir, "KB")
    os.makedirs(kb_dir, exist_ok=True)
    today_str = datetime.now().strftime("%Y-%m-%d")

    standard_kb_articles = {
        "INDEX.md": ("INDEX", "Knowledge Base Index", "index", [
            "# Knowledge Base Index\n\nCentral topic map for project documentation.\n\n"
            "- [[01-architecture]]: System architecture and data flows.\n"
            "- [[02-domain-model]]: Core domain entities and business rules.\n"
            "- [[03-setup-and-workflow]]: Build, run, test, and contribution workflows.\n"
        ]),
        "01-architecture.md": ("01-architecture", "System Architecture & Flow", "architecture", [
            "# System Architecture & Flow\n\nHigh-level architectural components, module boundaries, and execution models.\n"
        ]),
        "02-domain-model.md": ("02-domain-model", "Domain Model & Entities", "domain-model", [
            "# Domain Model & Entities\n\nCore domain terminology, data models, and schema relationships.\n"
        ]),
        "03-setup-and-workflow.md": ("03-setup-and-workflow", "Setup & Developer Workflow", "setup-workflow", [
            "# Setup & Developer Workflow\n\nBuild instructions, test suites, local development, and skill deployment guidelines.\n"
        ]),
    }

    created = 0
    for filename, (slug, title, type_name, body_lines) in standard_kb_articles.items():
        filepath = os.path.join(kb_dir, filename)
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            fm = {
                "slug": slug,
                "title": title,
                "type": type_name,
                "created": today_str,
                "updated": today_str,
                "tags": [type_name]
            }
            body = "".join(body_lines)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(dump_yaml_frontmatter(fm, body))
            created += 1

    crg_ignore = os.path.join(repo_root, ".code-review-graph-ignore")
    if not os.path.exists(crg_ignore):
        with open(crg_ignore, "w", encoding="utf-8") as f:
            f.write("# Code Review Graph Exclusions\nnode_modules/\ndist/\nbuild/\nout/\n.git/\n.agents/SESSIONS/\n*.min.js\n*.bundle.js\n*.pyc\n__pycache__/\n")

    return created

def step_migrate_v1_5_entity_ecosystem(repo_root, agents_dir):
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_year = datetime.now().strftime("%Y")

    dirs = [
        os.path.join(agents_dir, "ISSUES", "done"),
        os.path.join(agents_dir, "SESSIONS", today_year),
        os.path.join(agents_dir, "KB"),
        os.path.join(agents_dir, "MILESTONES"),
        os.path.join(agents_dir, "RISKS"),
        os.path.join(agents_dir, "SPIKES"),
        os.path.join(agents_dir, "CHECKLISTS"),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        gitkeep = os.path.join(d, ".gitkeep")
        if not os.path.exists(gitkeep) and len(os.listdir(d)) == 0:
            open(gitkeep, "a").close()

    checklists_dir = os.path.join(agents_dir, "CHECKLISTS")
    standard_checklists = {
        "stage-completion.md": {
            "slug": "stage-completion",
            "title": "Mandatory Stage Completion & Wrap-Up",
            "category": "stage-completion",
            "body": "# Mandatory Stage Completion Checklist\n\n"
                    "1. [ ] Automated tests, linting, and builds run with quiet flags.\n"
                    "2. [ ] All completed issues moved to `ISSUES/done/` with `status: done` and `completed: YYYY-MM-DD`.\n"
                    "3. [ ] Related milestone progress percentage updated.\n"
                    "4. [ ] Active session log written to `SESSIONS/`.\n"
                    "5. [ ] CONTEXT snapshot rewritten (< 20 lines).\n"
                    "6. [ ] ISSUES board updated and lean.\n"
                    "7. [ ] Prompt user to compact session (`/compact`).\n"
        },
        "pre-commit.md": {
            "slug": "pre-commit",
            "title": "Pre-Commit Quality Gate",
            "category": "pre-commit",
            "body": "# Pre-Commit Verification Checklist\n\n"
                    "1. [ ] Code compiles and unit tests pass.\n"
                    "2. [ ] Mandatory git diff inspected for zero unintended deletions.\n"
                    "3. [ ] No API keys, secrets, or sensitive credentials committed.\n"
                    "4. [ ] Filenames are Windows-safe (no colons, YYYY-MM-DD dates).\n"
        }
    }
    for filename, data in standard_checklists.items():
        cpath = os.path.join(checklists_dir, filename)
        if not os.path.exists(cpath):
            fm = {
                "slug": data["slug"],
                "title": data["title"],
                "category": data["category"],
                "created": today_str,
                "updated": today_str
            }
            with open(cpath, "w", encoding="utf-8") as f:
                f.write(dump_yaml_frontmatter(fm, data["body"]))

    milestones_dir = os.path.join(agents_dir, "MILESTONES")
    done_issues = glob.glob(os.path.join(agents_dir, "ISSUES", "done", "*.md"))
    active_issues = glob.glob(os.path.join(agents_dir, "ISSUES", "*.md"))

    done_slugs = [os.path.basename(f).replace(".md", "") for f in done_issues]
    active_slugs = [os.path.basename(f).replace(".md", "") for f in active_issues]

    if len(glob.glob(os.path.join(milestones_dir, "*.md"))) == 0:
        if done_slugs:
            past_m = os.path.join(milestones_dir, "v1.3.0-knowledge-base-and-graph.md")
            fm_past = {
                "slug": "v1.3.0-knowledge-base-and-graph",
                "title": "v1.3.0: Knowledge Base Architecture & Code Graph Integration",
                "status": "completed",
                "due_date": "2026-08-26",
                "created": "2026-08-11",
                "target_issues": done_slugs,
                "progress_pct": 100
            }
            body_past = "# Milestone: v1.3.0 Knowledge Base & Code Graph\n\nDelivered structured `.agents/KB/` documentation architecture, `/init-kb`, `/search-kb`, `/sync-kb`, `/check-graph`, and `code-review-graph` MCP integration.\n"
            with open(past_m, "w", encoding="utf-8") as f:
                f.write(dump_yaml_frontmatter(fm_past, body_past))

        current_m = os.path.join(milestones_dir, "v1.5.0-dashboard-and-analytics.md")
        fm_curr = {
            "slug": "v1.5.0-dashboard-and-analytics",
            "title": "v1.5.0: Automated Entity Ecosystem & Project Dashboard",
            "status": "in-progress",
            "due_date": "2026-09-05",
            "created": "2026-08-27",
            "target_issues": active_slugs,
            "progress_pct": 50
        }
        body_curr = "# Milestone: v1.5.0 Automated Entity Ecosystem & Dashboard\n\nDelivers full automated entity lifecycles (`MILESTONES`, `RISKS`, `SPIKES`, `CHECKLISTS`), protocol migration engine, and `/repo-dashboard` visual analytics.\n"
        with open(current_m, "w", encoding="utf-8") as f:
            f.write(dump_yaml_frontmatter(fm_curr, body_curr))

    all_issue_files = done_issues + active_issues
    for filepath in all_issue_files:
        is_done = "done" in os.path.dirname(filepath).replace("\\", "/").split("/")
        filename = os.path.basename(filepath)
        raw_slug = filename.replace(".md", "")
        clean_slug = raw_slug.split("--", 1)[1] if "--" in raw_slug else raw_slug
        issue_type = filename.split("--", 1)[0] if "--" in filename else "feat"

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        fm, body = parse_yaml_frontmatter(content)
        fm["slug"] = fm.get("slug", clean_slug)
        fm["type"] = fm.get("type", issue_type)
        fm["status"] = "done" if is_done else fm.get("status", "open")
        fm["priority"] = fm.get("priority", "medium")
        fm["created"] = fm.get("created", today_str)
        fm["updated"] = fm.get("updated", fm["created"])
        if is_done:
            fm["completed"] = fm.get("completed", fm["updated"])
        else:
            if "completed" in fm:
                del fm["completed"]
        fm["agent"] = fm.get("agent", "antigravity")
        
        if "tags" not in fm or not fm["tags"]:
            tags = []
            if "mcp" in fm["slug"]: tags.append("mcp")
            if "kb" in fm["slug"] or "knowledge" in fm["slug"]: tags.append("kb")
            if "dashboard" in fm["slug"] or "analytics" in fm["slug"]: tags.append("dashboard")
            fm["tags"] = tags

        if "milestone" not in fm or not fm["milestone"]:
            if is_done:
                fm["milestone"] = "v1.3.0-knowledge-base-and-graph"
            else:
                fm["milestone"] = "v1.5.0-dashboard-and-analytics"

        new_content = dump_yaml_frontmatter(fm, body)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    session_files = glob.glob(os.path.join(agents_dir, "SESSIONS", "**", "*.md"), recursive=True)
    for filepath in session_files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        fm, body = parse_yaml_frontmatter(content)
        fm["date"] = fm.get("date", today_str)
        fm["slug"] = fm.get("slug", os.path.basename(filepath).replace(".md", ""))
        fm["agent"] = fm.get("agent", "antigravity")
        fm["branch"] = fm.get("branch", "main")
        fm["commit"] = fm.get("commit", "unknown")
        fm["summary"] = fm.get("summary", "Work session log.")
        fm["milestone"] = fm.get("milestone", "v1.5.0-dashboard-and-analytics")
        fm["issues_advanced"] = fm.get("issues_advanced", [])
        fm["issues_completed"] = fm.get("issues_completed", [])
        fm["decisions"] = fm.get("decisions", [])
        fm["risks_logged"] = fm.get("risks_logged", [])
        fm["spikes_conducted"] = fm.get("spikes_conducted", [])

        new_content = dump_yaml_frontmatter(fm, body)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    kb_files = glob.glob(os.path.join(agents_dir, "KB", "*.md"))
    for filepath in kb_files:
        filename = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        fm, body = parse_yaml_frontmatter(content)
        slug = filename.replace(".md", "")
        title = slug.replace("-", " ").title()
        fm["slug"] = fm.get("slug", slug)
        fm["title"] = fm.get("title", title)
        fm["type"] = fm.get("type", "topic")
        fm["created"] = fm.get("created", today_str)
        fm["updated"] = fm.get("updated", today_str)
        fm["tags"] = fm.get("tags", [])

        new_content = dump_yaml_frontmatter(fm, body)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    # 7. Typography and markdown punctuation sanitation (no em-dash)
    sanitize_markdown_typography(agents_dir)

    return True

TYPOGRAPHY_REPLACEMENTS = {
    '\u2014': '-',      # em-dash
    '\u2013': '-',      # en-dash
    '\u2212': '-',      # math minus
    '\u2011': '-',      # non-breaking hyphen
    '\u201c': '"',      # left double quote
    '\u201d': '"',      # right double quote
    '\u2018': "'",      # left single quote
    '\u2019': "'",      # right single quote
    '\u00ab': '"',      # left guillemet
    '\u00bb': '"',      # right guillemet
    '\u2026': '...',    # ellipsis
    '\u00a0': ' ',      # NBSP
    '\u202f': ' ',      # narrow NBSP
    '\u200b': '',       # ZWSP
    '\ufeff': '',       # BOM
    '\u2022': '-',      # bullet
    '\u2023': '-',      # bullet
    '\u2043': '-',      # bullet
}

def sanitize_markdown_typography(target_dir):
    md_files = glob.glob(os.path.join(target_dir, "**", "*.md"), recursive=True)
    count = 0
    em_dash = '\u2014'
    for fpath in md_files:
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        cleaned = content
        if f" {em_dash} " in cleaned:
            cleaned = cleaned.replace(f" {em_dash} ", " - ")
        for char, repl in TYPOGRAPHY_REPLACEMENTS.items():
            if char in cleaned:
                cleaned = cleaned.replace(char, repl)
        if cleaned != content:
            with open(fpath, "w", encoding="utf-8", newline="\n") as f:
                f.write(cleaned)
            count += 1
    return count

def run_migrations(repo_root):
    agents_dir = os.path.join(repo_root, ".agents")
    if not os.path.exists(agents_dir):
        print(f"No .agents/ directory found in {repo_root}. Run /init-agents first.")
        return

    detected_version = detect_protocol_version(repo_root)
    print("==================================================")
    print("-> ACTDIM-AGENTS Migration Engine")
    print(f"   Target: {repo_root}")
    print(f"   Detected Protocol Version: v{detected_version}")
    print(f"   Target Protocol Version:   v{CURRENT_PROTOCOL_VERSION}")
    print("==================================================")

    # Step 1
    print("-> Step 1 [v1.0 -> v1.1]: Verifying ISSUES directory structure...")
    step_migrate_v1_1_tasks_to_issues(agents_dir)

    # Step 2
    print("-> Step 2 [v1.1 -> v1.3]: Scaffolding Knowledge Base (KB) & Code Graph ignore...")
    step_migrate_v1_3_kb_scaffolding(repo_root, agents_dir)

    # Step 3
    print("-> Step 3 [v1.3 -> v1.5]: Upgrading Entity Ecosystem, Milestones & Checklists...")
    step_migrate_v1_5_entity_ecosystem(repo_root, agents_dir)

    # Step 4
    print("-> Step 4: Sanitizing Markdown typography & invisible characters...")
    sanitized_count = sanitize_markdown_typography(agents_dir)
    if sanitized_count > 0:
        print(f"   Sanitized typography in {sanitized_count} Markdown files.")

    print(f"-> [OK] All migrations completed successfully to v{CURRENT_PROTOCOL_VERSION} standard!")

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    run_migrations(root)
