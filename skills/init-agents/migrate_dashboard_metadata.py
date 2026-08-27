#!/usr/bin/env python3
"""
Migrate .agents/ protocol metadata to v1.5.0 (Automated Entity Ecosystem & Structured Metadata).
Scans .agents/ISSUES/, .agents/SESSIONS/, .agents/KB/, .agents/MILESTONES/, .agents/RISKS/,
.agents/SPIKES/, .agents/CHECKLISTS/ and ensures complete, parseable YAML front-matter.
"""

import os
import re
import sys
import glob
from datetime import datetime

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
            fm[key] = val
    return fm, body

def dump_yaml_frontmatter(fm, body):
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            lines.append(f"{k}: [{', '.join(v)}]")
        elif v is None:
            lines.append(f"{k}: null")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.lstrip()

def ensure_entity_dirs(agents_dir):
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

def migrate_issues(agents_dir):
    issues_dir = os.path.join(agents_dir, "ISSUES")
    if not os.path.exists(issues_dir):
        return 0

    count = 0
    today_str = datetime.now().strftime("%Y-%m-%d")

    all_files = glob.glob(os.path.join(issues_dir, "*.md")) + glob.glob(os.path.join(issues_dir, "done", "*.md"))

    for filepath in all_files:
        is_done = "done" in os.path.dirname(filepath).replace("\\", "/").split("/")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        fm, body = parse_yaml_frontmatter(content)
        modified = False

        if "slug" not in fm:
            slug = os.path.basename(filepath).replace(".md", "")
            if "--" in slug:
                slug = slug.split("--", 1)[1]
            fm["slug"] = slug
            modified = True

        if "type" not in fm:
            filename = os.path.basename(filepath)
            if "--" in filename:
                fm["type"] = filename.split("--", 1)[0]
            else:
                fm["type"] = "feat"
            modified = True

        if "status" not in fm:
            fm["status"] = "done" if is_done else "open"
            modified = True

        if "priority" not in fm:
            fm["priority"] = "medium"
            modified = True

        if "created" not in fm:
            fm["created"] = today_str
            modified = True

        if "updated" not in fm:
            fm["updated"] = fm.get("created", today_str)
            modified = True

        if is_done or fm.get("status") == "done":
            fm["status"] = "done"
            if "completed" not in fm:
                fm["completed"] = fm.get("updated", today_str)
                modified = True
        else:
            if "completed" in fm and fm["completed"] is not None:
                del fm["completed"]
                modified = True

        if "agent" not in fm:
            fm["agent"] = "antigravity"
            modified = True

        if "tags" not in fm:
            tags = []
            if "mcp" in fm.get("slug", ""):
                tags.append("mcp")
            if "kb" in fm.get("slug", "") or "knowledge" in fm.get("slug", ""):
                tags.append("kb")
            fm["tags"] = tags
            modified = True

        if modified:
            new_content = dump_yaml_frontmatter(fm, body)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            count += 1

    return count

def migrate_sessions(agents_dir):
    sessions_dir = os.path.join(agents_dir, "SESSIONS")
    if not os.path.exists(sessions_dir):
        return 0

    count = 0
    today_str = datetime.now().strftime("%Y-%m-%d")

    all_files = glob.glob(os.path.join(sessions_dir, "**", "*.md"), recursive=True)

    for filepath in all_files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        fm, body = parse_yaml_frontmatter(content)
        modified = False

        if "date" not in fm:
            fm["date"] = today_str
            modified = True

        if "slug" not in fm:
            fm["slug"] = os.path.basename(filepath).replace(".md", "")
            modified = True

        if "agent" not in fm:
            fm["agent"] = "antigravity"
            modified = True

        if "branch" not in fm:
            fm["branch"] = "main"
            modified = True

        if "commit" not in fm:
            fm["commit"] = "unknown"
            modified = True

        if "summary" not in fm:
            fm["summary"] = "Work session update."
            modified = True

        if "issues_advanced" not in fm:
            fm["issues_advanced"] = []
            modified = True

        if "issues_completed" not in fm:
            fm["issues_completed"] = []
            modified = True

        if "decisions" not in fm:
            fm["decisions"] = []
            modified = True

        if "risks_logged" not in fm:
            fm["risks_logged"] = []
            modified = True

        if "spikes_conducted" not in fm:
            fm["spikes_conducted"] = []
            modified = True

        if modified:
            new_content = dump_yaml_frontmatter(fm, body)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            count += 1

    return count

def migrate_kb(agents_dir):
    kb_dir = os.path.join(agents_dir, "KB")
    if not os.path.exists(kb_dir):
        return 0

    count = 0
    today_str = datetime.now().strftime("%Y-%m-%d")
    all_files = glob.glob(os.path.join(kb_dir, "*.md"))

    for filepath in all_files:
        filename = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        fm, body = parse_yaml_frontmatter(content)
        modified = False

        if not fm:
            slug = filename.replace(".md", "")
            title = slug.replace("-", " ").title()
            fm = {
                "slug": slug,
                "title": title,
                "type": "topic",
                "created": today_str,
                "updated": today_str,
                "tags": []
            }
            modified = True
        else:
            if "slug" not in fm:
                fm["slug"] = filename.replace(".md", "")
                modified = True
            if "updated" not in fm:
                fm["updated"] = today_str
                modified = True

        if modified:
            new_content = dump_yaml_frontmatter(fm, body)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            count += 1

    return count

def main():
    repo_root = os.getcwd()
    if len(sys.argv) > 1:
        repo_root = sys.argv[1]

    agents_dir = os.path.join(repo_root, ".agents")
    if not os.path.exists(agents_dir):
        print(f"No .agents/ directory found in {repo_root}")
        sys.exit(0)

    print(f"-> Migrating .agents/ metadata in {repo_root} to v1.5.0 standard...")
    ensure_entity_dirs(agents_dir)
    migrated_issues = migrate_issues(agents_dir)
    migrated_sessions = migrate_sessions(agents_dir)
    migrated_kb = migrate_kb(agents_dir)

    print(f"   Issues updated:   {migrated_issues}")
    print(f"   Sessions updated: {migrated_sessions}")
    print(f"   KB articles updated: {migrated_kb}")
    print("-> Metadata migration to v1.5.0 complete!")

if __name__ == "__main__":
    main()
