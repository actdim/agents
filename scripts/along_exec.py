#!/usr/bin/env python3
"""
along_exec.py - Unified Command Router & Lifecycle Dispatcher for Along Protocol.

Dispatches:
1. Project Lifecycle Hooks:
   - build        -> executes .along/scripts/build.py (or auto-detects build command)
   - test         -> executes .along/scripts/test.py (or auto-detects quiet test runner)
   - dev          -> executes .along/scripts/dev.py (or auto-detects dev runner)
2. Along Protocol Tools (Direct Precursor to along CLI):
   - kb-sync      -> runs along_kb_sync.py
   - kb-search    -> runs along_kb_search.py
   - dep-scan     -> runs along_dep_scan.py
   - history-sync -> runs along_history_sync.py
   - commit       -> runs along_commit.py
   - version-bump -> runs along_version_bump.py
   - update       -> runs along_update.py
   - dash         -> runs along_dash.py
   - migrate      -> runs migrate_protocol.py
   - sanitize     -> runs sanitize_typography.py
"""

import sys
import os
import re
import json
import shutil
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Tuple

TOOL_MAPPINGS = {
    "kb-sync": "along_kb_sync.py",
    "kbsync": "along_kb_sync.py",
    "kb-search": "along_kb_search.py",
    "kbsearch": "along_kb_search.py",
    "dep-scan": "along_dep_scan.py",
    "depscan": "along_dep_scan.py",
    "history-sync": "along_history_sync.py",
    "historysync": "along_history_sync.py",
    "commit": "along_commit.py",
    "version-bump": "along_version_bump.py",
    "versionbump": "along_version_bump.py",
    "bump": "along_version_bump.py",
    "update": "along_update.py",
    "dash": "along_dash.py",
    "dashboard": "along_dash.py",
    "migrate": "migrate_protocol.py",
    "sanitize": "sanitize_typography.py",
    "typography": "sanitize_typography.py",
}

LIFECYCLE_ACTIONS = {"build", "test", "dev", "debug"}


def find_repo_root(start_dir: Optional[str] = None) -> str:
    cur = os.path.abspath(start_dir or os.getcwd())
    while True:
        if (
            os.path.exists(os.path.join(cur, ".along"))
            or os.path.exists(os.path.join(cur, ".git"))
            or os.path.exists(os.path.join(cur, "AGENTS.md"))
        ):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return os.path.abspath(start_dir or os.getcwd())
        cur = parent


def resolve_tool_script(script_name: str, repo_root: str) -> Optional[str]:
    """Resolves an Along tool script using hierarchical search."""
    exec_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(exec_dir, script_name),
        os.path.join(repo_root, "scripts", script_name),
        os.path.expanduser(f"~/.along/bin/{script_name}"),
        os.path.expanduser(f"~/.config/opencode/actdim-along/{script_name}"),
        os.path.expanduser(f"~/.gemini/config/scripts/{script_name}"),
        os.path.expanduser(f"~/.claude/scripts/{script_name}"),
        os.path.expanduser(f"~/.codex/scripts/{script_name}"),
    ]
    for p in candidates:
        if os.path.isfile(p):
            return os.path.abspath(p)
    return None


def get_lifecycle_script_path(repo_root: str, action: str) -> str:
    scripts_dir = os.path.join(repo_root, ".along", "scripts")
    for ext in [".py", ".sh", ".ps1", ".bat"]:
        p = os.path.join(scripts_dir, f"{action}{ext}")
        if os.path.exists(p):
            return p
    return os.path.join(scripts_dir, f"{action}.py")


def synthesize_lifecycle_script(script_path: str, content: str):
    os.makedirs(os.path.dirname(script_path), exist_ok=True)
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(content)
    try:
        os.chmod(script_path, 0o755)
    except Exception:
        pass
    print(f"-> Created lifecycle hook: {script_path}")


