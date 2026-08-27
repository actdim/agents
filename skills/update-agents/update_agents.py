#!/usr/bin/env python3
"""
update_agents.py - Automated one-liner updater engine for ACTDIM-AGENTS-PROTOCOL.

Recursively discovers and updates existing agent contexts in repository root and subdirectories:
  1. Checks protocol versions across local repo, global installations, and GitHub.
  2. Updates global skills installation if a newer release exists.
  3. Walks repository tree from root to find all folders that ALREADY contain AGENTS.md or .agents/.
  4. Selectively refreshes protocol blocks and runs migration engine only where agents are already present.
  5. Leaves clean directories untouched (anti-pollution guarantee).

Usage:
    python scripts/update_agents.py [TARGET_REPO_ROOT] [OPTIONS]
    Options:
      --check-only      Only inspect versions and print report without making changes.
      --dry-run         Simulate updates and migrations without writing files.
      --force           Force reinstall/refresh even if versions match.
      --local-only      Skip remote GitHub check, use only local global installation.
"""

import os
import re
import sys
import shutil
import urllib.request
import subprocess
from datetime import datetime

REMOTE_GIT_URL = "https://github.com/actdim/agents.git"
REMOTE_RAW_URL = "https://raw.githubusercontent.com/actdim/agents/main/AGENTS.md"
NETWORK_TIMEOUT_SECS = 4

def parse_semver(v_str):
    if not v_str:
        return (0, 0, 0)
    cleaned = v_str.strip().lstrip("v").split("-")[0]
    parts = cleaned.split(".")
    try:
        return tuple(int(p) for p in parts[:3])
    except (ValueError, IndexError):
        return (0, 0, 0)

def semver_to_str(sem_tuple):
    return f"{sem_tuple[0]}.{sem_tuple[1]}.{sem_tuple[2]}"

def detect_repo_version(repo_root):
    agents_md = os.path.join(repo_root, "AGENTS.md")
    if os.path.exists(agents_md):
        try:
            with open(agents_md, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            m = re.search(r"ACTDIM-AGENTS-PROTOCOL v(\d+\.\d+\.\d+)", content)
            if m:
                return m.group(1)
        except Exception:
            pass
    return None

def get_global_skill_paths():
    user_home = os.path.expanduser("~")
    paths = [
        os.path.join(user_home, ".gemini", "config", "skills", "init-agents", "protocol.md"),
        os.path.join(user_home, ".claude", "skills", "init-agents", "protocol.md"),
        os.path.join(user_home, ".codex", "skills", "init-agents", "protocol.md"),
        os.path.join(user_home, ".config", "opencode", "actdim-agents", "protocol.md"),
    ]
    return paths

def detect_global_version():
    highest = (0, 0, 0)
    for p in get_global_skill_paths():
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    c = f.read()
                m = re.search(r"ACTDIM-AGENTS-PROTOCOL v(\d+\.\d+\.\d+)", c)
                if m:
                    ver = parse_semver(m.group(1))
                    if ver > highest:
                        highest = ver
            except Exception:
                pass
    return semver_to_str(highest) if highest > (0, 0, 0) else None

def detect_remote_version():
    try:
        res = subprocess.run(
            ["git", "ls-remote", "--tags", "--refs", REMOTE_GIT_URL],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=NETWORK_TIMEOUT_SECS
        )
        if res.returncode == 0 and res.stdout:
            tags = re.findall(r"refs/tags/v?(\d+\.\d+\.\d+)", res.stdout)
            if tags:
                sorted_tags = sorted(tags, key=parse_semver, reverse=True)
                return sorted_tags[0]
    except Exception:
        pass

    try:
        req = urllib.request.Request(
            REMOTE_RAW_URL,
            headers={"User-Agent": "actdim-agents-updater/1.5"}
        )
        with urllib.request.urlopen(req, timeout=NETWORK_TIMEOUT_SECS) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
            m = re.search(r"ACTDIM-AGENTS-PROTOCOL v(\d+\.\d+\.\d+)", raw)
            if m:
                return m.group(1)
    except Exception:
        pass

    return None

def is_dev_repo(repo_root):
    is_agents_repo = (
        os.path.exists(os.path.join(repo_root, "skills", "init-agents", "SKILL.md")) and
        os.path.exists(os.path.join(repo_root, "skills", "bump-version", "SKILL.md"))
    )
    return is_agents_repo

def update_global_from_git(dry_run=False):
    print("-> Synchronizing global skills from remote GitHub repository...")
    cache_dir = os.path.expanduser("~/.cache/actdim-agents/repo")
    if dry_run:
        print(f"   [DRY-RUN] Would git clone/pull {REMOTE_GIT_URL} into {cache_dir} and run install script.")
        return True

    try:
        if os.path.exists(os.path.join(cache_dir, ".git")):
            subprocess.run(["git", "-C", cache_dir, "fetch", "--all", "--tags"], check=True, timeout=15)
            subprocess.run(["git", "-C", cache_dir, "reset", "--hard", "origin/main"], check=True, timeout=10)
        else:
            os.makedirs(os.path.dirname(cache_dir), exist_ok=True)
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir, ignore_errors=True)
            subprocess.run(["git", "clone", "--depth", "1", REMOTE_GIT_URL, cache_dir], check=True, timeout=20)

        # Run installation script from cached clone
        if sys.platform == "win32":
            ps1_script = os.path.join(cache_dir, "install.ps1")
            cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps1_script, "-Target", "all"]
        else:
            sh_script = os.path.join(cache_dir, "install.sh")
            cmd = ["bash", sh_script]

        res = subprocess.run(cmd, check=True)
        return res.returncode == 0
    except Exception as e:
        print(f"   [ERROR] Failed to update global skills from GitHub: {e}")
        return False

