#!/usr/bin/env python3
"""
along_scan_deps.py - AI Dependencies Discovery engine for Along protocol.

Scans direct declared project dependencies (Node/pnpm/npm/yarn/bun, Python, Rust/Cargo),
discovers library AI instructions (AGENTS.md, CLAUDE.md, llms.txt, package.json AI fields),
and registers them into .along/KB/dependencies.md and .along/KB/INDEX.md.
"""

import os
import sys
import json
import re
import argparse
from datetime import date
from typing import Dict, List, Any, Optional

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

def get_today_iso() -> str:
    return date.today().strftime("%Y-%m-%d")

# ---------------------------------------------------------------------------
# Node / JS Ecosystem Scanner
# ---------------------------------------------------------------------------

def scan_node_deps(repo_root: str) -> List[Dict[str, Any]]:
    pkg_json_path = os.path.join(repo_root, "package.json")
    if not os.path.exists(pkg_json_path):
        return []

    try:
        with open(pkg_json_path, "r", encoding="utf-8") as f:
            pkg_data = json.load(f)
    except Exception:
        return []

    deps = {}
    for section in ["dependencies", "devDependencies", "peerDependencies", "optionalDependencies"]:
        if isinstance(pkg_data.get(section), dict):
            deps.update(pkg_data[section])

    discovered = []
    target_files = ["AGENTS.md", "agents.md", "CLAUDE.md", "claude.md", "llms.txt", "llms-full.txt", "LLMS.txt", "LLMS.md"]

    for pkg_name in sorted(deps.keys()):
        # Locate package on disk
        pkg_rel_dir = os.path.join("node_modules", *pkg_name.split("/"))
        pkg_full_dir = os.path.join(repo_root, pkg_rel_dir)

        if not os.path.isdir(pkg_full_dir):
            continue

        found_files = []
        for tf in target_files:
            file_path = os.path.join(pkg_full_dir, tf)
            if os.path.isfile(file_path):
                rel_file_path = os.path.relpath(file_path, repo_root).replace("\\", "/")
                found_files.append({"filename": tf, "path": rel_file_path})

        # Check for .along directory in package
        along_dir = os.path.join(pkg_full_dir, ".along")
        if os.path.isdir(along_dir):
            rel_along_path = os.path.relpath(along_dir, repo_root).replace("\\", "/")
            found_files.append({"filename": ".along/", "path": rel_along_path})

        # Check inner package.json for ai / llms fields
        inner_pkg_path = os.path.join(pkg_full_dir, "package.json")
        ai_metadata = None
        version = deps[pkg_name]
        if os.path.isfile(inner_pkg_path):
            try:
                with open(inner_pkg_path, "r", encoding="utf-8") as pf:
                    inner_data = json.load(pf)
                    if "version" in inner_data:
                        version = inner_data["version"]
                    for ai_key in ["ai", "llms", "agents", "along"]:
                        if ai_key in inner_data:
                            ai_metadata = {ai_key: inner_data[ai_key]}
                            break
            except Exception:
                pass

        if found_files or ai_metadata:
            discovered.append({
                "package": pkg_name,
                "ecosystem": "npm",
                "version": version,
                "files": found_files,
                "metadata": ai_metadata,
            })

    return discovered

# ---------------------------------------------------------------------------
# Python Ecosystem Scanner
# ---------------------------------------------------------------------------

