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

def is_along_wiki_article(content):
    """Checks if a file is already a compiled Along Wiki article (has protocol: along)."""
    fm, _ = parse_frontmatter(content)
    return fm.get("protocol") == "along"

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

def ingest_and_archive_sources(repo_root, docs_dir, archive_dir, dry_run=False):
    """
    Inspects allowed source locations: docs/, wiki/, kb/, and legacy .along/KB/, .agents/KB/.
    - If file is already a compiled Wiki article (protocol: along): standardizes topic-- naming in docs/.
    - If file is a raw unmanaged document (no protocol: along): synthesizes a topic article and moves original to .archive/.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    normalized = 0
    archived = 0

    os.makedirs(docs_dir, exist_ok=True)

    # 1. Ingest external source directories: wiki/, kb/, .along/KB/, .agents/KB/
    external_sources = [
        os.path.join(repo_root, "wiki"),
        os.path.join(repo_root, "kb"),
        os.path.join(repo_root, ".along", "KB"),
        os.path.join(repo_root, ".agents", "KB"),
    ]

    for src_dir in external_sources:
        if not os.path.exists(src_dir):
            continue
        for item in list(os.listdir(src_dir)):
            if item == "INDEX.md" or not item.endswith(".md"):
                continue
            s_path = os.path.join(src_dir, item)
            if not os.path.isfile(s_path):
                continue
            with open(s_path, "r", encoding="utf-8", errors="replace") as fp:
                raw = fp.read()
            
            target_name = LEGACY_FILE_MAPPING.get(item, item)
            if not target_name.startswith("topic--"):
                target_name = f"topic--{target_name}"
            d_path = os.path.join(docs_dir, target_name)

            if is_along_wiki_article(raw):
                # Already a compiled wiki article -> move directly to docs/
                if not dry_run:
                    fm, body = parse_frontmatter(raw)
                    slug = target_name.replace(".md", "")
                    fm["slug"] = slug
                    with open(d_path, "w", encoding="utf-8") as fp:
                        fp.write(dump_frontmatter(fm, body))
                print(f"   Migrated article: {src_dir}/{item} -> docs/{target_name}")
                normalized += 1
            else:
                # Raw source -> synthesize Wiki article and move original to .archive/
                if not dry_run:
                    h1_m = re.search(r"^#\s+(.*)$", raw, re.MULTILINE)
                    title = h1_m.group(1).strip() if h1_m else item.replace(".md", "").replace("-", " ").title()
                    slug = target_name.replace(".md", "")
                    fm = {
                        "protocol": "along",
                        "slug": slug,
                        "title": title,
                        "type": "topic",
                        "created": today,
                        "updated": today,
                        "tags": [slug.replace("topic--", "")],
                    }
                    with open(d_path, "w", encoding="utf-8") as fp:
                        fp.write(dump_frontmatter(fm, raw))
                    # Move original raw file to .archive/
                    arch_path = os.path.join(archive_dir, f"{os.path.basename(src_dir)}--{item}")
                    shutil.copy2(s_path, arch_path)
                print(f"   Compiled & Archived raw source: {src_dir}/{item} -> docs/{target_name} (original -> .archive/)")
                archived += 1

        # Clean up legacy .along/KB/ or .agents/KB/
        if src_dir.endswith("KB") and not dry_run:
            shutil.rmtree(src_dir, ignore_errors=True)

    # 2. Inspect docs/ for raw sources vs compiled articles
    if os.path.exists(docs_dir):
        for item in list(os.listdir(docs_dir)):
            if item == "INDEX.md" or not item.endswith(".md"):
                continue
            f_path = os.path.join(docs_dir, item)
            if not os.path.isfile(f_path):
                continue
            with open(f_path, "r", encoding="utf-8", errors="replace") as fp:
                raw = fp.read()

            target_name = LEGACY_FILE_MAPPING.get(item, item)
            if not target_name.startswith("topic--"):
                target_name = f"topic--{target_name}"

            if is_along_wiki_article(raw):
                # It's an Along Wiki article: ensure standardized topic-- filename
                if target_name != item and not dry_run:
                    dst_path = os.path.join(docs_dir, target_name)
                    fm, body = parse_frontmatter(raw)
                    fm["slug"] = target_name.replace(".md", "")
                    with open(dst_path, "w", encoding="utf-8") as fp:
                        fp.write(dump_frontmatter(fm, body))
                    os.remove(f_path)
                    print(f"   Normalized wiki article name: docs/{item} -> docs/{target_name}")
                    normalized += 1
            else:
                # Raw document in docs/ -> synthesize topic article and archive original
                if not dry_run:
                    h1_m = re.search(r"^#\s+(.*)$", raw, re.MULTILINE)
                    title = h1_m.group(1).strip() if h1_m else item.replace(".md", "").replace("-", " ").title()
                    slug = target_name.replace(".md", "")
                    fm = {
                        "protocol": "along",
                        "slug": slug,
                        "title": title,
                        "type": "topic",
                        "created": today,
                        "updated": today,
                        "tags": [slug.replace("topic--", "")],
                    }
                    dst_path = os.path.join(docs_dir, target_name)
                    with open(dst_path, "w", encoding="utf-8") as fp:
                        fp.write(dump_frontmatter(fm, raw))
                    # Move original raw file to .archive/
                    arch_path = os.path.join(archive_dir, f"raw--{item}")
                    shutil.move(f_path, arch_path)
                print(f"   Compiled & Archived raw document: docs/{item} -> docs/{target_name} (original -> .archive/)")
                archived += 1

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
    ingest_and_archive_sources(repo_root, docs_dir, archive_dir, dry_run=check_only)

    if not os.path.exists(docs_dir) or not os.listdir(docs_dir):
        print("   docs/ is missing or empty. Bootstrapping standard articles...")
        bootstrapped = bootstrap_docs_if_empty(docs_dir, repo_root, dry_run=check_only)
        print(f"   Bootstrapped {bootstrapped} core Knowledge Base articles.")

    articles = []
    broken_links = []
    doc_cross_links = {}

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
                title = h1_m.group(1).strip() if h1_m else slug.replace("topic--", "").replace("-", " ").title()
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
            doc_cross_links[f] = []
            for link_text, link_target in rel_links:
                if link_target.startswith("http://") or link_target.startswith("https://") or link_target.startswith("#") or link_target.startswith("file://"):
                    continue
                clean_target = link_target.split("#")[0].lstrip("./")
                if clean_target and clean_target.endswith(".md"):
                    target_full = os.path.join(docs_dir, clean_target)
                    if not os.path.exists(target_full):
                        broken_links.append((f, link_target))
                    else:
                        doc_cross_links[f].append(clean_target)

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

    # Build Mermaid Knowledge Graph
    mermaid_lines = [
        "## Knowledge Graph & Topic Map\n",
        "```mermaid",
        "flowchart TD",
        "    INDEX[\"Knowledge Base (INDEX)\"]",
    ]
    
    node_ids = {}
    for i, art in enumerate(articles, 1):
        clean_nid = "T_" + re.sub(r"[^A-Z0-9_]", "_", art['slug'].replace('topic--', '').upper())
        node_ids[art['filename']] = clean_nid
        safe_title = art['title'].replace('"', "'")
        mermaid_lines.append(f'    {clean_nid}["{safe_title}"]')
        mermaid_lines.append(f'    INDEX --> {clean_nid}')

    for f_name, cross_targets in doc_cross_links.items():
        src_id = node_ids.get(f_name)
        if not src_id:
            continue
        for tgt in cross_targets:
            tgt_id = node_ids.get(tgt)
            if tgt_id and tgt_id != src_id:
                mermaid_lines.append(f'    {src_id} -.->|references| {tgt_id}')

    mermaid_lines.append("```\n")
    mermaid_lines.append("---\n")
    mermaid_lines.append("## Articles\n")

    index_body_lines = [
        "# Knowledge Base Topic Index\n",
        "Central entry point and cross-linked topic catalog for project documentation:\n",
        "\n".join(mermaid_lines),
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