def install_global_from_local(repo_root, dry_run=False):
    print("-> Installing skills locally from dev repository...")
    if dry_run:
        print("   [DRY-RUN] Would run install.ps1/install.sh from current dev repo.")
        return True
    try:
        if sys.platform == "win32":
            ps1_script = os.path.join(repo_root, "install.ps1")
            cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps1_script, "-Target", "all"]
        else:
            sh_script = os.path.join(repo_root, "install.sh")
            cmd = ["bash", sh_script]

        res = subprocess.run(cmd, check=True)
        return res.returncode == 0
    except Exception as e:
        print(f"   [ERROR] Local installer failed: {e}")
        return False

def find_existing_agent_contexts(repo_root):
    """
    Recursively discovers all directories containing AGENTS.md or .agents/.
    Skips ignored build/cache/dependency directories.
    Returns list of absolute directory paths sorted by depth (root first).
    """
    contexts = []
    ignored = {
        '.git', 'node_modules', 'dist', 'build', '.venv', 'venv',
        'bin', 'obj', '.cache', 'target', 'vendor', '.gemini', '.claude', '.codex'
    }

    for root, dirs, files in os.walk(repo_root):
        # Filter directories in-place to avoid descending into ignored folders
        dirs[:] = [d for d in dirs if d not in ignored and not d.startswith('.')]

        has_agents_md = "AGENTS.md" in files
        has_agents_dir = os.path.isdir(os.path.join(root, ".agents"))

        if has_agents_md or has_agents_dir:
            contexts.append(os.path.abspath(root))

    # Sort by path depth (root first)
    contexts.sort(key=lambda p: (len(p.split(os.sep)), p))
    return contexts

