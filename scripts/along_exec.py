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
    "feedback": "along_feedback.py",
    "diagnostics": "along_feedback.py",
    "telemetry": "along_feedback.py",
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


def try_record_incident(component: str, error_message: str, stack_trace: str = "", command: str = "", repo_root: str = ""):
    """Safely traps and records internal Along exceptions into ~/.along/diagnostics/ without crashing."""
    try:
        feedback_script = resolve_tool_script("along_feedback.py", repo_root)
        if feedback_script and os.path.exists(feedback_script):
            scripts_dir = os.path.dirname(feedback_script)
            if scripts_dir not in sys.path:
                sys.path.insert(0, scripts_dir)
            import along_feedback
            along_feedback.DiagnosticsStore.record_incident(
                component=component,
                error_message=error_message,
                event_type="script_crash",
                stack_trace=stack_trace,
                command=command,
                repo_root=repo_root
            )
    except Exception:
        pass


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
    print("""Along Command Router (along_exec.py) [v2.1.5]

Usage:
  python scripts/along_exec.py <command> [subcommand] [args...]

Lifecycle Commands (project hooks):
  build          Execute project build (.along/scripts/build.py or auto-detected)
  test           Execute project tests (.along/scripts/test.py or auto-detected)
  dev            Launch project dev server (.along/scripts/dev.py or auto-detected)

Entity Management Commands:
  issue create <type> <slug> --title "Title" [--priority high|medium|low] [--tags "t1,t2"]
  issue done <slug>
  issue list
  session create <slug> --summary "Summary" [--issues "slug1,slug2"] [--decisions "#001"]
  decision add <num> "Title" --context "Why" --decision "What" --consequences "Tradeoffs"
  scratch init <slug>
  scratch purge <slug>

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
  feedback       Global diagnostics, error capture, and feedback dispatch (Telegram/Webhook/File)
""")


