#!/usr/bin/env python3
# along_kb_sync.py - Idempotent LLM-Wiki Knowledge Base synchronization, link linting, and index compiler.

import os
import re
import sys
import shutil
import argparse
from datetime import datetime

STANDARD_ARTICLES = [
    ("topic--architecture.md", "System Architecture & Flow", "architecture", ["architecture", "boundaries", "providers", "mcp", "dashboard"]),
    ("topic--domain-model.md", "Domain Model & Entity Ecosystem", "domain-model", ["domain-model", "entities", "schemas", "dag", "metadata"]),
    ("topic--setup-and-workflow.md", "Setup, Installation & Agent Workflows", "setup-workflow", ["setup", "workflow", "installation", "lifecycle", "quality-gates"]),
]

LEGACY_FILE_MAPPING = {
    "01-architecture.md": "topic--architecture.md",
    "02-domain-model.md": "topic--domain-model.md",
    "03-setup-and-workflow.md": "topic--setup-and-workflow.md",
    "04-frontend-frameworks.md": "topic--frontend-frameworks.md",
    "dependencies.md": "topic--dependencies.md",
    "MIGRATIONS.md": "topic--migrations.md",
}

def parse_frontmatter(content):
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
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if v.startswith("[") and v.endswith("]"):
                items = [x.strip().strip('"').strip("'") for x in v[1:-1].split(",") if x.strip()]
                fm[k] = items
            else:
                fm[k] = v
    return fm, body

def dump_frontmatter(fm, body):
    lines = ["---"]
    lines.append("protocol: along")
    for k, v in fm.items():
        if k == "protocol":
            continue
        if isinstance(v, list):
            items_str = ", ".join(f'"{x}"' if " " in x else x for x in v)
            lines.append(f"{k}: [{items_str}]")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.strip() + "\n"

def ensure_archive_structure(repo_root, dry_run=False):
    archive_dir = os.path.join(repo_root, ".archive")
    if not dry_run:
        os.makedirs(archive_dir, exist_ok=True)
        gitkeep = os.path.join(archive_dir, ".gitkeep")
        if not os.path.exists(gitkeep):
            with open(gitkeep, "w", encoding="utf-8") as f:
                f.write("")
        readme = os.path.join(archive_dir, "README.md")
        if not os.path.exists(readme):
            with open(readme, "w", encoding="utf-8") as f:
                f.write("# Archived Raw Sources (.archive/)\n\nThis directory holds processed raw notes, external documentation dumps, drafts, and unstructured source files that have been synthesized into structured Knowledge Base articles in `docs/`.\n")
    return archive_dir

def normalize_and_archive_sources(repo_root, docs_dir, archive_dir, dry_run=False):
    normalized = 0
    archived = 0

    # 1. Normalize legacy files in docs/
    if os.path.exists(docs_dir):
        for item in list(os.listdir(docs_dir)):
            if item == "INDEX.md" or not item.endswith(".md"):
                continue
            target_name = LEGACY_FILE_MAPPING.get(item, item)
            if not target_name.startswith("topic--") and target_name != "INDEX.md":
                target_name = f"topic--{target_name}"
            if target_name != item:
                src_p = os.path.join(docs_dir, item)
                dst_p = os.path.join(docs_dir, target_name)
                if not dry_run:
                    with open(src_p, "r", encoding="utf-8", errors="replace") as fp:
                        content = fp.read()
                    slug = target_name.replace(".md", "")
                    content = re.sub(r"^slug:\s*[^\n]+", f"slug: {slug}", content, flags=re.MULTILINE)
                    with open(dst_p, "w", encoding="utf-8") as fp:
                        fp.write(content)
                    os.remove(src_p)
                print(f"   Normalized legacy doc: docs/{item} -> docs/{target_name}")
                normalized += 1

    # 2. Archive raw unmanaged source folders
    raw_dirs = [os.path.join(repo_root, "docs_raw"), os.path.join(docs_dir, "raw")]
    for rdir in raw_dirs:
        if os.path.exists(rdir):
            for item in os.listdir(rdir):
                s = os.path.join(rdir, item)
                d = os.path.join(archive_dir, item)
                if not dry_run:
                    shutil.move(s, d)
                archived += 1
            if not dry_run:
                shutil.rmtree(rdir, ignore_errors=True)
            print(f"   Archived raw directory: {rdir} -> .archive/")

    return normalized, archived

def bootstrap_docs_if_empty(docs_dir, repo_root, dry_run=False):
    today = datetime.now().strftime("%Y-%m-%d")
    repo_name = os.path.basename(os.path.abspath(repo_root))
    created = 0
    if not dry_run:
        os.makedirs(docs_dir, exist_ok=True)
    for filename, title, art_type, tags in STANDARD_ARTICLES:
        target_path = os.path.join(docs_dir, filename)
        if not os.path.exists(target_path):
            slug = filename.replace(".md", "")
            fm = {
                "protocol": "along",
                "slug": slug,
                "title": title,
                "type": art_type,
                "created": today,
                "updated": today,
                "tags": tags,
            }
            body = f"# {title}\n\nCore technical specification and documentation for {repo_name}.\n\n## Overview\nDocument system components and engineering guidelines here.\n"
            full_text = dump_frontmatter(fm, body)
            if not dry_run:
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(full_text)
            print(f"   + Bootstrapped {filename}")
            created += 1
    return created

