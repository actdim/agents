#!/usr/bin/env python3
"""
along_commit.py - Smart, ASCII-safe, and issue-linked Conventional Committer for Along.

Features:
- Enforces clean ASCII typography before committing (cleans NBSP, ZWSP, curly quotes, etc.)
- Auto-extracts active issue from .along/ISSUES.md and appends issue reference
- Enforces or formats Conventional Commits (feat, fix, docs, refactor, test, chore)
- Supports optional --push flag
"""

import sys
import os
import re
import subprocess

def find_repo_root():
    cur = os.path.abspath(os.getcwd())
    while True:
        if os.path.exists(os.path.join(cur, ".along")) or os.path.exists(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return os.path.abspath(os.getcwd())
        cur = parent

def sanitize_typography(repo_root):
    sanitizer = os.path.join(repo_root, "scripts", "sanitize_typography.py")
    if os.path.exists(sanitizer):
        res = subprocess.run([sys.executable, sanitizer], cwd=repo_root, capture_output=True, text=True)
        if "Total files sanitized: 0" not in res.stdout and res.stdout.strip():
            print(f"-> [Typography Sanitizer] {res.stdout.strip()}")

def run_precommit_tests(repo_root):
    """Executes repository tests before allowing a commit."""
    test_hook = os.path.join(repo_root, ".along", "scripts", "test.py")
    tests_dir = os.path.join(repo_root, "tests")

    cmd = None
    if os.path.exists(test_hook):
        cmd = [sys.executable, test_hook]
    elif os.path.exists(tests_dir):
        cmd = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]
    elif os.path.exists(os.path.join(repo_root, "package.json")):
        try:
            with open(os.path.join(repo_root, "package.json"), "r", encoding="utf-8") as f:
                pkg = json.load(f)
            if "scripts" in pkg and "test" in pkg["scripts"]:
                cmd = ["npm", "test", "--", "--silent"]
        except Exception:
            pass

    if cmd:
        print(f"-> [Pre-Commit Quality Gate] Running automated tests: {' '.join(cmd)}")
        res = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[Error] Pre-commit automated tests failed!\n", file=sys.stderr)
            if res.stdout:
                print(res.stdout, file=sys.stderr)
            if res.stderr:
                print(res.stderr, file=sys.stderr)
            print("Commit aborted. Fix failing tests before committing.", file=sys.stderr)
            sys.exit(1)
        print("-> [Pre-Commit Quality Gate] All tests passed successfully.")

def get_active_issue(repo_root):
    issues_board = os.path.join(repo_root, ".along", "ISSUES.md")
    if not os.path.exists(issues_board):
        return None
    try:
        with open(issues_board, "r", encoding="utf-8") as f:
            lines = f.readlines()
        in_active = False
        for line in lines:
            if line.startswith("## Active"):
                in_active = True
                continue
            elif line.startswith("## "):
                in_active = False
                continue
            if in_active:
                m = re.search(r'\[[ ~]\]\s*`\((\w+)\)`\s*\[([^\]]+)\]', line)
                if m:
                    return {"type": m.group(1), "slug": m.group(2)}
    except Exception:
        pass
    return None

def format_commit_message(raw_msg, active_issue):
    msg = raw_msg.strip()
    # Check if already conventional commit (type(scope): message or type: message)
    conv_match = re.match(r'^(\w+)(?:\(([^)]+)\))?:\s*(.+)$', msg)
    if not conv_match and active_issue:
        itype = active_issue["type"]
        # Map Along issue types to Conventional Commits
        type_map = {"feat": "feat", "bug": "fix", "debt": "refactor", "task": "chore", "docs": "docs"}
        ctype = type_map.get(itype, "chore")
        msg = f"{ctype}: {msg}"
    
    # Append issue reference if available and not already present
    if active_issue:
        slug = active_issue["slug"]
        if slug not in msg:
            msg = f"{msg} (refs #{slug})"
            
    return msg

def main():
    repo_root = find_repo_root()
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = [a for a in sys.argv[1:] if a.startswith("-")]
    
    push = "--push" in flags or "-p" in flags
    skip_tests = "--no-verify" in flags or "-n" in flags
    all_files = "--all" in flags or "-a" in flags or len(args) > 0

    if not args:
        print("Usage: python along_commit.py \"<commit message>\" [--push] [--no-verify]")
        print("Example: python along_commit.py \"add cytoscape graph view\" -p")
        sys.exit(1)

    raw_msg = " ".join(args)
    
    print("==================================================")
    print("-> Along Smart Committer")
    print(f"   Target: {repo_root}")
    print("==================================================")

    # 1. Mandatory Pre-Commit Tests
    if not skip_tests:
        run_precommit_tests(repo_root)

    # 2. Pre-commit typography check
    sanitize_typography(repo_root)

    # 3. Extract active issue context
    active_issue = get_active_issue(repo_root)
    final_msg = format_commit_message(raw_msg, active_issue)
    
    print(f"-> Commit message: \"{final_msg}\"")

    # 3. Stage changes and commit
    try:
        subprocess.run(["git", "add", "-A"], cwd=repo_root, check=True)
        res = subprocess.run(["git", "commit", "-m", final_msg], cwd=repo_root, capture_output=True, text=True)
        if res.returncode != 0:
            if "nothing to commit" in res.stdout or "nothing to commit" in res.stderr:
                print("-> [Notice] Nothing to commit, working tree clean.")
                sys.exit(0)
            else:
                print(f"[Error] Git commit failed:\n{res.stderr}", file=sys.stderr)
                sys.exit(res.returncode)
        print(f"-> Git commit created successfully.")
        print(res.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"[Error] Git staging failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Optional Push
    if push:
        print("-> Pushing to remote repository...")
        res = subprocess.run(["git", "push"], cwd=repo_root, capture_output=True, text=True)
        if res.returncode == 0:
            print("-> Successfully pushed to remote.")
        else:
            print(f"[Warning] Git push failed:\n{res.stderr}", file=sys.stderr)

if __name__ == "__main__":
    main()