def handle_issue_command(repo_root: str, args: List[str]):
    if not args or args[0] in ("-h", "--help", "help"):
        print("Usage: along_exec.py issue [create|done|list] [args...]")
        sys.exit(0)

    subcmd = args[0].lower()
    from datetime import datetime

    issues_dir = os.path.join(repo_root, ".along", "ISSUES")
    done_dir = os.path.join(issues_dir, "done")
    os.makedirs(issues_dir, exist_ok=True)
    os.makedirs(done_dir, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")

    if subcmd == "create":
        if len(args) < 3:
            print("[Error] Usage: along_exec.py issue create <type> <slug> --title \"Title\" [--priority high|medium|low] [--tags \"tag1,tag2\"]", file=sys.stderr)
            sys.exit(1)
        itype = args[1].lower()
        islug = args[2].lower()
        title = islug.replace("-", " ").capitalize()
        priority = "medium"
        tags = []

        i = 3
        while i < len(args):
            if args[i] in ("--title", "-t") and i + 1 < len(args):
                title = args[i + 1]
                i += 2
            elif args[i] in ("--priority", "-p") and i + 1 < len(args):
                priority = args[i + 1]
                i += 2
            elif args[i] in ("--tags",) and i + 1 < len(args):
                tags = [t.strip() for t in args[i + 1].split(",") if t.strip()]
                i += 2
            else:
                i += 1

        target_file = os.path.join(issues_dir, f"{itype}--{islug}.md")
        tags_str = f"[{', '.join(tags)}]" if tags else "[]"
        content = f"""---
protocol: along
slug: {islug}
type: {itype}
status: open
priority: {priority}
created: {today}
updated: {today}
agent: antigravity
tags: {tags_str}
milestone: v2.1.0-along
blocked_by: []
related: []
---

# {title}

Describe the feature, requirements, and background context here.

## Acceptance Criteria
- [ ] Task requirement 1
- [ ] Automated tests passing
"""
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"-> Created issue: {target_file}")

        # Update ISSUES.md
        issues_board = os.path.join(repo_root, ".along", "ISSUES.md")
        if os.path.exists(issues_board):
            with open(issues_board, "r", encoding="utf-8") as f:
                b_content = f.read()
            entry = f"- [ ] `({itype})` [{islug}](file://.along/ISSUES/{itype}--{islug}.md)"
            if entry not in b_content:
                b_content = b_content.replace("## Active\n", f"## Active\n{entry}\n")
                with open(issues_board, "w", encoding="utf-8") as f:
                    f.write(b_content)
                print(f"-> Updated .along/ISSUES.md")
        sys.exit(0)

    elif subcmd == "done":
        if len(args) < 2:
            print("[Error] Usage: along_exec.py issue done <slug>", file=sys.stderr)
            sys.exit(1)
        islug = args[1].lower()
        
        # Locate issue file
        found_file = None
        for f in os.listdir(issues_dir):
            if f.endswith(f"--{islug}.md") and os.path.isfile(os.path.join(issues_dir, f)):
                found_file = os.path.join(issues_dir, f)
                break

        if not found_file:
            print(f"[Error] Issue '{islug}' not found in {issues_dir}", file=sys.stderr)
            sys.exit(1)

        filename = os.path.basename(found_file)
        dest_file = os.path.join(done_dir, filename)

        with open(found_file, "r", encoding="utf-8") as f:
            content = f.read()

        content = re.sub(r'status:\s*\w+', 'status: done', content)
        content = re.sub(r'updated:\s*\S+', f'updated: {today}', content)
        if "completed:" not in content:
            content = re.sub(r'(status:\s*done\n)', f'\\1completed: {today}\n', content)
        else:
            content = re.sub(r'completed:\s*\S+', f'completed: {today}', content)

        with open(dest_file, "w", encoding="utf-8") as f:
            f.write(content)
        os.remove(found_file)
        print(f"-> Moved issue to done: {dest_file}")

        # Update ISSUES.md
        issues_board = os.path.join(repo_root, ".along", "ISSUES.md")
        if os.path.exists(issues_board):
            with open(issues_board, "r", encoding="utf-8") as f:
                b_content = f.read()
            # Remove from Active
            b_content = re.sub(rf'- \[[ ~]\] `\(\w+\)` \[{re.escape(islug)}\]\([^\)]+\)\n?', '', b_content)
            # Add to Done
            itype = filename.split("--")[0]
            done_entry = f"- [x] `({itype})` [{islug}](file://.along/ISSUES/done/{filename})"
            if done_entry not in b_content:
                b_content = b_content.replace("## Done (recent)\n", f"## Done (recent)\n{done_entry}\n")
            with open(issues_board, "w", encoding="utf-8") as f:
                f.write(b_content)
            print(f"-> Updated .along/ISSUES.md")
        sys.exit(0)

    elif subcmd == "list":
        print(f"-> Active issues in {issues_dir}:")
        count = 0
        for f in os.listdir(issues_dir):
            if f.endswith(".md") and os.path.isfile(os.path.join(issues_dir, f)):
                print(f"   - {f}")
                count += 1
        print(f"Total active issues: {count}")
        sys.exit(0)


def handle_session_command(repo_root: str, args: List[str]):
    if not args or args[0] in ("-h", "--help", "help"):
        print("Usage: along_exec.py session create <slug> --summary \"Summary text\" [--issues \"slug1,slug2\"] [--decisions \"#001\"]")
        sys.exit(0)

    subcmd = args[0].lower()
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    year = datetime.now().strftime("%Y")
    sessions_dir = os.path.join(repo_root, ".along", "SESSIONS", year)
    os.makedirs(sessions_dir, exist_ok=True)

    if subcmd == "create":
        if len(args) < 2:
            print("[Error] Usage: along_exec.py session create <slug> --summary \"Summary\"", file=sys.stderr)
            sys.exit(1)
        slug = args[1].lower()
        summary = "Work session"
        issues = []
        decisions = []

        i = 2
        while i < len(args):
            if args[i] in ("--summary", "-s") and i + 1 < len(args):
                summary = args[i + 1]
                i += 2
            elif args[i] in ("--issues", "-i") and i + 1 < len(args):
                issues = [iss.strip() for iss in args[i + 1].split(",") if iss.strip()]
                i += 2
            elif args[i] in ("--decisions", "-d") and i + 1 < len(args):
                decisions = [d.strip() for d in args[i + 1].split(",") if d.strip()]
                i += 2
            else:
                i += 1

        target_file = os.path.join(sessions_dir, f"{today}--{slug}.md")
        issues_str = f"[{', '.join(issues)}]" if issues else "[]"
        decisions_str = f"[{', '.join([f'\"{d}\"' for d in decisions])}]" if decisions else "[]"

        content = f"""---
protocol: along
date: {today}
slug: {slug}
agent: antigravity
branch: main
commit: pending
summary: {summary}
milestone: v2.1.0-along
issues_advanced: []
issues_completed: {issues_str}
decisions: {decisions_str}
risks_logged: []
spikes_conducted: []
---

# Session: {slug.replace('-', ' ').capitalize()}

## Summary
{summary}

## Work Completed
- Document key tasks and achievements.

## Code Review & Blast Radius
- Automated tests verified and passing.
"""
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"-> Created session log: {target_file}")

        # Update HISTORY.md
        history_file = os.path.join(repo_root, ".along", "HISTORY.md")
        if os.path.exists(history_file):
            with open(history_file, "r", encoding="utf-8") as f:
                h_content = f.read()
            entry = f"{today} - {slug} - antigravity - {summary} - [.along/SESSIONS/{year}/{today}--{slug}.md](file://.along/SESSIONS/{year}/{today}--{slug}.md)"
            if entry not in h_content:
                h_content = h_content.strip() + f"\n{entry}\n"
                with open(history_file, "w", encoding="utf-8") as f:
                    f.write(h_content)
                print(f"-> Appended history entry to .along/HISTORY.md")
        sys.exit(0)