def sync_kb(repo_root, check_only=False):
    repo_root = os.path.abspath(repo_root)
    docs_dir = os.path.join(repo_root, "docs")
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"-> Synchronizing Knowledge Base in {docs_dir}...")
    archive_dir = ensure_archive_structure(repo_root, dry_run=check_only)
    normalize_and_archive_sources(repo_root, docs_dir, archive_dir, dry_run=check_only)

    if not os.path.exists(docs_dir) or not os.listdir(docs_dir):
        print("   docs/ is missing or empty. Bootstrapping standard articles...")
        bootstrapped = bootstrap_docs_if_empty(docs_dir, repo_root, dry_run=check_only)
        print(f"   Bootstrapped {bootstrapped} core Knowledge Base articles.")

    articles = []
    broken_links = []

    for f in sorted(os.listdir(docs_dir)):
        if not f.endswith(".md") or f == "INDEX.md":
            continue
        file_path = os.path.join(docs_dir, f)
        if not os.path.isfile(file_path):
            continue

        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as fp:
                raw_content = fp.read()
            fm, body = parse_frontmatter(raw_content)

            needs_update = False
            slug = fm.get("slug", f.replace(".md", ""))
            title = fm.get("title")
            if not title:
                h1_m = re.search(r"^#\s+(.*)$", body, re.MULTILINE)
                title = h1_m.group(1).strip() if h1_m else slug
                fm["title"] = title
                needs_update = True

            if fm.get("protocol") != "along":
                fm["protocol"] = "along"
                needs_update = True
            if not fm.get("slug"):
                fm["slug"] = slug
                needs_update = True
            if not fm.get("type"):
                fm["type"] = "topic"
                needs_update = True
            if not fm.get("created"):
                fm["created"] = today
                needs_update = True
            if not fm.get("tags"):
                fm["tags"] = [slug.replace("topic--", "")]
                needs_update = True

            if needs_update and not check_only:
                fm["updated"] = today
                new_content = dump_frontmatter(fm, body)
                with open(file_path, "w", encoding="utf-8") as fp:
                    fp.write(new_content)

            rel_links = re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", body)
            for link_text, link_target in rel_links:
                if link_target.startswith("http://") or link_target.startswith("https://") or link_target.startswith("#") or link_target.startswith("file://"):
                    continue
                clean_target = link_target.split("#")[0].lstrip("./")
                if clean_target and clean_target.endswith(".md"):
                    target_full = os.path.join(docs_dir, clean_target)
                    if not os.path.exists(target_full):
                        broken_links.append((f, link_target))

            articles.append({
                "filename": f,
                "slug": slug,
                "title": title,
                "type": fm.get("type", "topic"),
                "tags": fm.get("tags", []),
            })
        except Exception as e:
            print(f"   [WARN] Failed to process {f}: {e}")

    index_path = os.path.join(docs_dir, "INDEX.md")
    index_fm = {
        "protocol": "along",
        "slug": "INDEX",
        "title": "Knowledge Base Topic Index",
        "type": "index",
        "created": today,
        "updated": today,
        "tags": ["index", "kb", "topics", "map"],
    }

    index_body_lines = [
        "# Knowledge Base Topic Index\n",
        "Central entry point and cross-linked topic catalog for project documentation:\n",
        "## Articles\n",
    ]

    for art in articles:
        tags_str = ", ".join(f"`{t}`" for t in art["tags"]) if art["tags"] else ""
        index_body_lines.append(f"- **[{art['title']}](./{art['filename']})** ({art['type']}) {tags_str}")

    index_body_lines.append("\n---\n\n## Related Context\n")
    index_body_lines.append("- [AGENTS.md](file://AGENTS.md): Active protocol conventions and rules.")
    index_body_lines.append("- [.along/DECISIONS.md](file://.along/DECISIONS.md): Architectural Decision Records.")
    index_body_lines.append("- [.along/ISSUES.md](file://.along/ISSUES.md): Active issue tracking board.")
    index_body_lines.append("- [.along/CONTEXT.md](file://.along/CONTEXT.md): Current session snapshot.")

    if not check_only:
        full_index = dump_frontmatter(index_fm, "\n".join(index_body_lines))
        with open(index_path, "w", encoding="utf-8") as fp:
            fp.write(full_index)
        print(f"   -> Rebuilt docs/INDEX.md ({len(articles)} articles indexed).")

    if broken_links:
        print(f"   [WARN] Detected {len(broken_links)} dangling or unverified Markdown link(s):")
        for src, target in broken_links:
            print(f"      - In {src}: target '{target}' not found.")
    else:
        print("   [OK] All internal Markdown links verified.")

    print(f"-> Knowledge Base sync complete. Total active articles: {len(articles) + (1 if os.path.exists(index_path) else 0)}\n")
    return len(articles), len(broken_links)

def main():
    parser = argparse.ArgumentParser(description="Along Knowledge Base Compiler & Linter")
    parser.add_argument("repo_root", nargs="?", default=".", help="Target repository root directory")
    parser.add_argument("--check", action="store_true", help="Check links and structure without modifying files")
    args = parser.parse_args()

    sync_kb(args.repo_root, check_only=args.check)

if __name__ == "__main__":
    main()