def apply_migration_to_context(ctx_dir, protocol_text, migrate_script, is_root=True, ancestor_root=None, dry_run=False):
    rel_display = os.path.relpath(ctx_dir, os.getcwd())
    if rel_display == ".":
        rel_display = "repository root"

    print(f"-> Updating agent context: {rel_display} ({ctx_dir})")
    if dry_run:
        print(f"   [DRY-RUN] Would refresh protocol block and run migration engine on {ctx_dir}.")
        return True

    # 1. Prepare managed protocol block for AGENTS.md
    agents_md = os.path.join(ctx_dir, "AGENTS.md")

    if is_root or not ancestor_root:
        begin_marker = "<!-- BEGIN ACTDIM-AGENTS-PROTOCOL root (managed by init-agents - do not edit by hand) -->"
        end_marker = "<!-- END ACTDIM-AGENTS-PROTOCOL -->"
        block = f"{begin_marker}\n{protocol_text}\n{end_marker}"
    else:
        # Subproject referencing ancestor AGENTS.md
        rel_path = os.path.relpath(os.path.join(ancestor_root, "AGENTS.md"), ctx_dir).replace('\\', '/')
        begin_marker = f"<!-- BEGIN ACTDIM-AGENTS-PROTOCOL ref={rel_path} (managed by init-agents - do not edit by hand) -->"
        end_marker = "<!-- END ACTDIM-AGENTS-PROTOCOL -->"
        block = (
            f"{begin_marker}\n"
            f"This folder belongs to a repository that uses the ACTDIM-AGENTS structure. The full working\n"
            f"guidance + agent-context protocol live once in the nearest ancestor `AGENTS.md` (`{rel_path}`) -\n"
            f"read it there. This folder keeps its OWN `.agents/` state; use the nearest one.\n"
            f"Only this folder's specifics follow.\n"
            f"{end_marker}"
        )

    # 2. Update AGENTS.md if it exists (or if this is the root context)
    if os.path.exists(agents_md):
        with open(agents_md, "r", encoding="utf-8") as f:
            existing = f.read()
        pattern = re.compile(
            r"<!-- BEGIN ACTDIM-AGENTS-PROTOCOL.*?-->.*?<!-- END ACTDIM-AGENTS-PROTOCOL -->",
            re.DOTALL
        )
        if pattern.search(existing):
            new_content = pattern.sub(block, existing)
        else:
            new_content = block + "\n\n" + existing
        with open(agents_md, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"   [OK] Refreshed managed protocol block in {os.path.basename(agents_md)}.")
    elif is_root:
        with open(agents_md, "w", encoding="utf-8") as f:
            f.write(block + "\n\n## Project specifics\n\n- Add project conventions here.\n")
        print("   [OK] Created root AGENTS.md with managed protocol block.")

    # 3. Run migrate_protocol.py if .agents/ exists in this context
    agents_dir = os.path.join(ctx_dir, ".agents")
    if os.path.isdir(agents_dir):
        if migrate_script:
            print(f"   Executing migration engine on .agents/ in {rel_display}...")
            res = subprocess.run([sys.executable, migrate_script, ctx_dir])
            if res.returncode != 0:
                print(f"   [WARN] Migration engine returned code {res.returncode} for {ctx_dir}")
        else:
            print("   [WARN] migrate_protocol.py not found; skipping entity structure migration.")

    return True

