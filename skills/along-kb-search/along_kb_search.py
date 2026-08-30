#!/usr/bin/env python3
# along_kb_search.py - Fast targeted structured retrieval across docs/ and project documentation.

import os
import re
import sys
import argparse

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

def search_docs(query, repo_root=".", limit=5, filter_tag=None):
    repo_root = os.path.abspath(repo_root)
    docs_dir = os.path.join(repo_root, "docs")
    query_terms = [t.lower().strip() for t in query.split() if t.strip()]

    if not os.path.exists(docs_dir):
        print(f"[WARN] No docs/ directory found at {repo_root}.")
        return []

    results = []
    for f in sorted(os.listdir(docs_dir)):
        if not f.endswith(".md") or f == "INDEX.md":
            continue
        file_path = os.path.join(docs_dir, f)
        if not os.path.isfile(file_path):
            continue

        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as fp:
                raw = fp.read()
            fm, body = parse_frontmatter(raw)
            tags = fm.get("tags", [])
            if isinstance(tags, str):
                tags = [tags]

            if filter_tag and filter_tag.lower() not in [t.lower() for t in tags]:
                continue

            title = fm.get("title", f)
            body_lower = body.lower()
            title_lower = title.lower()

            score = 0.0
            for term in query_terms:
                if term in title_lower:
                    score += 10.0
                for t in tags:
                    if term in t.lower():
                        score += 5.0
                matches = body_lower.count(term)
                score += min(matches * 1.0, 10.0)

            if score > 0 or not query_terms:
                snippet = ""
                if query_terms:
                    pos = body_lower.find(query_terms[0])
                    if pos != -1:
                        start = max(0, pos - 80)
                        end = min(len(body), pos + 150)
                        snippet = body[start:end].replace("\n", " ").strip()
                if not snippet:
                    snippet = body[:180].replace("\n", " ").strip()

                results.append({
                    "file": f"docs/{f}",
                    "title": title,
                    "type": fm.get("type", "topic"),
                    "tags": tags,
                    "score": score,
                    "snippet": snippet,
                })
        except Exception as e:
            pass

    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:limit]

def main():
    parser = argparse.ArgumentParser(description="Along Knowledge Base Fast Search")
    parser.add_argument("query", nargs="?", default="", help="Search query terms")
    parser.add_argument("--repo", default=".", help="Target repository root")
    parser.add_argument("--limit", type=int, default=5, help="Maximum results to return")
    parser.add_argument("--tag", default=None, help="Filter by specific tag")
    args = parser.parse_args()

    results = search_docs(args.query, repo_root=args.repo, limit=args.limit, filter_tag=args.tag)
    print(f"=== Along KB Search: '{args.query}' ({len(results)} matches) ===")
    for i, r in enumerate(results, 1):
        tags_str = ", ".join(r["tags"]) if r["tags"] else "none"
        print(f"{i}. [{r['title']}](./{r['file']}) (Type: {r['type']}, Tags: {tags_str}, Score: {r['score']})")
        print(f"   \"{r['snippet']}...\"\n")

if __name__ == "__main__":
    main()