def detect_lifecycle_action(repo_root: str, action: str) -> Tuple[Optional[str], bool]:
    # Node.js
    pkg_json = os.path.join(repo_root, "package.json")
    if os.path.exists(pkg_json):
        try:
            with open(pkg_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            scripts = data.get("scripts", {})
            if action == "build" and "build" in scripts:
                return "npm run build", True
            elif action == "test":
                return "npm test -- --silent" if "test" in scripts else "npm test", True
            elif action == "dev":
                cmd = "npm run dev" if "dev" in scripts else ("npm start" if "start" in scripts else None)
                if cmd:
                    return cmd, True
        except Exception:
            pass

    # Rust
    if os.path.exists(os.path.join(repo_root, "Cargo.toml")):
        if action == "build":
            return "cargo build", True
        elif action == "test":
            return "cargo test -q", True
        elif action == "dev":
            return "cargo run", True

    # .NET
    if glob_files(repo_root, "*.csproj") or os.path.exists(os.path.join(repo_root, "Directory.Build.props")):
        if action == "build":
            return "dotnet build -v q", True
        elif action == "test":
            return "dotnet test -v q", True
        elif action == "dev":
            return "dotnet run", True

    # Python
    if os.path.exists(os.path.join(repo_root, "pyproject.toml")) or os.path.exists(os.path.join(repo_root, "setup.py")):
        if action == "build":
            return "python -m build", True
        elif action == "test":
            return "pytest -q" if shutil.which("pytest") else "python -m unittest discover tests -q", True
        elif action == "dev":
            for main_file in ["main.py", "app.py", "server.py"]:
                if os.path.exists(os.path.join(repo_root, main_file)):
                    return f"python {main_file}", True

    return None, False


def glob_files(root: str, pattern: str) -> bool:
    import glob
    return bool(glob.glob(os.path.join(root, pattern)))


def print_help():
    print("""Along Command Router (along_exec.py) [v2.1.3]

Usage:
  python scripts/along_exec.py <command> [args...]

Lifecycle Commands (project hooks):
  build          Execute project build (.along/scripts/build.py or auto-detected)
  test           Execute project tests (.along/scripts/test.py or auto-detected)
  dev            Launch project dev server (.along/scripts/dev.py or auto-detected)

Along Protocol Tools:
  kb-sync        Synchronize and compile Knowledge Base in docs/
  kb-search      Search Knowledge Base and project memory
  dep-scan       Scan multi-project dependencies and AI rules
  history-sync   Reconcile Git commit history and synthesize entities
  commit         Safe Conventional Commits with typography sanitization
  version-bump   Increment project version and create release commit
  update         Update Along protocol and skills across workspaces
  dash           Launch executive dashboard and OpenAPI service
  migrate        Run protocol migration and YAML front-matter fixes
  sanitize       Sanitize non-ASCII typography across repository files
""")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower().strip()
    extra_args = sys.argv[2:]
    repo_root = find_repo_root()

    # 1. Check if command is an Along Protocol Tool
    if cmd in TOOL_MAPPINGS:
        script_name = TOOL_MAPPINGS[cmd]
        script_path = resolve_tool_script(script_name, repo_root)
        if not script_path:
            print(f"[Error] Could not locate Along tool script: {script_name}", file=sys.stderr)
            print(f"Searched in local scripts/ and global Along home.", file=sys.stderr)
            sys.exit(1)

        # For dash, use uv run if available
        if script_name == "along_dash.py":
            uv_bin = shutil.which("uv")
            if uv_bin:
                full_cmd = [uv_bin, "run", script_path] + extra_args
                res = subprocess.run(full_cmd, cwd=repo_root)
                sys.exit(res.returncode)

        full_cmd = [sys.executable, script_path] + extra_args
        res = subprocess.run(full_cmd, cwd=repo_root)
        sys.exit(res.returncode)

    # 2. Check if command is a Lifecycle Hook (build / test / dev / debug)
    if cmd in LIFECYCLE_ACTIONS:
        script_file = get_lifecycle_script_path(repo_root, cmd)

        if os.path.exists(script_file):
            with open(script_file, "r", encoding="utf-8", errors="ignore") as f:
                header = f.read(500)
            if "# Status: unconfigured" in header:
                print(f"[Notice] {script_file} is unconfigured. Please customize it for this repository.")

            print(f"-> Executing .along/scripts/{os.path.basename(script_file)}...")
            if script_file.endswith(".py"):
                res = subprocess.run([sys.executable, script_file] + extra_args, cwd=repo_root)
            else:
                res = subprocess.run([script_file] + extra_args, cwd=repo_root, shell=True)
            sys.exit(res.returncode)

        # Auto-Detection and Non-Destructive Synthesis
        detected_cmd, verified = detect_lifecycle_action(repo_root, cmd)

        if detected_cmd and verified:
            status_tag = "verified"
            py_content = f'''#!/usr/bin/env python3
# Status: {status_tag}
# Auto-generated by Along for {cmd}
import sys, subprocess, os

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    cmd = "{detected_cmd}"
    extra = " ".join(sys.argv[1:])
    full_cmd = f"{{cmd}} {{extra}}".strip()
    print(f"-> Running: {{full_cmd}}")
    res = subprocess.run(full_cmd, shell=True, cwd=repo_root)
    sys.exit(res.returncode)

if __name__ == "__main__":
    main()
'''
            synthesize_lifecycle_script(script_file, py_content)
            print(f"-> Running: {detected_cmd}")
            res = subprocess.run(f"{detected_cmd} {' '.join(extra_args)}".strip(), shell=True, cwd=repo_root)
            sys.exit(res.returncode)
        else:
            status_tag = "unconfigured"
            py_content = f'''#!/usr/bin/env python3
# Status: {status_tag}
# Template for {cmd} in this repository
import sys, subprocess, os

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print("[Notice] Please configure {cmd} command in .along/scripts/{cmd}.py")

if __name__ == "__main__":
    main()
'''
            synthesize_lifecycle_script(script_file, py_content)
            print(f"[Notice] Created unconfigured template: {script_file}")
            print(f"Please customize .along/scripts/{cmd}.py for your repository build/test configuration.")
            sys.exit(0)

    print(f"[Error] Unknown command: '{cmd}'. Run 'python scripts/along_exec.py --help' for available commands.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()