def run_update(repo_root, check_only=False, dry_run=False, force=False, local_only=False):
    repo_root = os.path.abspath(repo_root)
    print("==================================================")
    print("-> ACTDIM-AGENTS One-Liner Updater (/update-agents)")
    print(f"   Target Repository: {repo_root}")
    print("==================================================")

    v_repo_str = detect_repo_version(repo_root)
    v_global_str = detect_global_version()
    v_remote_str = None if local_only else detect_remote_version()

    v_repo = parse_semver(v_repo_str) if v_repo_str else (0, 0, 0)
    v_global = parse_semver(v_global_str) if v_global_str else (0, 0, 0)
    v_remote = parse_semver(v_remote_str) if v_remote_str else (0, 0, 0)

    print(f"   Repository Version: v{v_repo_str or 'none'}")
    print(f"   Global Version:     v{v_global_str or 'none'}")
    print(f"   Remote Git Version: v{v_remote_str or ('skipped' if local_only else 'unreachable')}")
    print("--------------------------------------------------")

    if check_only:
        print("-> [Check-Only Mode] No modifications made.")
        return

    is_dev = is_dev_repo(repo_root)

    # Determine highest available target version
    if is_dev:
        print("-> [Dev Repo Detected] Working inside actdim-agents repository.")
        install_global_from_local(repo_root, dry_run=dry_run)
    else:
        # Check if remote has a newer version than locally installed global
        if v_remote > v_global or (force and v_remote > (0, 0, 0)):
            print(f"-> Remote version (v{v_remote_str}) is newer than global (v{v_global_str}).")
            success = update_global_from_git(dry_run=dry_run)
            if not success:
                print("   [WARN] Falling back to existing global installation.")
        elif v_global > (0, 0, 0):
            print(f"-> Global installation (v{v_global_str}) is up-to-date.")
        else:
            if v_remote > (0, 0, 0):
                print("-> No global installation detected. Installing from remote git...")
                update_global_from_git(dry_run=dry_run)
            else:
                print("   [ERROR] No global installation and remote is unreachable.")
                return

    # Locate protocol.md source
    protocol_src = None
    local_proto = os.path.join(repo_root, "skills", "init-agents", "protocol.md")
    if os.path.exists(local_proto):
        protocol_src = local_proto
    else:
        for p in get_global_skill_paths():
            if os.path.exists(p):
                protocol_src = p
                break

    if not protocol_src:
        print("   [ERROR] Could not locate protocol.md in local repo or global skills.")
        return

    with open(protocol_src, "r", encoding="utf-8") as f:
        protocol_text = f.read().strip()

    # Locate migrate_protocol.py
    migrate_script = None
    local_mig = os.path.join(repo_root, "scripts", "migrate_protocol.py")
    if os.path.exists(local_mig):
        migrate_script = local_mig
    else:
        user_home = os.path.expanduser("~")
        cand_scripts = [
            os.path.join(user_home, ".gemini", "config", "skills", "init-agents", "migrate_protocol.py"),
            os.path.join(user_home, ".claude", "skills", "init-agents", "migrate_protocol.py"),
            os.path.join(user_home, ".codex", "skills", "init-agents", "migrate_protocol.py"),
            os.path.join(user_home, ".config", "opencode", "actdim-agents", "migrate_protocol.py"),
        ]
        for c in cand_scripts:
            if os.path.exists(c):
                migrate_script = c
                break

    # Discover all existing agent contexts in the repository
    print("-> Discovering active agent contexts in repository...")
    contexts = find_existing_agent_contexts(repo_root)

    if not contexts:
        print("   [Note] No existing AGENTS.md or .agents/ found in repository.")
        print("   Run /init-agents to scaffold agent context.")
        return

    print(f"   Found {len(contexts)} active agent context(s):")
    for c in contexts:
        rel = os.path.relpath(c, repo_root)
        print(f"     - {rel if rel != '.' else '<root>'}")

    # Determine root context
    root_context = repo_root if repo_root in contexts else contexts[0]

    for ctx in contexts:
        is_root = (ctx == root_context)
        ancestor = root_context if not is_root else None
        apply_migration_to_context(
            ctx_dir=ctx,
            protocol_text=protocol_text,
            migrate_script=migrate_script,
            is_root=is_root,
            ancestor_root=ancestor,
            dry_run=dry_run
        )

    print("==================================================")
    print(f"-> [OK] Successfully updated {len(contexts)} agent context(s) across repository!")

if __name__ == "__main__":
    target = os.getcwd()
    check_only_flag = "--check-only" in sys.argv
    dry_run_flag = "--dry-run" in sys.argv
    force_flag = "--force" in sys.argv
    local_only_flag = "--local-only" in sys.argv

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        target = args[0]

    run_update(
        target,
        check_only=check_only_flag,
        dry_run=dry_run_flag,
        force=force_flag,
        local_only=local_only_flag
    )
