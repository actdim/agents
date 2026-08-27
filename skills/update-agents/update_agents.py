#!/usr/bin/env python3
"""
update_agents.py - Automated one-liner updater engine for ACTDIM-AGENTS-PROTOCOL.

Checks protocol versions across:
  1. Target repository (./AGENTS.md)
  2. Globally installed agent skills (~/.gemini/config, ~/.claude, ~/.codex, ~/.config/opencode)
  3. Remote GitHub repository (https://github.com/actdim/agents.git)

Workflow:
  - If remote version > global version: updates global skills via install.ps1 / install.sh from git.
  - If global version >= remote version: uses installed global skills.
  - Applies managed protocol refresh & migration engine (migrate_protocol.py) to target repository.

Usage:
    python skills/update-agents/update_agents.py [TARGET_REPO_ROOT] [OPTIONS]
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
    # 1. Try git ls-remote tags first
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
                sorted_tags = sorted([parse_semver(t) for t in tags], reverse=True)
                return semver_to_str(sorted_tags[0])
    except Exception:
        pass

    # 2. Fallback: query raw AGENTS.md on main branch via HTTP
    try:
        req = urllib.request.Request(
            REMOTE_RAW_URL,
            headers={"User-Agent": "actdim-agents-updater"}
        )
        with urllib.request.urlopen(req, timeout=NETWORK_TIMEOUT_SECS) as resp:
            raw_text = resp.read().decode("utf-8", errors="ignore")
            m = re.search(r"ACTDIM-AGENTS-PROTOCOL v(\d+\.\d+\.\d+)", raw_text)
            if m:
                return m.group(1)
    except Exception:
        pass

    return None

def is_dev_repo(repo_root):
    if os.path.exists(os.path.join(repo_root, "install.ps1")) and \
       os.path.exists(os.path.join(repo_root, "skills", "init-agents", "protocol.md")) and \
       os.path.exists(os.path.join(repo_root, "scripts", "bump-version.py")):
        return True
    return False

def get_cache_repo_dir():
    user_home = os.path.expanduser("~")
    cache_dir = os.path.join(user_home, ".cache", "actdim-agents")
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, "repo")

def update_global_from_git(dry_run=False):
    cache_repo = get_cache_repo_dir()
    print(f"-> Updating global installation from {REMOTE_GIT_URL}...")
    if dry_run:
        print("   [DRY-RUN] Would clone/pull remote repository and execute installer.")
        return True

    try:
        if os.path.exists(os.path.join(cache_repo, ".git")):
            print(f"   Fetching latest changes in {cache_repo}...")
            subprocess.run(["git", "-C", cache_repo, "fetch", "--all", "--tags"], check=True, timeout=30)
            subprocess.run(["git", "-C", cache_repo, "reset", "--hard", "origin/main"], check=True, timeout=30)
        else:
            if os.path.exists(cache_repo):
                shutil.rmtree(cache_repo, ignore_errors=True)
            print(f"   Cloning fresh repository to {cache_repo}...")
            subprocess.run(["git", "clone", "--depth", "1", REMOTE_GIT_URL, cache_repo], check=True, timeout=30)

        # Run installer
        if os.name == "nt":
            ps_script = os.path.join(cache_repo, "install.ps1")
            cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps_script, "-Target", "all"]
        else:
            sh_script = os.path.join(cache_repo, "install.sh")
            cmd = ["bash", sh_script]

        print(f"   Executing installer: {' '.join(cmd)}")
        res = subprocess.run(cmd, check=True)
        return res.returncode == 0
    except Exception as e:
        print(f"   [ERROR] Failed to update global installation from git: {e}")
        return False

def install_global_from_local(repo_root, dry_run=False):
    print(f"-> Performing local global deployment from {repo_root}...")
    if dry_run:
        print("   [DRY-RUN] Would run local install script.")
        return True

    try:
        if os.name == "nt":
            ps_script = os.path.join(repo_root, "install.ps1")
            cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps_script, "-Target", "all"]
        else:
            sh_script = os.path.join(repo_root, "install.sh")
            cmd = ["bash", sh_script]

        res = subprocess.run(cmd, check=True)
        return res.returncode == 0
    except Exception as e:
        print(f"   [ERROR] Local installer failed: {e}")
        return False

def apply_migration_to_repo(repo_root, dry_run=False):
    print(f"-> Applying protocol refresh & migration to: {repo_root}")
    if dry_run:
        print("   [DRY-RUN] Would refresh AGENTS.md managed block and run migrate_protocol.py.")
        return True

    # 1. Locate protocol.md source
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
        return False

    with open(protocol_src, "r", encoding="utf-8") as f:
        protocol_text = f.read().strip()

    # 2. Update AGENTS.md managed block
    agents_md = os.path.join(repo_root, "AGENTS.md")
    begin_marker = "<!-- BEGIN ACTDIM-AGENTS-PROTOCOL root (managed by init-agents - do not edit by hand) -->"
    end_marker = "<!-- END ACTDIM-AGENTS-PROTOCOL -->"

    block = f"{begin_marker}\n{protocol_text}\n{end_marker}"

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
        print("   [OK] Refreshed managed protocol block in AGENTS.md.")
    else:
        with open(agents_md, "w", encoding="utf-8") as f:
            f.write(block + "\n\n## Project specifics\n\n- Add project conventions here.\n")
        print("   [OK] Created AGENTS.md with managed protocol block.")

    # 3. Locate and execute migrate_protocol.py
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

    if migrate_script:
        print(f"   Executing migration engine: {migrate_script}")
        res = subprocess.run([sys.executable, migrate_script, repo_root])
        return res.returncode == 0
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

    # Apply changes to target repository
    apply_migration_to_repo(repo_root, dry_run=dry_run)
    print("==================================================")
    print("-> [OK] Repository agent context successfully updated!")

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

