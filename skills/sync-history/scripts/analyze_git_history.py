#!/usr/bin/env python3
"""
analyze_git_history.py - Extract structured git commit history, tags, diffstats,
and identify commits not yet mapped to .agents/SESSIONS/ or .agents/ISSUES/.
"""

import os
import re
import sys
import json
import subprocess
import glob

def run_git_cmd(args, cwd=None):
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=cwd or os.getcwd(),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception as e:
        print(f"Git error: {e}", file=sys.stderr)
    return ""

def get_mapped_commits(agents_dir):
    mapped_commits = set()
    session_files = glob.glob(os.path.join(agents_dir, "SESSIONS", "**", "*.md"), recursive=True)
    for sf in session_files:
        with open(sf, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        m = re.search(r"^commit:\s*([a-fA-F0-9]+)", content, re.MULTILINE)
        if m:
            mapped_commits.add(m.group(1).strip()[:7])
    return mapped_commits

def get_git_tags(repo_root):
    tags_raw = run_git_cmd(["tag", "-l", "--sort=-creatordate", "--format=%(refname:short)|%(creatordate:short)|%(subject)"], repo_root)
    tags = []
    for line in tags_raw.splitlines():
        if not line.strip(): continue
        parts = line.split("|", 2)
        if len(parts) >= 2:
            tags.append({
                "tag": parts[0],
                "date": parts[1],
                "subject": parts[2] if len(parts) > 2 else ""
            })
    return tags

def extract_commits(repo_root, max_count=100, since_commit=None):
    cmd = ["log", f"-n{max_count}", "--pretty=format:%H|%h|%an|%ad|%s", "--date=short"]
    if since_commit:
        cmd.append(f"{since_commit}..HEAD")

    raw_log = run_git_cmd(cmd, repo_root)
    commits = []
    for line in raw_log.splitlines():
        if not line.strip(): continue
        parts = line.split("|", 4)
        if len(parts) == 5:
            full_hash, short_hash, author, date, subject = parts
            
            # Classify conventional commit prefix
            c_type = "feat"
            lower_s = subject.lower()
            if lower_s.startswith("fix") or "bug" in lower_s:
                c_type = "bug"
            elif lower_s.startswith("refactor") or "debt" in lower_s or "clean" in lower_s:
                c_type = "debt"
            elif lower_s.startswith("docs") or "readme" in lower_s:
                c_type = "docs"
            elif lower_s.startswith("test") or "chore" in lower_s:
                c_type = "task"

            commits.append({
                "full_hash": full_hash,
                "short_hash": short_hash,
                "author": author,
                "date": date,
                "subject": subject,
                "inferred_type": c_type
            })
    return commits

def main():
    repo_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    agents_dir = os.path.join(repo_root, ".agents")

    mapped = get_mapped_commits(agents_dir) if os.path.exists(agents_dir) else set()
    tags = get_git_tags(repo_root)
    commits = extract_commits(repo_root, max_count=100)

    unmapped = []
    for c in commits:
        if c["short_hash"] not in mapped and not any(c["full_hash"].startswith(m) for m in mapped):
            unmapped.append(c)

    result = {
        "repo_root": repo_root,
        "total_tags": len(tags),
        "tags": tags[:10],
        "total_commits_scanned": len(commits),
        "mapped_commits_count": len(mapped),
        "unmapped_commits_count": len(unmapped),
        "unmapped_commits": unmapped
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