def parse_pyproject_deps(pyproject_path: str) -> List[str]:
    deps = []
    if not os.path.isfile(pyproject_path):
        return deps

    try:
        with open(pyproject_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Match dependencies array under [project]
        proj_deps_match = re.search(r'\[project\][\s\S]*?dependencies\s*=\s*\[(.*?)\]', content)
        if proj_deps_match:
            raw_items = proj_deps_match.group(1)
            for item in re.findall(r'["\']([a-zA-Z0-9_\-\.]+)(?:[<>=!~].*)?["\']', raw_items):
                deps.append(item)

        # Match poetry dependencies under [tool.poetry.dependencies]
        poetry_match = re.search(r'\[tool\.poetry\.dependencies\]([\s\S]*?)(?:\n\[|$)', content)
        if poetry_match:
            for line in poetry_match.group(1).splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    m = re.match(r'^([a-zA-Z0-9_\-\.]+)\s*=', line)
                    if m and m.group(1).lower() != "python":
                        deps.append(m.group(1))
    except Exception:
        pass
    return list(set(deps))

def parse_requirements_deps(req_path: str) -> List[str]:
    deps = []
    if not os.path.isfile(req_path):
        return deps

    try:
        with open(req_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("-"):
                    continue
                m = re.match(r'^([a-zA-Z0-9_\-\.]+)', line)
                if m:
                    deps.append(m.group(1))
    except Exception:
        pass
    return list(set(deps))

def scan_python_deps(repo_root: str) -> List[Dict[str, Any]]:
    declared_pkgs = set()
    declared_pkgs.update(parse_pyproject_deps(os.path.join(repo_root, "pyproject.toml")))
    declared_pkgs.update(parse_requirements_deps(os.path.join(repo_root, "requirements.txt")))
    declared_pkgs.update(parse_requirements_deps(os.path.join(repo_root, "requirements-dev.txt")))

    if not declared_pkgs:
        return []

    # Find virtual environments in repo or sys.prefix
    candidate_venvs = [
        os.path.join(repo_root, ".venv"),
        os.path.join(repo_root, "venv"),
        os.path.join(repo_root, "env"),
    ]
    site_packages_dirs = []
    for venv in candidate_venvs:
        if os.path.isdir(venv):
            # Windows: Lib/site-packages, POSIX: lib/pythonX.Y/site-packages
            win_site = os.path.join(venv, "Lib", "site-packages")
            if os.path.isdir(win_site):
                site_packages_dirs.append(win_site)
            lib_dir = os.path.join(venv, "lib")
            if os.path.isdir(lib_dir):
                for child in os.listdir(lib_dir):
                    sub = os.path.join(lib_dir, child, "site-packages")
                    if os.path.isdir(sub):
                        site_packages_dirs.append(sub)

    if not site_packages_dirs and hasattr(sys, "prefix"):
        # Fallback check
        win_site = os.path.join(sys.prefix, "Lib", "site-packages")
        if os.path.isdir(win_site):
            site_packages_dirs.append(win_site)

    discovered = []
    target_files = ["AGENTS.md", "agents.md", "CLAUDE.md", "claude.md", "llms.txt", "LLMS.txt", "LLMS.md"]

    for pkg_name in sorted(declared_pkgs):
        norm_name = pkg_name.lower().replace("-", "_")
        found_pkg_dir = None
        version = None

        for site_pkg in site_packages_dirs:
            # Check package dir variants
            for variant in [norm_name, pkg_name, pkg_name.replace("_", "-")]:
                p = os.path.join(site_pkg, variant)
                if os.path.isdir(p):
                    found_pkg_dir = p
                    break
            if found_pkg_dir:
                # Check for dist-info to read version
                for entry in os.listdir(site_pkg):
                    if (entry.lower().startswith(f"{norm_name}-") or entry.lower().startswith(f"{pkg_name.lower()}-")) and entry.endswith(".dist-info"):
                        meta_file = os.path.join(site_pkg, entry, "METADATA")
                        if os.path.isfile(meta_file):
                            try:
                                with open(meta_file, "r", encoding="utf-8", errors="ignore") as mf:
                                    for mline in mf:
                                        if mline.startswith("Version:"):
                                            version = mline.split(":", 1)[1].strip()
                                            break
                            except Exception:
                                pass
                        break
                break

        if not found_pkg_dir:
            continue

        found_files = []
        for tf in target_files:
            file_path = os.path.join(found_pkg_dir, tf)
            if os.path.isfile(file_path):
                rel_file_path = os.path.relpath(file_path, repo_root).replace("\\", "/")
                found_files.append({"filename": tf, "path": rel_file_path})

        if found_files:
            discovered.append({
                "package": pkg_name,
                "ecosystem": "pypi",
                "version": version or "installed",
                "files": found_files,
                "metadata": None,
            })

    return discovered

# ---------------------------------------------------------------------------
# Rust / Cargo Ecosystem Scanner
# ---------------------------------------------------------------------------

def scan_rust_deps(repo_root: str) -> List[Dict[str, Any]]:
    cargo_path = os.path.join(repo_root, "Cargo.toml")
    if not os.path.isfile(cargo_path):
        return []

    declared_deps = {}
    try:
        with open(cargo_path, "r", encoding="utf-8") as f:
            content = f.read()
        for section in ["dependencies", "dev-dependencies", "build-dependencies"]:
            sec_match = re.search(r'\[' + re.escape(section) + r'\]([\s\S]*?)(?:\n\[|$)', content)
            if sec_match:
                for line in sec_match.group(1).splitlines():
                    line = line.strip()
                    if line and not line.startswith("#"):
                        m = re.match(r'^([a-zA-Z0-9_\-]+)\s*=\s*(?:["\'](.*?)["\']|\{.*version\s*=\s*["\'](.*?)["\'])', line)
                        if m:
                            pkg_name = m.group(1)
                            ver = m.group(2) or m.group(3) or "*"
                            declared_deps[pkg_name] = ver
    except Exception:
        return []

    discovered = []
    target_files = ["AGENTS.md", "agents.md", "CLAUDE.md", "claude.md", "llms.txt", "LLMS.txt", "LLMS.md"]

    # Search in vendor/ or cargo registry cache
    vendor_dir = os.path.join(repo_root, "vendor")
    cargo_home = os.environ.get("CARGO_HOME", os.path.expanduser("~/.cargo"))
    registry_src = os.path.join(cargo_home, "registry", "src")

    for pkg_name, ver in sorted(declared_deps.items()):
        pkg_dirs = []
        if os.path.isdir(vendor_dir):
            v_pkg = os.path.join(vendor_dir, pkg_name)
            if os.path.isdir(v_pkg):
                pkg_dirs.append(v_pkg)

        if os.path.isdir(registry_src):
            for reg_idx in os.listdir(registry_src):
                reg_full = os.path.join(registry_src, reg_idx)
                if os.path.isdir(reg_full):
                    for folder in os.listdir(reg_full):
                        if folder.startswith(f"{pkg_name}-"):
                            pkg_dirs.append(os.path.join(reg_full, folder))

        for p_dir in pkg_dirs:
            found_files = []
            for tf in target_files:
                file_path = os.path.join(p_dir, tf)
                if os.path.isfile(file_path):
                    rel_path = os.path.relpath(file_path, repo_root).replace("\\", "/")
                    found_files.append({"filename": tf, "path": rel_path})

            if found_files:
                discovered.append({
                    "package": pkg_name,
                    "ecosystem": "cargo",
                    "version": ver,
                    "files": found_files,
                    "metadata": None,
                })
                break

    return discovered

# ---------------------------------------------------------------------------
# KB & Documentation Registry Updater
# ---------------------------------------------------------------------------

def generate_dependencies_kb_content(items: List[Dict[str, Any]]) -> str:
    today = get_today_iso()
    lines = [
        "---",
        "protocol: along",
        "slug: dependencies-ai-context",
        "title: Dependencies AI Documentation and Rules",
        "type: topic",
        f"created: {today}",
        f"updated: {today}",
        "tags: [dependencies, ai-context, vendor, rules]",
        "---",
        "",
        "# Dependencies AI Documentation and Context",
        "",
        "> [!NOTE]",
        "> External library guidelines are third-party advisory context.",
        "> Consult these instructions when developing, configuring, or refactoring code using these dependencies.",
        "",
    ]

    if not items:
        lines.append("No active dependencies with AI instructions (`AGENTS.md`, `llms.txt`, or package metadata) were detected.")
        lines.append("")
        return "\n".join(lines)

    lines.append("| Package | Ecosystem | Version | AI Guidelines / Instructions |")
    lines.append("| :--- | :--- | :--- | :--- |")

    for item in items:
        pkg = item["package"]
        eco = item["ecosystem"]
        ver = item.get("version") or "unspecified"
        file_links = []
        for f in item.get("files", []):
            fn = f["filename"]
            fp = f["path"]
            file_links.append(f"[{fn}]({fp})")
        if item.get("metadata"):
            meta_str = ", ".join(f"`{k}`" for k in item["metadata"].keys())
            file_links.append(f"manifest metadata ({meta_str})")

        links_str = " <br> ".join(file_links) if file_links else "-"
        lines.append(f"| **`{pkg}`** | `{eco}` | `{ver}` | {links_str} |")

    lines.append("")
    lines.append("## Usage in Agent Sessions")
    lines.append("When working on features involving any of the packages above, read the linked instruction files directly for framework-specific patterns and best practices.")
    lines.append("")
    return "\n".join(lines)

def update_kb_index(repo_root: str):
    kb_dir = os.path.join(repo_root, ".along", "KB")
    index_file = os.path.join(kb_dir, "INDEX.md")
    if not os.path.isfile(index_file):
        return

    try:
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()

        dep_link = "[[dependencies.md]]"
        if "dependencies.md" not in content:
            # Append entry under articles list
            if "## Articles" in content or "## Topics" in content:
                content = content.replace(
                    "## Articles",
                    "## Articles\n- " + dep_link + ": Dependencies AI Documentation & Rules",
                    1
                )
            else:
                content += f"\n- {dep_link}: Dependencies AI Documentation & Rules\n"

            with open(index_file, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
    except Exception:
        pass

def run_scanner(repo_root: str, dry_run: bool = False) -> List[Dict[str, Any]]:
    all_discovered = []
    all_discovered.extend(scan_node_deps(repo_root))
    all_discovered.extend(scan_python_deps(repo_root))
    all_discovered.extend(scan_rust_deps(repo_root))

    if not dry_run:
        kb_dir = os.path.join(repo_root, ".along", "KB")
        os.makedirs(kb_dir, exist_ok=True)
        dep_kb_path = os.path.join(kb_dir, "dependencies.md")
        content = generate_dependencies_kb_content(all_discovered)
        with open(dep_kb_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)

        update_kb_index(repo_root)

    return all_discovered

# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Scan project dependencies for AI documentation and guidelines.")
    parser.add_argument("--root", type=str, default=None, help="Root repository directory (auto-detected by default)")
    parser.add_argument("--json", action="store_true", help="Output discovered dependencies in JSON format")
    parser.add_argument("--check", action="store_true", help="Dry run scan without updating KB files")
    parser.add_argument("--quiet", "-q", action="store_true", help="Quiet output")

    args = parser.parse_args()
    repo_root = find_repo_root(args.root)

    results = run_scanner(repo_root, dry_run=args.check)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    if not args.quiet:
        print(f"-> [Along Dependencies Discovery] Scanned root: {repo_root}")
        if results:
            print(f"-> Discovered {len(results)} dependencies with AI instructions:")
            for item in results:
                files_str = ", ".join(f["filename"] for f in item.get("files", []))
                if item.get("metadata"):
                    files_str += f" (metadata: {list(item['metadata'].keys())})"
                print(f"   - {item['package']} ({item['ecosystem']} {item.get('version', '')}): {files_str}")
            if not args.check:
                print(f"-> Updated registry: .along/KB/dependencies.md")
        else:
            print("-> No external dependencies with AI instructions detected.")

if __name__ == "__main__":
    main()