def handle_decision_command(repo_root: str, args: List[str]):
    if not args or args[0] in ("-h", "--help", "help"):
        print("Usage: along_exec.py decision add <num> \"Title\" --context \"Context\" --decision \"Decision\" --consequences \"Tradeoffs\"")
        sys.exit(0)

    subcmd = args[0].lower()
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    if subcmd == "add":
        if len(args) < 3:
            print("[Error] Usage: along_exec.py decision add <num> \"Title\" --context \"Why\" --decision \"What\" --consequences \"Consequences\"", file=sys.stderr)
            sys.exit(1)
        num = args[1].lstrip("#")
        title = args[2]
        context = ""
        decision = ""
        consequences = ""

        i = 3
        while i < len(args):
            if args[i] == "--context" and i + 1 < len(args):
                context = args[i + 1]
                i += 2
            elif args[i] == "--decision" and i + 1 < len(args):
                decision = args[i + 1]
                i += 2
            elif args[i] == "--consequences" and i + 1 < len(args):
                consequences = args[i + 1]
                i += 2
            else:
                i += 1

        dec_file = os.path.join(repo_root, ".along", "DECISIONS.md")
        entry = f"""
## #{num} - {title}
- Date: {today}
- Status: accepted
- Context: {context}
- Decision: {decision}
- Consequences: {consequences}
"""
        with open(dec_file, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"-> Appended Decision #{num} to .along/DECISIONS.md")
        sys.exit(0)


def handle_scratch_command(repo_root: str, args: List[str]):
    if not args or args[0] in ("-h", "--help", "help"):
        print("Usage: along_exec.py scratch [init|purge] <slug>")
        sys.exit(0)

    subcmd = args[0].lower()
    if len(args) < 2:
        print("[Error] Usage: along_exec.py scratch [init|purge] <slug>", file=sys.stderr)
        sys.exit(1)
    slug = args[1].lower()
    scratch_dir = os.path.join(repo_root, ".along", ".session", slug)

    if subcmd == "init":
        os.makedirs(scratch_dir, exist_ok=True)
        plan_file = os.path.join(scratch_dir, "plan.md")
        if not os.path.exists(plan_file):
            with open(plan_file, "w", encoding="utf-8") as f:
                f.write(f"# Living Plan: {slug}\n\n## Steps\n- [ ] Step 1: Initialize\n")
        print(f"-> Initialized scratchpad: {scratch_dir}")
        sys.exit(0)
    elif subcmd == "purge":
        if os.path.exists(scratch_dir):
            shutil.rmtree(scratch_dir)
            print(f"-> Purged scratchpad: {scratch_dir}")
        else:
            print(f"-> Scratchpad not found (already clean): {scratch_dir}")
        sys.exit(0)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower().strip()
    extra_args = sys.argv[2:]
    repo_root = find_repo_root()

    # 1. Native Entity Management Subcommands
    if cmd == "issue":
        handle_issue_command(repo_root, extra_args)
    elif cmd == "session":
        handle_session_command(repo_root, extra_args)
    elif cmd == "decision":
        handle_decision_command(repo_root, extra_args)
    elif cmd == "scratch":
        handle_scratch_command(repo_root, extra_args)

    # 2. Check if command is an Along Protocol Tool
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

    # 3. Check if command is a Lifecycle Hook (build / test / dev / debug)
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


